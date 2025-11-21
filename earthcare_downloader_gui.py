#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: earthcare_downloader_gui.py
Author: Onrona Functions
Created: 2025-11-20
Version: 1.0
Description:
    Graphical User Interface for EarthCARE Downloader.
    Provides an interactive interface to configure and run downloads.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import queue
import time
from earthcare_downloader import EarthCareDownloader

# Import baseline data
try:
    from aux_data import aux_dict_L1, aux_dict_L2
except ImportError:
    # Fallback if aux_data.py is not found
    aux_dict_L1 = {}
    aux_dict_L2 = {}


class EarthCareDownloaderGUI:
    """
    Graphical User Interface for EarthCARE product downloads.
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EarthCARE Data Downloader")
        self.root.geometry("1200x600")  # Increased height to accommodate integrated log
        self.root.resizable(True, True)
        
        # Variables
        self.csv_file_path = tk.StringVar()
        self.download_directory = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.collection = tk.StringVar()
        self.baseline = tk.StringVar()
        self.product_category = tk.StringVar()  # New variable for product category
        self.selected_product = tk.StringVar()  # New variable for selected product
        self.orbit_column = tk.StringVar()
        self.override_files = tk.BooleanVar()
        self.verbose_mode = tk.BooleanVar()
        
        # Status variables
        self.is_downloading = False
        self.downloader = None
        self.log_queue = queue.Queue()
        self.current_entry = 0
        self.total_entries = 0
        
        # Combine baseline dictionaries
        self.all_baselines = {**aux_dict_L1, **aux_dict_L2}
        
        # Collections available
        self.collections = {
            'EarthCARE L1 Products (Cal/Val Users)': 'EarthCAREL1InstChecked',
            'EarthCARE L1 Products (Validated)': 'EarthCAREL1Validated',
            'EarthCARE L2 Products (Cal/Val Users)': 'EarthCAREL2InstChecked',
            'EarthCARE L2 Products (Validated)': 'EarthCAREL2Validated',
            'EarthCARE L2 Products (Commissioning)': 'EarthCAREL2Products',
            'EarthCARE Auxiliary Data': 'EarthCAREAuxiliary',
            'EarthCARE Orbit Data': 'EarthCAREOrbitData',
            'JAXA L2 Products (Cal/Val Users)': 'JAXAL2InstChecked',
            'JAXA L2 Products (Validated)': 'JAXAL2Validated',
            'JAXA L2 Products (Commissioning)': 'JAXAL2Products'
        }
        
        # Product categories
        self.product_categories = {
            'ATLID Level 1B': ['ATL_NOM_1B', 'ATL_DCC_1B', 'ATL_CSC_1B', 'ATL_FSC_1B'],
            'MSI Level 1B': ['MSI_NOM_1B', 'MSI_BBS_1B', 'MSI_SD1_1B', 'MSI_SD2_1B'],
            'BBR Level 1B': ['BBR_NOM_1B', 'BBR_SNG_1B', 'BBR_SOL_1B', 'BBR_LIN_1B'],
            'CPR Level 1B': ['CPR_NOM_1B'],
            'MSI Level 1C': ['MSI_RGR_1C'],
            'Auxiliary Level 1D': ['AUX_MET_1D', 'AUX_JSG_1D'],
            'ATLID Level 2A': ['ATL_FM__2A', 'ATL_AER_2A', 'ATL_ICE_2A', 'ATL_TC__2A', 
                              'ATL_EBD_2A', 'ATL_CTH_2A', 'ATL_ALD_2A'],
            'MSI Level 2A': ['MSI_CM__2A', 'MSI_COP_2A', 'MSI_AOT_2A'],
            'CPR Level 2A': ['CPR_FMR_2A', 'CPR_CD__2A', 'CPR_TC__2A', 'CPR_CLD_2A', 'CPR_APC_2A'],
            'Level 2B Combined': ['AM__MO__2B', 'AM__CTH_2B', 'AM__ACD_2B', 'AC__TC__2B',
                                 'BM__RAD_2B', 'BMA_FLX_2B', 'ACM_CAP_2B', 'ACM_COM_2B',
                                 'ACM_RT__2B', 'ALL_DF__2B', 'ALL_3D__2B'],
            'Orbit Data': ['MPL_ORBSCT', 'AUX_ORBPRE', 'AUX_ORBRES']
        }
        
        # Baselines available
        self.baselines = ['Auto-detect', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ',
                         'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ']
        
        # Products available
        self.products = {
            'ATLID Level 1B': ['ATL_NOM_1B', 'ATL_DCC_1B', 'ATL_CSC_1B', 'ATL_FSC_1B'],
            'MSI Level 1B': ['MSI_NOM_1B', 'MSI_BBS_1B', 'MSI_SD1_1B', 'MSI_SD2_1B'],
            'BBR Level 1B': ['BBR_NOM_1B', 'BBR_SNG_1B', 'BBR_SOL_1B', 'BBR_LIN_1B'],
            'CPR Level 1B': ['CPR_NOM_1B'],
            'MSI Level 1C': ['MSI_RGR_1C'],
            'Auxiliary Level 1D': ['AUX_MET_1D', 'AUX_JSG_1D'],
            'ATLID Level 2A': ['ATL_FM__2A', 'ATL_AER_2A', 'ATL_ICE_2A', 'ATL_TC__2A', 
                              'ATL_EBD_2A', 'ATL_CTH_2A', 'ATL_ALD_2A'],
            'MSI Level 2A': ['MSI_CM__2A', 'MSI_COP_2A', 'MSI_AOT_2A'],
            'CPR Level 2A': ['CPR_FMR_2A', 'CPR_CD__2A', 'CPR_TC__2A', 'CPR_CLD_2A', 'CPR_APC_2A'],
            'Level 2B Combined': ['AM__MO__2B', 'AM__CTH_2B', 'AM__ACD_2B', 'AC__TC__2B',
                                 'BM__RAD_2B', 'BMA_FLX_2B', 'ACM_CAP_2B', 'ACM_COM_2B',
                                 'ACM_RT__2B', 'ALL_DF__2B', 'ALL_3D__2B'],
            'Orbit Data': ['MPL_ORBSCT', 'AUX_ORBPRE', 'AUX_ORBRES']
        }
        
        # Set default values
        self.collection.set('EarthCAREL1InstChecked')
        self.baseline.set('Auto-detect')
        self.override_files.set(False)
        self.verbose_mode.set(False)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        
        # Main frame 
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(main_frame, text="EarthCARE Data Downloader", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Create main content frame with two columns
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column for controls (fixed, no scroll)
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        # Create notebook for tabs in left frame
        self.notebook = ttk.Notebook(left_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Configuration tab
        self.create_config_tab()
        
        # Advanced tab
        self.create_advanced_tab()
        
        # Control buttons frame
        control_frame = ttk.Frame(left_frame)
        control_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Download button
        self.download_btn = ttk.Button(control_frame, text="Start Download", 
                                      command=self.start_download,
                                      style='Accent.TButton')
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        self.cancel_btn = ttk.Button(control_frame, text="Cancel", 
                                    command=self.cancel_download,
                                    state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear form button
        clear_btn = ttk.Button(control_frame, text="Clear Form", 
                              command=self.clear_form)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Right column for status and log
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Status frame in right column
        status_frame = ttk.LabelFrame(right_frame, text="Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(status_frame, text="Ready to download")
        self.status_label.pack(anchor=tk.W)
        
        # Progress information
        self.progress_info_label = ttk.Label(status_frame, text="")
        self.progress_info_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # File progress bar
        self.file_progress_label = ttk.Label(status_frame, text="")
        self.file_progress_label.pack(anchor=tk.W, pady=(10, 0))
        
        self.file_progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.file_progress.pack(fill=tk.X, pady=(5, 0))
        
        # Download Log frame (integrated in right column)
        log_frame = ttk.LabelFrame(right_frame, text="Download Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Log text widget with scrollbar
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text widget
        self.log_text = tk.Text(log_text_frame, wrap=tk.WORD, height=15, width=50, 
                               bg='#f8f9fa', font=('Consolas', 9))
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Log control frame
        log_control_frame = ttk.Frame(log_frame)
        log_control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Clear log button
        clear_log_btn = ttk.Button(log_control_frame, text="Clear Log", 
                                  command=self.clear_log)
        clear_log_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save log button
        save_log_btn = ttk.Button(log_control_frame, text="Save Log", 
                                 command=self.save_log)
        save_log_btn.pack(side=tk.LEFT)
        
        # Auto-scroll checkbox
        self.auto_scroll = tk.BooleanVar(value=True)
        auto_scroll_check = ttk.Checkbutton(log_control_frame, text="Auto-scroll", 
                                          variable=self.auto_scroll)
        auto_scroll_check.pack(side=tk.RIGHT)
        
        # Start processing log messages
        self.process_log_queue()
        
        # Add initial welcome message to log
        self.add_log_message("🌍 EarthCARE Data Downloader initialized and ready", 'info')
        
    def create_config_tab(self):
        """Create the configuration tab."""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Configuration")
        
        # Direct frame without scrollbar (fixed content)
        main_config_frame = ttk.Frame(config_frame)
        main_config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Credentials section
        cred_frame = ttk.LabelFrame(main_config_frame, text="OADS Credentials", padding=10)
        cred_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(cred_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        username_entry = ttk.Entry(cred_frame, textvariable=self.username, width=40)
        username_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=(0, 10))
        
        ttk.Label(cred_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        password_entry = ttk.Entry(cred_frame, textvariable=self.password, show="*", width=40)
        password_entry.grid(row=1, column=1, sticky=tk.W+tk.E)
        
        cred_frame.columnconfigure(1, weight=1)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_config_frame, text="File Selection", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # CSV file selection
        ttk.Label(file_frame, text="CSV File:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        csv_frame = ttk.Frame(file_frame)
        csv_frame.grid(row=0, column=1, sticky=tk.W+tk.E, pady=(0, 10))
        
        csv_entry = ttk.Entry(csv_frame, textvariable=self.csv_file_path, width=35)
        csv_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        csv_btn = ttk.Button(csv_frame, text="Browse...", command=self.browse_csv_file)
        csv_btn.pack(side=tk.RIGHT)
        
        # Download directory selection
        ttk.Label(file_frame, text="Download Directory:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        dir_frame = ttk.Frame(file_frame)
        dir_frame.grid(row=1, column=1, sticky=tk.W+tk.E)
        
        dir_entry = ttk.Entry(dir_frame, textvariable=self.download_directory, width=35)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        dir_btn = ttk.Button(dir_frame, text="Browse...", command=self.browse_download_directory)
        dir_btn.pack(side=tk.RIGHT)
        
        file_frame.columnconfigure(1, weight=1)
        
        # Product Selection section
        product_frame = ttk.LabelFrame(main_config_frame, text="Product Selection", padding=10)
        product_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Collection selection
        ttk.Label(product_frame, text="Collection:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.collection_combo = ttk.Combobox(product_frame, textvariable=self.collection,
                                           values=list(self.collections.keys()), state="readonly", width=50)
        self.collection_combo.grid(row=0, column=1, sticky=tk.W+tk.E, pady=(0, 10))
        self.collection_combo.bind('<<ComboboxSelected>>', self.on_collection_changed)
        
        # Product Category selection
        ttk.Label(product_frame, text="Product Category:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.category_combo = ttk.Combobox(product_frame, textvariable=self.product_category,
                                         state="readonly", width=50)
        self.category_combo.grid(row=1, column=1, sticky=tk.W+tk.E, pady=(0, 10))
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_changed)
        
        # Available Product selection
        ttk.Label(product_frame, text="Available Product:").grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.product_combo = ttk.Combobox(product_frame, textvariable=self.selected_product,
                                        state="readonly", width=50)
        self.product_combo.grid(row=2, column=1, sticky=tk.W+tk.E, pady=(0, 10))
        self.product_combo.bind('<<ComboboxSelected>>', self.on_product_changed)
        
        # Baseline selection
        ttk.Label(product_frame, text="Baseline:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        self.baseline_combo = ttk.Combobox(product_frame, textvariable=self.baseline,
                                         state="readonly", width=50)
        self.baseline_combo.grid(row=3, column=1, sticky=tk.W+tk.E)
        
        product_frame.columnconfigure(1, weight=1)
        
        # Set default values
        self.collection.set('EarthCARE L1 Products (Cal/Val Users)')
        self.override_files.set(False)
        self.verbose_mode.set(False)
        
        # Initialize product categories
        self.on_collection_changed()
        
    def create_advanced_tab(self):
        """Create the advanced options tab."""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="Advanced")
        
        # Create scrollable frame
        canvas = tk.Canvas(advanced_frame)
        scrollbar = ttk.Scrollbar(advanced_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # CSV Options
        csv_options_frame = ttk.LabelFrame(scrollable_frame, text="CSV Options", padding=15)
        csv_options_frame.pack(fill=tk.X, pady=(10, 15))
        
        ttk.Label(csv_options_frame, text="Orbit Column Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        orbit_entry = ttk.Entry(csv_options_frame, textvariable=self.orbit_column, width=30)
        orbit_entry.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(csv_options_frame, text="(Optional - leave empty if not available)", 
                 font=('Arial', 8)).grid(row=1, column=1, sticky=tk.W, pady=(5, 0))
        
        # Download Options
        download_options_frame = ttk.LabelFrame(scrollable_frame, text="Download Options", padding=15)
        download_options_frame.pack(fill=tk.X, pady=(0, 15))
        
        override_check = ttk.Checkbutton(download_options_frame, 
                                        text="Override existing files",
                                        variable=self.override_files)
        override_check.pack(anchor=tk.W, pady=(0, 10))
        
        verbose_check = ttk.Checkbutton(download_options_frame, 
                                       text="Verbose output (detailed logging)",
                                       variable=self.verbose_mode)
        verbose_check.pack(anchor=tk.W)
        
        # Information section
        info_frame = ttk.LabelFrame(scrollable_frame, text="Information", padding=15)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = """
