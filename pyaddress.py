from dotenv import load_dotenv
from os import environ, path

import multiprocessing as mp
import pycep_correios as pc
import pandas as pd
import argparse
import requests
import time
import glob
import os


def get_address(cep: str, source: str) -> {}:
    if source == 'pycep':
        return pc.get_address_from_cep(cep)
    elif source == 'webmania':
        basedir = path.abspath(path.dirname(__file__))
        load_dotenv(path.join(basedir, '.env'))
        url = (
            f'https://webmaniabr.com/api/1/cep/{cep}/'
            f'?app_key={environ.get("APP_KEY")}'
            f'&app_secret={environ.get("APP_SECRET")}'
        )
    elif source == 'apicep':
        url = f'https://ws.apicep.com/cep.json?code={cep}'
    elif source == 'postmon':
        url = f'https://api.postmon.com.br/v1/cep/{cep}'
    elif source == 'viacep':
        url = f'https://viacep.com.br/ws/{cep}/json/'
    else:
        raise ValueError('Source does not exist')

    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    return {}


def process_addr(
    row: int, df: pd.DataFrame, cep_col: str, source: str
) -> pd.DataFrame:
    assert cep_col in df.columns, f'Column {cep_col} does not exist'

    aux = df.loc[[row]]
    cep = str(aux.loc[row, cep_col])
    addr = get_address(cep, source)

    for col in addr.keys():
        aux.loc[row, col] = str(addr.get(col))
    print(f'[INFO] {cep} processed')

    return aux


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    '-f',
    '--files',
    type=str,
    nargs='+',
    required=True,
    help='list of input files',
)
ap.add_argument(
    '-cc',
    '--cep-col',
    type=str,
    required=True,
    help='CEP col',
)
ap.add_argument(
    '-o', '--output', type=str, required=True, help='path to output file'
)
ap.add_argument(
    '-c',
    '--compress',
    type=str,
    default=None,
    help='type of compression, default is None',
)
ap.add_argument(
    '-s',
    '--source',
    type=str,
    default='postmon',
    help=(
        "source of download,types: ['pycep', 'webmania', 'apicep', 'postmon',"
        "'viacep'], default is postmon"
    ),
)
ap.add_argument(
    '-d',
    '--delete',
    default=False,
    action='store_true',
    help='delete input files, default if False',
)
ap.add_argument(
    '--sleep',
    type=int,
    default=2,
    help='sleep to next request, default is 2',
)
args = vars(ap.parse_args())


# Directory for checkpoint files
if not os.path.exists('.process'):
    os.mkdir('.process')

files = args.get('files')
for file in files:
    df = pd.read_csv(file, low_memory=False, compression=args.get('compress'))
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap_async(
        process_addr,
        [
            (row, df, args.get('cep_col'), args.get('source'))
            for row in range(len(df))
        ],
    ).get()
    pool.close()
    pool.join()

    out = f".process/{file.split('/')[-1]}"
    aux = pd.concat(list(results))
    aux.to_csv(out, index=False, compression=args.get('compress'))

    print(f"[INFO] Done {file} (processed)")
    if args.get('delete'):
        print(f"[INFO] Deleting {file}")
        os.remove(file)

    time.sleep(args.get('sleep'))

checkpoints = glob.glob('.process/*')

aux = pd.DataFrame()
for file in checkpoints:
    print(f"[INFO] Merging [{file}]")
    df = pd.read_csv(file, low_memory=False, compression=args.get('compress'))
    aux = pd.concat([df, aux], ignore_index=True)

aux.to_csv(args.get('output'), index=False, compression=args.get('compress'))
print(f"[INFO] Done [{args.get('output')}]")
