# CEP2Address 🏠

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A powerful and efficient Python tool for batch processing Brazilian postal codes (CEP) into complete addresses using multiple data sources. This tool is designed to handle large datasets with parallel processing capabilities and supports various output formats.

## ✨ Features

- **Multiple Data Sources**: Support for various Brazilian postal code APIs:
  - Postmon
  - ViaCEP
  - CEPLA
  - APICEP
  - WebMania
  - Google Geocoding
  - Correios (via pycep-correios)

- **High Performance**:
  - Parallel processing using multiprocessing
  - Efficient batch processing of large datasets
  - Configurable request delays to prevent API rate limiting

- **Flexible Input/Output**:
  - Supports multiple input files
  - Various compression formats
  - Customizable output formats
  - Checkpoint system for large datasets

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/patricksferraz/cep2address.git
cd cep2address
```

2. Install dependencies:
```bash
pip install -r dev-requirements.txt
```

3. Set up your environment variables (optional, for APIs that require authentication):
```bash
cp .env-example .env
# Edit .env with your API keys
```

## 💻 Usage

Basic usage:
```bash
python pyaddress.py -f input.csv -cc cep_column -o output.csv
```

Advanced usage with options:
```bash
python pyaddress.py \
  -f input1.csv input2.csv \
  -cc postal_code \
  -o results.csv \
  -s viacep \
  --sleep 1 \
  --compress gzip
```

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `-f, --files` | Input file(s) | Required |
| `-cc, --cep-col` | Column name containing CEP | Required |
| `-o, --output` | Output file path | Required |
| `-s, --source` | Data source | postmon |
| `--sleep` | Delay between requests (seconds) | 2 |
| `-c, --compress` | Compression type | None |
| `-d, --delete` | Delete input files after processing | False |

## 🔧 Development

The project uses several development tools to maintain code quality:

- **Black**: Code formatting
- **Pylama**: Code linting
- **Pydocstyle**: Documentation style checking

To run the development tools:
```bash
black pyaddress.py
pylama pyaddress.py
pydocstyle pyaddress.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all the Brazilian postal code API providers
- The Python community for the amazing tools and libraries
- All contributors who have helped improve this project

## 📫 Contact

Project Link: [https://github.com/patricksferraz/cep2address](https://github.com/patricksferraz/cep2address)