CSV File Requirements:
• The CSV file will be automatically analyzed to detect:
  - Column separator (comma, semicolon, tab, etc.)
  - Date column (formats like yyyy-mm-dd, date, fecha, etc.)
  - Time column (formats like hh:mm:ss.sss, time, hora, etc.)

Collection Information:
• Cal/Val Users: For calibration and validation users
• Validated: Fully validated products
• Commissioning: For commissioning team use

Baseline Information:
• Auto-detect will choose the most common baseline
• Manual selection allows specific baseline filtering
        """
        
        info_label = ttk.Label(info_frame, text=info_text.strip(), justify=tk.LEFT)
        info_label.pack(anchor=tk.W)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def add_log_message(self, message, level='info'):
        """Add a message to the log queue."""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        self.log_queue.put((timestamp, message, level))
    
    def process_log_queue(self):
        """Process messages from the log queue."""
        try:
            while True:
                timestamp, message, level = self.log_queue.get_nowait()
                
                # Add to log window
                log_entry = f"[{timestamp}] {message}\n"
                self.log_text.insert(tk.END, log_entry)
                
                # Color coding based on level
                if level == 'error':
                    # Configure tag for error messages
                    self.log_text.tag_configure("error", foreground="red")
                    start_index = f"{self.log_text.index(tk.END).split('.')[0]}.0"
                    end_index = tk.END
                    self.log_text.tag_add("error", f"{int(start_index.split('.')[0])-1}.0", end_index)
                elif level == 'warning':
                    self.log_text.tag_configure("warning", foreground="orange")
                    start_index = f"{self.log_text.index(tk.END).split('.')[0]}.0"
                    end_index = tk.END
                    self.log_text.tag_add("warning", f"{int(start_index.split('.')[0])-1}.0", end_index)
                elif level == 'success':
                    self.log_text.tag_configure("success", foreground="green")
                    start_index = f"{self.log_text.index(tk.END).split('.')[0]}.0"
                    end_index = tk.END
                    self.log_text.tag_add("success", f"{int(start_index.split('.')[0])-1}.0", end_index)
                
                # Auto-scroll to bottom if enabled
                if hasattr(self, 'auto_scroll') and self.auto_scroll.get():
                    self.log_text.see(tk.END)
                
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_log_queue)
    
    def clear_log(self):
        """Clear the log window."""
        self.log_text.delete(1.0, tk.END)
    
    def save_log(self):
        """Save the log to a file."""
        file_path = filedialog.asksaveasfilename(
            title="Save Log File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Log Saved", f"Log saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save log: {e}")
        
    def on_collection_changed(self, event=None):
        """Handle collection combobox selection change."""
        # Update product categories based on collection
        self.category_combo.set('')
        self.product_combo.set('')
        self.baseline_combo.set('')
        self.selected_product.set('')
        self.product_category.set('')
        self.baseline.set('')
        
        # Set available categories (for now, show all)
        self.category_combo['values'] = list(self.product_categories.keys())
    
    def on_category_changed(self, event=None):
        """Handle product category selection change."""
        category = self.product_category.get()
        if category and category in self.product_categories:
            # Update available products
            self.product_combo['values'] = self.product_categories[category]
            self.product_combo.set('')
            self.baseline_combo.set('')
            self.selected_product.set('')
            self.baseline.set('')
    
    def on_product_changed(self, event=None):
        """Handle product selection change."""
        product = self.selected_product.get()
        if product:
            # Get available baselines for this product
            available_baselines = ['Auto-detect']
            if product in self.all_baselines:
                available_baselines.extend(self.all_baselines[product])
            
            self.baseline_combo['values'] = available_baselines
            self.baseline.set('Auto-detect')
    
    def get_selected_products(self):
        """Get the currently selected product as a list (for compatibility)."""
        if self.selected_product.get():
            return [self.selected_product.get()]
        return []
        # """Update the selected products display."""
        # selected_indices = self.products_listbox.curselection()
        # selected_products = [self.products_listbox.get(i) for i in selected_indices]
        
        # if selected_products:
        #     self.products_selected.set(','.join(selected_products))
        #     self.selected_products_label.config(text=f"Selected: {', '.join(selected_products)}")
        # else:
        #     self.products_selected.set('')
        #     self.selected_products_label.config(text="No products selected")
    
    def browse_csv_file(self):
        """Open file dialog to select CSV file."""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        if file_path:
            self.csv_file_path.set(file_path)
    
    def browse_download_directory(self):
        """Open directory dialog to select download directory."""
        dir_path = filedialog.askdirectory(
            title="Select Download Directory",
            initialdir=os.getcwd()
        )
        if dir_path:
            self.download_directory.set(dir_path)
    
    def validate_inputs(self):
        """Validate all input fields."""
        errors = []
        
        if not self.username.get().strip():
            errors.append("Username is required")
        
        if not self.password.get().strip():
            errors.append("Password is required")
        
        if not self.csv_file_path.get().strip():
            errors.append("CSV file must be selected")
        elif not os.path.exists(self.csv_file_path.get()):
            errors.append("CSV file does not exist")
        
        if not self.download_directory.get().strip():
            errors.append("Download directory must be selected")
        
        if not self.selected_product.get().strip():
            errors.append("Product must be selected")
        
        return errors
    
    def start_download(self):
        """Start the download process."""
        # Validate inputs
        errors = self.validate_inputs()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        
        # Clear log
        self.clear_log()
        
        # Update GUI state
        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress.config(mode='determinate')
        self.progress['value'] = 0
        self.file_progress.start(10)
        self.status_label.config(text="Initializing download...")
        self.progress_info_label.config(text="")
        self.file_progress_label.config(text="")
        
        self.add_log_message("🚀 Starting EarthCARE download process...")
        
        # Start download in separate thread
        download_thread = threading.Thread(target=self.run_download)
        download_thread.daemon = True
        download_thread.start()
    
    def run_download(self):
        """Run the actual download process."""
        try:
            # Create downloader instance
            baseline = self.baseline.get() if self.baseline.get() != 'Auto-detect' else None
            
            # Get collection ID from the collections dictionary
            collection_name = self.collection.get()
            collection_id = self.collections.get(collection_name, collection_name)
            
            self.downloader = EarthCareDownloaderGUI_Custom(
                username=self.username.get().strip(),
                password=self.password.get().strip(),
                collection=collection_id,
                baseline=baseline,
                verbose=False,  # Keep False for clean terminal output
                gui_callback=self.add_log_message,
                progress_callback=self.update_progress
            )
            
            # Update status
            self.add_log_message("✅ Downloader initialized successfully")
            
            # Prepare products list (single product now)
            products = [self.selected_product.get()]
            self.add_log_message(f"📦 Product to download: {products[0]}")
            
            # Prepare orbit column
            orbit_col = self.orbit_column.get().strip() if self.orbit_column.get().strip() else None
            
            # Update status
            self.add_log_message("🔄 Starting download process...")
            
            # Run download
            summary = self.downloader.download_from_csv(
                csv_file_path=self.csv_file_path.get(),
                products=products,
                download_directory=self.download_directory.get(),
                orbit_column=orbit_col,
                override=self.override_files.get()
            )
            
            # Download completed successfully
            self.root.after(0, lambda: self.download_completed(summary))
            
        except Exception as e:
            # Handle errors
            self.add_log_message(f"Critical error: {str(e)}", 'error')
            self.root.after(0, lambda: self.download_error(str(e)))
    
    def update_progress(self, current, total, message=""):
        """Update progress bars and status."""
        def update_gui():
            if total > 0:
                progress_percent = (current / total) * 100
                self.progress['value'] = progress_percent
                self.progress_info_label.config(text=f"Processing entry {current}/{total} ({progress_percent:.1f}%)")
            
            if message:
                self.file_progress_label.config(text=message)
        
        self.root.after(0, update_gui)
    
    def download_completed(self, summary):
        """Handle successful download completion."""
        self.progress['value'] = 100
        self.file_progress.stop()
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        
        # Log completion
        self.add_log_message("🎉 Download completed successfully!", 'success')
        self.add_log_message(f"📊 Processed entries: {summary['processed_entries']}/{summary['total_entries']}", 'success')
        self.add_log_message(f"⬇️ Downloaded files: {len(summary['downloaded_files'])}", 'success')
        self.add_log_message(f"⏭️ Skipped files: {len(summary['skipped_files'])}", 'success')
        self.add_log_message(f"❌ Failed files: {len(summary['failed_files'])}", 'success')
        self.add_log_message(f"⏱️ Execution time: {summary['execution_time']}", 'success')
        
        # Create summary message
        message = f"""Download completed successfully!

