#!/usr/bin/env python3
"""
GUI Example for EarthCARE Downloader

This example shows how to customize and extend the GUI interface.
"""

import tkinter as tk
from tkinter import ttk
from earthcare_downloader_gui import EarthCareDownloaderGUI

class CustomEarthCareGUI(EarthCareDownloaderGUI):
    """
    Custom version of the EarthCARE GUI with additional features.
    """
    
    def __init__(self):
        super().__init__()
        
        # Customize window
        self.root.title("Custom EarthCARE Data Downloader v1.0")
        self.root.configure(bg='#f0f0f0')
        
        # Add custom features
        self.add_custom_features()
    
    def add_custom_features(self):
        """Add custom features to the GUI."""
        
        # Add a status bar
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Version label
        version_label = ttk.Label(
            self.status_bar, 
            text="EarthCARE Downloader v1.0 | Onrona Functions",
            font=('Arial', 8)
        )
        version_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Connection status
        self.connection_status = ttk.Label(
            self.status_bar,
            text="● Ready",
            foreground='green',
            font=('Arial', 8)
        )
        self.connection_status.pack(side=tk.LEFT, padx=(10, 0))
    
    def start_download(self):
        """Override start_download to update connection status."""
        self.connection_status.config(text="● Downloading...", foreground='orange')
        super().start_download()
    
    def download_completed(self, summary):
        """Override download_completed to update connection status."""
        self.connection_status.config(text="● Completed", foreground='blue')
        super().download_completed(summary)
    
    def download_error(self, error_message):
        """Override download_error to update connection status."""
        self.connection_status.config(text="● Error", foreground='red')
        super().download_error(error_message)

def main():
    """Run the custom GUI."""
    try:
        app = CustomEarthCareGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        print("Make sure tkinter is properly installed")

if __name__ == "__main__":
    main()