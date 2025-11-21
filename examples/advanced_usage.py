#!/usr/bin/env python3
"""
Advanced EarthCARE Downloader Usage Example

This example demonstrates advanced features including multiple products,
baseline filtering, and geographic constraints.
"""

import os
from pathlib import Path
from datetime import datetime
from earthcare_downloader import EarthCareDownloader

def main():
    """Advanced usage example."""
    
    # Configuration from environment variables (recommended for security)
    username = os.getenv('OADS_USERNAME')
    password = os.getenv('OADS_PASSWORD')
    
    if not username or not password:
        print("Please set OADS_USERNAME and OADS_PASSWORD environment variables")
        print("Example:")
        print("  export OADS_USERNAME='your_username'")
        print("  export OADS_PASSWORD='your_password'")
        return
    
    # CSV file with datetime and location information
    csv_file = "sample_data_with_locations.csv"
    
    # Multiple products to download
    products = [
        'ATL_NOM_1B',   # ATLID Level 1B
        'MSI_NOM_1B',   # MSI Level 1B
        'CPR_NOM_1B'    # CPR Level 1B
    ]
    
    # Base download directory
    base_download_dir = Path("./downloads_advanced")
    
    # Initialize downloader with specific baseline
    downloader = EarthCareDownloader(
        username=username,
        password=password,
        collection='EarthCAREL1Validated',  # Validated L1 products
        baseline='BA',  # Specific baseline
        verbose=True
    )
    
    print("Starting advanced download with multiple products...")
    print(f"Products: {', '.join(products)}")
    print(f"Collection: EarthCAREL1Validated")
    print(f"Baseline: BA")
    
    # Download each product type
    total_summary = {
        'downloaded': [],
        'skipped': [],
        'failed': []
    }
    
    for product in products:
        print(f"\n--- Downloading {product} ---")
        
        # Create product-specific directory
        product_dir = base_download_dir / product
        product_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            summary = downloader.download_from_csv(
                csv_file_path=csv_file,
                products=[product],
                download_directory=str(product_dir),
                override=False,
                radius_search=500,  # 500 km radius search
                # bounding_box=(-30, -20, 130, 150)  # Optional bounding box [lat_min, lat_max, lon_min, lon_max]
            )
            
            # Aggregate results
            total_summary['downloaded'].extend(summary['downloaded'])
            total_summary['skipped'].extend(summary['skipped'])
            total_summary['failed'].extend(summary['failed'])
            
            print(f"  Downloaded: {len(summary['downloaded'])} files")
            print(f"  Skipped: {len(summary['skipped'])} files")
            print(f"  Failed: {len(summary['failed'])} files")
            
        except Exception as e:
            print(f"  Error downloading {product}: {e}")
            continue
    
    # Final summary
    print("\n" + "="*50)
    print("FINAL DOWNLOAD SUMMARY")
    print("="*50)
    print(f"Total Downloaded: {len(total_summary['downloaded'])} files")
    print(f"Total Skipped: {len(total_summary['skipped'])} files")
    print(f"Total Failed: {len(total_summary['failed'])} files")
    
    # Save summary to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = base_download_dir / f"download_summary_{timestamp}.txt"
    
    with open(summary_file, 'w') as f:
        f.write(f"EarthCARE Download Summary - {datetime.now()}\n")
        f.write("="*50 + "\n\n")
        f.write(f"Products: {', '.join(products)}\n")
        f.write(f"Collection: EarthCAREL1Validated\n")
        f.write(f"Baseline: BA\n\n")
        f.write(f"Total Downloaded: {len(total_summary['downloaded'])} files\n")
        f.write(f"Total Skipped: {len(total_summary['skipped'])} files\n")
        f.write(f"Total Failed: {len(total_summary['failed'])} files\n\n")
        
        if total_summary['downloaded']:
            f.write("Downloaded Files:\n")
            for file_info in total_summary['downloaded']:
                f.write(f"  - {file_info}\n")
        
        if total_summary['failed']:
            f.write("\nFailed Downloads:\n")
            for file_info in total_summary['failed']:
                f.write(f"  - {file_info}\n")
    
    print(f"\nDetailed summary saved to: {summary_file}")

if __name__ == "__main__":
    main()