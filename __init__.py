"""
EarthCARE Data Downloader Package

A comprehensive Python package for downloading EarthCARE satellite products 
from ESA's Online Archive and Distribution System (OADS).
"""

__version__ = "1.0.1"
__author__ = "Onrona Functions"
__email__ = "your-email@domain.com"
__license__ = "MIT"

from .earthcare_downloader import EarthCareDownloader
from .earthcare_downloader_gui import EarthCareDownloaderGUI

__all__ = ["EarthCareDownloader", "EarthCareDownloaderGUI"]