#!/usr/bin/env python3
"""
Basic EarthCARE Downloader Usage Example

This example demonstrates basic usage of the EarthCARE downloader
for downloading satellite products from OADS.
"""

import os
from pathlib import Path
from earthcare_downloader import EarthCareDownloader

def main():
    """Basic usage example."""
    
    # Configuration
    username = os.getenv('OADS_USERNAME')  # Set your username in environment variable
    password = os.getenv('OADS_PASSWORD')  # Set your password in environment variable
    
    if not username or not password:
        print("Please set OADS_USERNAME and OADS_PASSWORD environment variables")
        return
    
    # CSV file with datetime information
    csv_file = "sample_data.csv"
    
    # Products to download
    products = ['ATL_NOM_1B']  # ATLID Level 1B Nominal
    
    # Download directory
    download_dir = Path("./downloads") / products[0]
    download_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize downloader
    downloader = EarthCareDownloader(
        username=username,
        password=password,
        collection='EarthCAREL1InstChecked',  # Cal/Val L1 products
        baseline='Auto-detect',
        verbose=True
    )
    
    print(f"Starting download of {products[0]} products...")
    
    # Perform download
    try:
        summary = downloader.download_from_csv(
            csv_file_path=csv_file,
            products=products,
            download_directory=str(download_dir),
            override=False  # Skip already downloaded files
        )
        
        print("\n=== Download Summary ===")
        print(f"Downloaded: {len(summary['downloaded'])} files")
        print(f"Skipped: {len(summary['skipped'])} files")
        print(f"Failed: {len(summary['failed'])} files")
        
    except FileNotFoundError:
        print(f"CSV file '{csv_file}' not found. Please create it with datetime data.")
    except Exception as e:
        print(f"Error during download: {e}")

if __name__ == "__main__":
    main()