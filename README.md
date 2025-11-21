# EarthCARE Data Downloader 🛰️

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/psf/black)

A comprehensive Python application for downloading EarthCARE satellite products from the ESA's Online Archive and Distribution System (OADS). Features both command-line and graphical user interfaces for efficient bulk downloads of atmospheric and cloud observation data.

## ✨ Features

- 🖥️ **Dual Interface**: Command-line tool and intuitive GUI
- 📊 **CSV-based Downloads**: Bulk download using CSV files with datetime information
- 🔍 **Smart Detection**: Automatic CSV separator and datetime column detection
- 🎯 **Product Filtering**: Support for multiple EarthCARE product types and baselines
- 📈 **Progress Tracking**: Real-time download progress with detailed logging
- ⚙️ **Flexible Configuration**: Multiple collection types and search parameters
- 🔄 **Resume Support**: Skip already downloaded files with override option
- 📝 **Comprehensive Logging**: Detailed execution logs and download summaries

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/earthcare_downloader.git
cd earthcare_downloader

# Install dependencies
pip install -r requirements.txt
```

### GUI Usage

```bash
python earthcare_downloader_gui.py
```

### Command Line Usage

```python
from earthcare_downloader import EarthCareDownloader

# Initialize downloader
downloader = EarthCareDownloader(
    username="your_oads_username",
    password="your_oads_password",
    collection='EarthCAREL1InstChecked',
    baseline='BA',
    verbose=True
)