Processed entries: {summary['processed_entries']}/{summary['total_entries']}
Downloaded files: {len(summary['downloaded_files'])}
Skipped files: {len(summary['skipped_files'])}
Failed files: {len(summary['failed_files'])}
Execution time: {summary['execution_time']}

Check the download directory for detailed logs."""
        
        self.status_label.config(text="Download completed successfully!")
        self.progress_info_label.config(text=f"Completed: {summary['processed_entries']}/{summary['total_entries']} entries")
        self.file_progress_label.config(text="")
        messagebox.showinfo("Download Complete", message)
    
    def download_error(self, error_message):
        """Handle download errors."""
        self.progress['value'] = 0
        self.file_progress.stop()
        self.is_downloading = False
        self.download_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        
        self.status_label.config(text="Download failed!")
        self.progress_info_label.config(text="")
        self.file_progress_label.config(text="")
        self.add_log_message(f"❌ Download failed: {error_message}", 'error')
        messagebox.showerror("Download Error", f"Download failed with error:\n\n{error_message}")
    
    def cancel_download(self):
        """Cancel the ongoing download."""
        if self.is_downloading:
            # Note: This is a simple implementation
            # For a more robust solution, you'd need to implement proper thread cancellation
            self.progress['value'] = 0
            self.file_progress.stop()
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL)
            self.cancel_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Download cancelled by user")
            self.progress_info_label.config(text="")
            self.file_progress_label.config(text="")
            self.add_log_message("⏹️ Download cancelled by user", 'warning')
            messagebox.showinfo("Download Cancelled", "Download has been cancelled.")
    
    def clear_form(self):
        """Clear all form fields."""
        self.csv_file_path.set('')
        self.download_directory.set('')
        self.username.set('')
        self.password.set('')
        self.orbit_column.set('')
        self.selected_product.set('')
        self.product_category.set('')
        self.override_files.set(False)
        self.verbose_mode.set(False)
        self.collection.set('EarthCARE L1 Products (Cal/Val Users)')
        self.baseline.set('Auto-detect')
        
        # Clear combo selections
        self.category_combo.set('')
        self.product_combo.set('')
        self.baseline_combo.set('')
        
        self.status_label.config(text="Ready to download")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


class EarthCareDownloaderGUI_Custom(EarthCareDownloader):
    """Custom version of EarthCareDownloader that sends messages to GUI."""
    
    def __init__(self, username, password, collection='EarthCAREL1InstChecked', 
                 baseline=None, verbose=False, gui_callback=None, progress_callback=None):
        # Initialize normally but intercept prints
        super().__init__(username, password, collection, baseline, verbose)
        self.gui_callback = gui_callback
        self.progress_callback = progress_callback
        self.current_entry = 0
        self.total_entries = 0
        self.terminal_progress_bar = None
        self.original_print = print  # Store original print function
    
    def _log_to_gui(self, message, level='info'):
        """Send important messages to GUI only."""
        if self.gui_callback:
            self.gui_callback(message, level)
    
    def _print_summary(self, summary):
        """Print final summary to terminal like original code."""
        self.original_print("\n" + "=" * 60)
        self.original_print("           EarthCARE Download Summary")
        self.original_print("=" * 60)
        self.original_print(f"Execution time: {summary['execution_time']}")
        self.original_print(f"Total entries processed: {summary['processed_entries']}/{summary['total_entries']}")
        self.original_print(f"Files downloaded: {len(summary['downloaded_files'])}")
        self.original_print(f"Files skipped (already exist): {len(summary['skipped_files'])}")
        self.original_print(f"Files failed: {len(summary['failed_files'])}")
        self.original_print(f"Errors encountered: {len(summary['errors'])}")
        
        if summary['downloaded_files']:
            self.original_print(f"\n✅ Successfully downloaded {len(summary['downloaded_files'])} files")
        
        if summary['skipped_files']:
            self.original_print(f"⏭️  Skipped {len(summary['skipped_files'])} files (already exist)")
        
        if summary['failed_files']:
            self.original_print(f"❌ Failed to download {len(summary['failed_files'])} files")
        
        if summary['errors']:
            self.original_print(f"⚠️  {len(summary['errors'])} errors encountered")
            self.original_print("   Check the error log file for details.")
        
        self.original_print("=" * 60)
    
    def download_from_csv(self, csv_file_path, products, download_directory, 
                         orbit_column=None, override=False, radius_search=None, bounding_box=None):
        """Override to add progress tracking and GUI feedback."""
        import builtins
        from tqdm import tqdm
        
        # Temporarily redirect print to suppress output except for our progress bar
        def quiet_print(*args, **kwargs):
            # Only allow tqdm and our specific prints
            pass
        
        # Store original print and replace temporarily
        original_builtin_print = builtins.print
        builtins.print = quiet_print
        
        try:
            start_time = self._get_datetime_now()
            
            # Initialize execution summary
            summary = {
                'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'total_entries': 0,
                'processed_entries': 0,
                'downloaded_files': [],
                'skipped_files': [],
                'failed_files': [],
                'errors': [],
                'execution_time': None
            }
            
            # Auto-detect CSV separator
            separator = self._detect_csv_separator(csv_file_path)
            self._log(f"Detected CSV separator: '{separator}'")
            self._log_to_gui(f"📄 CSV file loaded successfully (separator: '{separator}')")
            
            # Load CSV file with detected separator
            import pandas as pd
            df = pd.read_csv(csv_file_path, sep=separator)
            
            # Auto-detect datetime columns
            date_col, time_col = self._find_datetime_columns(df)
            
            if not date_col or not time_col:
                available_cols = list(df.columns)
                error_msg = f"Could not automatically detect date/time columns. Available columns: {available_cols}"
                self._log(error_msg, 'error')
                self._log_to_gui("❌ Could not detect date/time columns in CSV", 'error')
                summary['errors'].append(error_msg)
                return summary
            
            self._log(f"Using date column: '{date_col}', time column: '{time_col}'")
            self._log_to_gui(f"📅 Using columns: {date_col} (date), {time_col} (time)")
            
            # Create download directory if it doesn't exist
            import os
            os.makedirs(download_directory, exist_ok=True)
            
            # Convert products to valid product names
            if isinstance(products, str):
                products = [products]
            product_names = [self.string_to_product_name(prod) for prod in products]
            
            # Get product search template
            template = self.get_product_search_template()
            
            summary['total_entries'] = len(df)
            self.total_entries = len(df)
            
            self._log(f"Processing {len(df)} entries...")
            self._log_to_gui(f"🚀 Starting download for {len(df)} entries")
            
            # Restore print temporarily for tqdm, then suppress again
            builtins.print = original_builtin_print
            self.terminal_progress_bar = tqdm(total=len(df), desc="Processing entries", unit="entry")
            builtins.print = quiet_print
            
            try:
                for index, row in df.iterrows():
                    self.current_entry = index + 1
                    
                    try:
                        date_str = str(row[date_col])
                        time_str = str(row[time_col])
                        
                        # Handle time string formatting
                        if '.' in time_str:
                            time_parts = time_str.split('.')
                            if len(time_parts[1]) > 3:
                                time_str = time_parts[0] + '.' + time_parts[1][:3]
                        
                        datetime_str = f"{date_str} {time_str}"
                        
                        # Update progress
                        if self.progress_callback:
                            self.progress_callback(self.current_entry, self.total_entries, 
                                                 f"Processing {datetime_str}")
                        
                        # Update terminal progress bar description
                        self.terminal_progress_bar.set_description(f"Processing {datetime_str[:19]}")
                        
                        # Log to file and GUI
                        self._log(f"Processing entry {index + 1}/{len(df)}: {datetime_str}")
                        self._log_to_gui(f"🔍 Processing entry {self.current_entry}/{self.total_entries}: {datetime_str}")
                        
                        # Prepare search parameters
                        search_params = {
                            'productType_text': '[' + ','.join(product_names) + ']',
                            'start_time_text': self.format_datetime_string(datetime_str),
                            'end_time_text': self.format_datetime_string(datetime_str)
                        }
                        
                        # Add orbit number if available
                        if orbit_column and orbit_column in df.columns:
                            orbit_number = row[orbit_column]
                            if pd.notna(orbit_number):
                                search_params['orbit_number_text'] = str(int(orbit_number))
                        
                        # Search for products (using original method)
                        dataframe = self.get_product_list(template, **search_params)
                        
                        # Apply baseline filtering
                        dataframe, selected_baseline = self.filter_by_baseline(dataframe)
                        
                        if dataframe.empty:
                            self._log(f"No products found for {datetime_str}")
                            self._log_to_gui(f"⚠️ No products found for {datetime_str}", 'warning')
                            self.terminal_progress_bar.update(1)
                            continue
                        
                        # Log detailed info
                        self._log(f"Found {len(dataframe)} products for {datetime_str} (baseline: {selected_baseline})")
                        self._log_to_gui(f"✅ Found {len(dataframe)} products (baseline: {selected_baseline})")
                        
                        # Download products (using original method)
                        download_result = self.download_products(dataframe, download_directory, override)
                        
                        # Update summary
                        summary['downloaded_files'].extend(download_result['downloaded'])
                        summary['skipped_files'].extend(download_result['skipped'])
                        summary['failed_files'].extend(download_result['failed'])
                        
                        # Show download results in GUI
                        if download_result['downloaded']:
                            for file in download_result['downloaded']:
                                self._log_to_gui(f"⬇️ Downloaded: {file}", 'success')
                        
                        if download_result['skipped']:
                            for file in download_result['skipped']:
                                self._log_to_gui(f"⏭️ Skipped: {file} (already exists)")
                        
                        if download_result['failed']:
                            for file in download_result['failed']:
                                self._log_to_gui(f"❌ Failed: {file}", 'error')
                        
                        summary['processed_entries'] += 1
                        self.terminal_progress_bar.update(1)
                        
                    except Exception as e:
                        error_msg = f"Error processing entry {index + 1} ({datetime_str}): {str(e)}"
                        self._log(error_msg, 'error')
                        self._log_to_gui(f"❌ Error processing {datetime_str}", 'error')
                        summary['errors'].append({
                            'entry': index + 1,
                            'datetime': datetime_str,
                            'error': str(e),
                            'orbit': row.get(orbit_column, 'N/A') if orbit_column and orbit_column in df.columns else 'N/A'
                        })
                        self.terminal_progress_bar.update(1)
                        
            except Exception as e:
                self._log(f"Error during processing: {str(e)}", 'error')
                self._log_to_gui(f"❌ Critical processing error", 'error')
                
            finally:
                # Close terminal progress bar
                if self.terminal_progress_bar:
                    self.terminal_progress_bar.close()
        
        except Exception as e:
            error_msg = f"Critical error during execution: {str(e)}"
            self._log(error_msg, 'error')
            self._log_to_gui(f"❌ Critical error: {str(e)}", 'error')
            summary['errors'].append(error_msg)
        
        finally:
            # Always restore original print
            builtins.print = original_builtin_print
        
        # Calculate execution time
        end_time = self._get_datetime_now()
        execution_time = end_time - start_time
        summary['execution_time'] = str(execution_time)
        summary['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Save execution summary
        self._save_execution_summary(summary, download_directory)
        
        # Print terminal summary
        self._print_summary(summary)
        
        # Final summary to GUI
        self._log_to_gui(f"🎉 Download completed! {len(summary['downloaded_files'])} downloaded, {len(summary['skipped_files'])} skipped, {len(summary['failed_files'])} failed", 'success')
        
        return summary
    
    def _get_datetime_now(self):
        """Get current datetime."""
        from datetime import datetime
        return datetime.now()


if __name__ == "__main__":
    app = EarthCareDownloaderGUI()
    app.run()