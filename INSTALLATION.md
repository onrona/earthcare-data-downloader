# EarthCARE Downloader - Installation Guide

## Requirements Installation

### Option 1: Install all dependencies (recommended)

```bash
pip install -r requirements.txt
```

### Option 2: Install minimal dependencies for downloader only

```bash
pip install -r requirements_gui.txt
```

### Option 3: Manual installation of essential packages

```bash
pip install requests beautifulsoup4 lxml pandas tqdm
```

## Python Version

- **Required**: Python 3.7 or higher
- **Recommended**: Python 3.9 or higher

## GUI Dependencies

- **tkinter**: Usually included with Python installation
- **threading** and **queue**: Part of Python standard library

## Usage

### Run the GUI Interface

```bash
python earthcare_downloader_gui.py
```

### Use the downloader directly

```python
from earthcare_downloader import EarthCareDownloader

downloader = EarthCareDownloader(
    username="your_username",
    password="your_password",
    collection='EarthCAREL1InstChecked'
)
```

## Verification

To verify all dependencies are installed correctly:

```bash
python -c "from earthcare_downloader_gui import EarthCareDownloaderGUI; print('GUI imports successfully')"
```

## Troubleshooting

### Common Issues

1. **tkinter not found**: Install python3-tk on Linux: `sudo apt-get install python3-tk`
2. **lxml installation fails**: Install libxml2-dev: `sudo apt-get install libxml2-dev libxslt-dev`
3. **pandas issues**: Ensure numpy is installed first: `pip install numpy`

### Platform-specific notes

- **Windows**: All dependencies should install without issues
- **macOS**: May need to install Xcode command line tools
- **Linux**: May need additional system packages for lxml and cartopy

## License

See project license for usage terms.