# Download products from CSV
summary = downloader.download_from_csv(
    csv_file_path="path/to/your/data.csv",
    products=['ATL_NOM_1B', 'MSI_NOM_1B'],
    download_directory="./downloads",
    override=False
)
```

## 📋 Supported Products

### Level 1B Products

- **ATLID**: `ATL_NOM_1B`, `ATL_DCC_1B`, `ATL_CSC_1B`, `ATL_FSC_1B`
- **MSI**: `MSI_NOM_1B`, `MSI_BBS_1B`, `MSI_SD1_1B`, `MSI_SD2_1B`
- **BBR**: `BBR_NOM_1B`, `BBR_SNG_1B`, `BBR_SOL_1B`, `BBR_LIN_1B`
- **CPR**: `CPR_NOM_1B`

### Level 1C Products

- **MSI**: `MSI_RGR_1C`

### Level 1D Products

- **Auxiliary**: `AUX_MET_1D`, `AUX_JSG_1D`

### Level 2A Products

- **ATLID**: `ATL_FM__2A`, `ATL_AER_2A`, `ATL_ICE_2A`, `ATL_TC__2A`, `ATL_EBD_2A`, `ATL_CTH_2A`, `ATL_ALD_2A`
- **MSI**: `MSI_CM__2A`, `MSI_COP_2A`, `MSI_AOT_2A`
- **CPR**: `CPR_FMR_2A`, `CPR_CD__2A`, `CPR_TC__2A`, `CPR_CLD_2A`, `CPR_APC_2A`

### Level 2B Combined Products

- **Atmospheric Motion**: `AM__MO__2B`, `AM__CTH_2B`, `AM__ACD_2B`
- **Atmospheric Composition**: `AC__TC__2B`
- **Broadband Radiometer**: `BM__RAD_2B`, `BMA_FLX_2B`
- **Active Combination**: `ACM_CAP_2B`, `ACM_COM_2B`, `ACM_RT__2B`
- **All Instruments**: `ALL_DF__2B`, `ALL_3D__2B`

### Orbit Data

- **Mission Planning**: `MPL_ORBSCT`
- **Auxiliary Orbit**: `AUX_ORBPRE`, `AUX_ORBRES`

## 📊 Collections Available

| Collection Name | Collection ID | Description |
|-----------------|---------------|-------------|
| EarthCARE L1 Products (Cal/Val) | `EarthCAREL1InstChecked` | Level 1 products for calibration/validation users |
| EarthCARE L1 Products (Validated) | `EarthCAREL1Validated` | Validated Level 1 products |
| EarthCARE L2 Products (Cal/Val) | `EarthCAREL2InstChecked` | Level 2 products for calibration/validation users |
| EarthCARE L2 Products (Validated) | `EarthCAREL2Validated` | Validated Level 2 products |
| EarthCARE L2 Products (Commissioning) | `EarthCAREL2Products` | Commissioning Level 2 products |
| EarthCARE Auxiliary Data | `EarthCAREAuxiliary` | Auxiliary data products |
| EarthCARE Orbit Data | `EarthCAREOrbitData` | Orbit data products |
| JAXA L2 Products (Cal/Val) | `JAXAL2InstChecked` | JAXA Level 2 products for calibration/validation |
| JAXA L2 Products (Validated) | `JAXAL2Validated` | Validated JAXA Level 2 products |
| JAXA L2 Products (Commissioning) | `JAXAL2Products` | Commissioning JAXA Level 2 products |

## 📁 CSV File Format

Your CSV file should contain datetime information. The downloader automatically detects:

- **Date columns**: `yyyy-mm-dd`, `date`, `fecha`, `day`
- **Time columns**: `hh:mm:ss.sss`, `hh:mm:ss`, `time`, `hora`, `hour`
- **CSV separators**: Automatic detection of `,`, `;`, `\t`

Example CSV format:

```csv
date,time,latitude,longitude,orbit
2024-06-15,12:30:45.123,-25.5,135.2,12345
2024-06-15,14:15:20.456,-30.1,140.8,12346
```

## ⚙️ Configuration Options

### Baselines

- `Auto-detect` (default)
- `AA`, `AB`, `AC`, `AD`, `AE`, `AF`, `AG`, `AH`, `AI`, `AJ`
- `BA`, `BB`, `BC`, `BD`, `BE`, `BF`, `BG`, `BH`, `BI`, `BJ`

### Search Parameters

- **Radius Search**: Geographic radius around points
- **Bounding Box**: Geographic area constraints
- **Orbit Column**: Specify orbit number column in CSV
- **Override Files**: Redownload existing files

## 🖼️ GUI Interface

The graphical interface provides:

1. **Configuration Tab**: Set credentials, file paths, and basic settings
2. **Products Tab**: Select product categories and specific products
3. **Advanced Tab**: Configure search parameters and output options
4. **Real-time Logging**: Monitor download progress and status
5. **Progress Tracking**: Visual progress bars for overall and individual file downloads

## 📖 Documentation

- [Installation Guide](INSTALLATION.md) - Detailed installation instructions
- [API Reference](docs/api.md) - Complete API documentation (coming soon)
- [Examples](examples/) - Usage examples and tutorials (coming soon)

## 🔧 Requirements

- **Python**: 3.7+ (3.9+ recommended)
- **Core Dependencies**: requests, beautifulsoup4, lxml, pandas, tqdm
- **GUI Dependencies**: tkinter (usually included with Python)

See [requirements.txt](requirements.txt) for complete dependency list.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure your OADS credentials are correct
2. **Network Timeouts**: Check your internet connection and proxy settings
3. **File Permission Errors**: Ensure write permissions to download directory
4. **Missing Dependencies**: Run `pip install -r requirements.txt`

### Getting Help

- 📧 Email: [your-email@domain.com](mailto:your-email@domain.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/earthcare_downloader/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/your-username/earthcare_downloader/discussions)

## 🎯 Roadmap

- [ ] Add support for additional satellite missions
- [ ] Implement parallel downloads
- [ ] Add data visualization capabilities
- [ ] Create web-based interface
- [ ] Add automated testing
- [ ] Docker containerization

## 🙏 Acknowledgments

- ESA for providing the EarthCARE mission data
- OADS team for the data distribution system
- Open source community for the excellent Python libraries

---

---

⭐ **Star this repository if you find it useful!** ⭐
