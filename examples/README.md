# Examples

This directory contains examples demonstrating how to use the EarthCARE Downloader.

## Available Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates simple usage of the EarthCARE downloader for downloading a single product type.

**Features:**

- Environment variable configuration
- Single product download
- Basic error handling
- Download summary

**Run:**

```bash
python basic_usage.py
```

### 2. Advanced Usage (`advanced_usage.py`)

Shows advanced features including multiple products, baseline filtering, and geographic constraints.

**Features:**

- Multiple product downloads
- Baseline filtering
- Geographic radius search
- Summary file generation
- Error handling for individual products

**Run:**

```bash
python advanced_usage.py
```

### 3. GUI Example (`gui_example.py`)

Demonstrates how to customize and extend the GUI interface.

**Features:**

- Custom GUI styling
- Status bar with connection indicator
- Override methods for custom behavior
- Enhanced user experience

**Run:**

```bash
python gui_example.py
```

## Sample Data

### `sample_data.csv`

A sample CSV file with the required format for the downloader:

- Date column (yyyy-mm-dd format)
- Time column (hh:mm:ss.sss format)
- Latitude and longitude (optional)
- Orbit information (optional)

## Prerequisites

Before running the examples:

1. **Set environment variables for credentials:**

   ```bash
   # Windows (PowerShell)
   $env:OADS_USERNAME="your_username"
   $env:OADS_PASSWORD="your_password"
   
   # Windows (CMD)
   set OADS_USERNAME=your_username
   set OADS_PASSWORD=your_password
   
   # Linux/macOS
   export OADS_USERNAME="your_username"
   export OADS_PASSWORD="your_password"
   ```

2. **Ensure you have valid OADS credentials**
   - Register at [ESA OADS](https://eocat.esa.int/oads/)
   - Obtain your username and password

3. **Prepare your CSV data**
   - Use `sample_data.csv` as a reference
   - Ensure proper datetime format
   - Include geographic coordinates if using spatial filtering

## Tips

- Start with `basic_usage.py` to understand the fundamentals
- Modify the sample CSV file with your actual data points
- Use `advanced_usage.py` for complex download scenarios
- Customize `gui_example.py` for your specific GUI needs

## Troubleshooting

- **Credentials Error**: Verify your OADS username and password
- **Network Issues**: Check internet connection and proxy settings
- **CSV Format**: Ensure your CSV follows the expected format
- **GUI Issues**: Make sure tkinter is properly installed

For more help, see the main [README.md](../README.md) or [INSTALLATION.md](../INSTALLATION.md).
