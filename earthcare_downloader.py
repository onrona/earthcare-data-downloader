#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: earthcare_downloader.py
Author: Onrona Functions
Created: 2025-11-20
Version: 1.0
Description:
    A class-based script for downloading EarthCARE products from OADS.
    Organizes functionality from oads_download_baseline.py into a structured class.
"""

import os
import re
import requests
import time
import pandas as pd
from urllib.parse import urlparse
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from lxml import html
from datetime import datetime
from pathlib import Path
import logging
from tqdm import tqdm
import csv
import io
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


class EarthCareDownloader:
    """
    A class for downloading EarthCARE products from OADS based on CSV input files.
    """
    
    def __init__(self, username, password, collection='EarthCAREL1InstChecked', baseline=None, verbose=False):
        """
        Initialize the EarthCare downloader.
        
        Parameters:
        - username: str, OADS username for authentication
        - password: str, OADS password for authentication  
        - collection: str, collection identifier for product search
        - baseline: str, specific baseline to filter by (e.g. 'AC', 'AD', 'AE', 'BA', etc.)
        - verbose: bool, whether to show detailed output during execution
        """
        self.username = username
        self.password = password
        self.collection = collection
        self.baseline = baseline
        self.verbose = verbose
        self.execution_log = []
        
        # Configure logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO if self.verbose else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler() if self.verbose else logging.NullHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _log(self, message, level='info'):
        """Log message and add to execution log."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self.execution_log.append(log_entry)
        
        if self.verbose:
            if level == 'error':
                self.logger.error(message)
            elif level == 'warning':
                self.logger.warning(message)
            else:
                self.logger.info(message)
    
    def _detect_csv_separator(self, csv_file_path):
        """Automatically detect CSV separator."""
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # Read first few lines to detect separator
            sample = file.read(1024)
            file.seek(0)
            
            # Use csv.Sniffer to detect dialect
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample, delimiters=',;\t|')
                return dialect.delimiter
            except:
                # Fallback: test common separators
                separators = [',', ';', '\t', '|']
                line = file.readline().strip()
                
                max_columns = 0
                best_separator = ','
                
                for sep in separators:
                    column_count = len(line.split(sep))
                    if column_count > max_columns:
                        max_columns = column_count
                        best_separator = sep
                
                return best_separator
    
    def _find_datetime_columns(self, df):
        """Find datetime columns in the dataframe automatically."""
        date_col = None
        time_col = None
        
        # Patterns to look for
        date_patterns = ['yyyy-mm-dd', 'date', 'fecha', 'day']
        time_patterns = ['hh:mm:ss.sss', 'hh:mm:ss', 'time', 'hora', 'hour']
        
        # Search for exact matches first
        for col in df.columns:
            col_lower = col.lower().strip()
            if col_lower in ['yyyy-mm-dd']:
                date_col = col
            elif col_lower in ['hh:mm:ss.sss', 'hh:mm:ss']:
                time_col = col
        
        # If not found, search for partial matches
        if not date_col:
            for col in df.columns:
                col_lower = col.lower().strip()
                for pattern in date_patterns:
                    if pattern in col_lower or col_lower in pattern:
                        date_col = col
                        break
                if date_col:
                    break
        
        if not time_col:
            for col in df.columns:
                col_lower = col.lower().strip()
                for pattern in time_patterns:
                    if pattern in col_lower or col_lower in pattern:
                        time_col = col
                        break
                if time_col:
                    break
        
        # Try to identify by data format
        if not date_col or not time_col:
            for col in df.columns:
                sample_value = str(df[col].iloc[0]) if not df[col].empty else ''
                
                # Check if it looks like a date (YYYY-MM-DD format)
                if not date_col and re.match(r'\d{4}-\d{2}-\d{2}', sample_value):
                    date_col = col
                
                # Check if it looks like time (HH:MM:SS format)
                if not time_col and re.match(r'\d{2}:\d{2}:\d{2}', sample_value):
                    time_col = col
        
        return date_col, time_col
        
    def format_datetime_string(self, datetime_string):
        """Format datetime string to the required format."""
        timestamp = pd.Timestamp(datetime_string)
        if timestamp.tzinfo is None:
            timestamp = timestamp.tz_localize('UTC')
        return timestamp.strftime('%Y-%m-%dT%XZ')

    def string_to_product_name(self, input_string):
        """Convert user input string to valid EarthCARE product name."""
        product_name_input = input_string.replace(' ','').replace('-','').replace('_','').lower()

        file_types = [
            # ATLID level 1b
            'ATL_NOM_1B',
            'ATL_DCC_1B',
            'ATL_CSC_1B',
            'ATL_FSC_1B',
            # MSI level 1b
            'MSI_NOM_1B',
            'MSI_BBS_1B',
            'MSI_SD1_1B',
            'MSI_SD2_1B',
            # BBR level 1b
            'BBR_NOM_1B',
            'BBR_SNG_1B',
            'BBR_SOL_1B',
            'BBR_LIN_1B',
            # CPR level 1b  #@ JAXA product
            'CPR_NOM_1B',   #@ JAXA product
            # MSI level 1c
            'MSI_RGR_1C',
            # level 1d
            'AUX_MET_1D',
            'AUX_JSG_1D',
            # ATLID level 2a
            'ATL_FM__2A',
            'ATL_AER_2A',
            'ATL_ICE_2A',
            'ATL_TC__2A',
            'ATL_EBD_2A',
            'ATL_CTH_2A',
            'ATL_ALD_2A',
            # MSI level 2a
            'MSI_CM__2A',
            'MSI_COP_2A',
            'MSI_AOT_2A',
            # CPR level 2a
            'CPR_FMR_2A',
            'CPR_CD__2A',
            'CPR_TC__2A',
            'CPR_CLD_2A',
            'CPR_APC_2A',
            # ATLID-MSI level 2b
            'AM__MO__2B',
            'AM__CTH_2B',
            'AM__ACD_2B',
            # ATLID-CPR level 2b
            'AC__TC__2B',
            # BBR-MSI-(ATLID) level 2b
            'BM__RAD_2B',
            'BMA_FLX_2B',
            # ATLID-CPR-MSI level 2b
            'ACM_CAP_2B',
            'ACM_COM_2B',
            'ACM_RT__2B',
            # ATLID-CPR-MSI-BBR
            'ALL_DF__2B',
            'ALL_3D__2B',
            # Orbit data    #@ Orbit files in Auxiliary data collection 
            'MPL_ORBSCT',   #@ orbit scenario file 
            'AUX_ORBPRE',   #@ predicted orbit file
            'AUX_ORBRES',   #@ restituted/reconstructed orbit file
        ]

        short_names = []

        for file_type in file_types:
            long_name = file_type.replace('_', '').lower()
            medium_name = long_name[0:-2]
            short_name = medium_name
            string_replacements = [('atl', 'a'), ('msi', 'm'), ('bbr', 'b'), ('cpr', 'c'), ('aux', 'x')]
            for old_string, new_string in string_replacements:
                short_name = short_name.replace(old_string, new_string)
            
            expected_inputs = [long_name, medium_name, short_name]

            if 'ALL_' == file_type[0:4]:
                alternative_long_name = 'acmb' + long_name[3:]
                alternative_short_name = 'acmb' + short_name[3:]
                expected_inputs.extend([alternative_long_name, alternative_short_name])
            
            if product_name_input in expected_inputs:
                return file_type
            
            short_names.append(short_name.upper())

        msg = ''
        msg2 = ''
        for i in range(len(file_types)):
            if i % 6 == 0:
                msg += '\n' + file_types[i]
                msg2 += '\n' + short_names[i]
            else:
                msg += '\t' + file_types[i]
                msg2 += '\t' + short_names[i]

        raise ValueError(f'The user input "{input_string}" is either not a valid product name or not supported by this function.\n' + msg + '\n\nor use the respective short forms (additional non letter characters like - or _ are also allowed, e.g. A-NOM):\n' + msg2)

    def load_dataframe(self, response):
        """Load response into a pandas DataFrame."""
        # Creating a dataframe with the following columns
        df = pd.DataFrame(columns=['dc:identifier', 
                                   'atom:title', 
                                   'atom:updated', 
                                   'atom:link[rel="search"]', 
                                   'atom:link[rel="enclosure"]', 
                                   'atom:link[rel="icon"]'])

        # from an OpenSearch query the following information is gathered.
        rt = ElementTree.fromstring(response.text)
        for r in rt.findall('{http://www.w3.org/2005/Atom}entry'):
            name = r.find('{http://purl.org/dc/elements/1.1/}identifier').text
            title = r.find('{http://www.w3.org/2005/Atom}title').text
            updated = r.find('{http://www.w3.org/2005/Atom}updated').text
            dcdate = r.find('{http://purl.org/dc/elements/1.1/}date').text

            try:
                href = r.find('{http://www.w3.org/2005/Atom}link[@rel="search"][@type="application/opensearchdescription+xml"]').attrib['href']
            except AttributeError:
                href= ''

            try:
                rel_enclosure = r.find('{http://www.w3.org/2005/Atom}link[@rel="enclosure"]').attrib['href']
            except AttributeError:
                rel_enclosure= ''

            try:
                rel_icon = r.find('{http://www.w3.org/2005/Atom}link[@rel="icon"]').attrib['href']
            except AttributeError:
                rel_icon= ''

            # append a row to the df 
            new_row = {'dc:identifier': name,
                       'atom:title': title,
                       'dc:date': dcdate,
                       'atom:updated': updated,
                       'atom:link[rel="search"]': href,
                       'atom:link[rel="enclosure"]': rel_enclosure,
                       'server': urlparse(rel_enclosure).netloc,
                       'atom:link[rel="icon"]': rel_icon}

            dfn = pd.DataFrame(new_row, index = [0])
            df = pd.concat([df, dfn], ignore_index=True)

        return df

    def get_api_request(self, template, os_querystring):
        """Fill URL template with OpenSearch parameter values."""
        OS_NAMESPACE = 'os:'

        # perform substitutions in template
        for p in os_querystring:
            result = re.subn(r'\{'+p+r'.*?\}', os_querystring[p] , template)
            n = result[1]
            template = result[0]
            if (n<1):
                if (':' in p):
                    print("ERROR: parameter " + p + " not found in template.")
                else:
                    # try with explicit namespace
                    result = re.subn(r'\{'+OS_NAMESPACE+p+r'.*?\}', os_querystring[p] , template)
                    n = result[1]
                    template = result[0]
                    if (n<1):
                        print("ERROR: parameter " + OS_NAMESPACE+p + " not found in template.")   

        # remove empty search parameters
        template = re.sub(r'&?[a-zA-Z]*=\{.*?\}', '' , template)
        template = re.sub(r'.?\{.*?\}', '' , template)
        template = template.replace('[','{')
        template = template.replace(']','}')

        self._log(f"API request: {template}")
        return template

    def download_products(self, dataframe, download_directory, is_override=False, progress_bar=None):
        """Download products from the dataframe."""
        downloaded_files = []
        skipped_files = []
        failed_files = []
        
        for server, df_group in dataframe.groupby('server'):
            # Product Download
            proxies = {}
            oads_hostname = server
            self._log(f"Connecting to dissemination service: {oads_hostname}")
            eoiam_idp_hostname = "eoiam-idp.eo.esa.int"

            # OADS Login Request
            response = requests.get(f"https://{oads_hostname}/oads/access/login", 
                                    proxies = proxies)

            # extracting the cookies from the response
            cookies = response.cookies
            for r in response.history:
                cookies = requests.cookies.merge_cookies(cookies, r.cookies)
            tree = html.fromstring(response.content)

            # extracting the sessionDataKey from the response 
            sessionDataKey = tree.findall(".//input[@name = 'sessionDataKey']")[0].attrib["value"]

            # Authentication Login Request
            post_data = {
                "tocommonauth": "true",
                "username": self.username,
                "password": self.password,
                "sessionDataKey": sessionDataKey
            }

            response = requests.post(url = f"https://{eoiam_idp_hostname}/samlsso",
                                    data = post_data, 
                                    cookies = cookies, 
                                    proxies = proxies)

            # parsing the response from Authentication platform
            tree = html.fromstring(response.content)
            responseView = BeautifulSoup(response.text, 'html.parser')

            # extracting the variables needed to redirect from a successful authentication to OADS
            relayState = tree.findall(".//input[@name='RelayState']")[0].attrib["value"]
            samlResponse = tree.findall(".//input[@name='SAMLResponse']")[0].attrib["value"]
            saml_redirect_url = tree.findall(".//form[@method='post']")[0].attrib["action"]

            # Redirecting to OADS
            post_data = {
                "RelayState": relayState,
                "SAMLResponse": samlResponse
            }

            response = requests.post(url = saml_redirect_url,
                                    data = post_data,
                                    proxies = proxies)

            cookies2 = response.cookies
            for r in response.history:
                cookies2 = requests.cookies.merge_cookies(cookies2, r.cookies)

            # Downloading Products
            max_retries = 3

            for index, row in df_group.iterrows():
                # extracting the filename from the download link
                file_name = (row['atom:link[rel="enclosure"]']).split("/")[-1]
                file_path = os.path.join(download_directory, file_name)
                file_path_no_ext = file_path[0:-4] if file_path.endswith('.zip') else file_path
                
                # Enhanced file existence check
                file_exists = any([
                    os.path.exists(file_path),
                    os.path.exists(file_path_no_ext),
                    os.path.exists(file_path + '.zip'),
                    any(os.path.exists(os.path.join(download_directory, f)) 
                        for f in os.listdir(download_directory) 
                        if f.startswith(file_name.split('.')[0]))
                ])
                
                if file_exists:
                    if is_override:
                        # Remove all versions of the file
                        for existing_file in [file_path, file_path_no_ext, file_path + '.zip']:
                            if os.path.exists(existing_file):
                                os.remove(existing_file)
                                self._log(f"Removed existing file: {existing_file}")
                    else:
                        self._log(f"Skipping {file_name} - already exists")
                        skipped_files.append(file_name)
                        if progress_bar:
                            progress_bar.update(1)
                        continue

                # defining the download url
                url = row['atom:link[rel="enclosure"]']
                download_success = False

                for attempt in range(max_retries):
                    try:
                        self._log(f"Downloading {file_name} (attempt {attempt + 1})")
                        response = requests.get(url, 
                                                cookies = cookies2, 
                                                proxies = proxies, 
                                                stream = True)
                        response.raise_for_status()
                        
                        # Get file size for progress tracking
                        total_size = int(response.headers.get('content-length', 0))
                        
                        # downloading the product with progress tracking
                        with open(file_path, "wb") as fd:
                            if total_size > 0 and not self.verbose:
                                with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name, leave=False) as pbar:
                                    for chunk in response.iter_content(chunk_size = 8192):
                                        fd.write(chunk)
                                        pbar.update(len(chunk))
                            else:
                                for chunk in response.iter_content(chunk_size = 8192):
                                    fd.write(chunk)
                                
                        self._log(f"Successfully downloaded: {file_name}")
                        downloaded_files.append(file_name)
                        download_success = True
                        break
                    except requests.exceptions.RequestException as e:
                        self._log(f"Failed to download {file_name} (attempt {attempt + 1}/{max_retries}): {e}", 'warning')
                        time.sleep(2)
                
                if not download_success:
                    self._log(f"Failed to download {file_name} after {max_retries} attempts", 'error')
                    failed_files.append(file_name)
                
                if progress_bar:
                    progress_bar.update(1)

            # logout
            try:
                logout_1 = requests.get(f'https://{oads_hostname}/oads/Shibboleth.sso/Logout', 
                                        proxies = proxies, 
                                        stream = True)
                logout_2 = requests.get(f'https://{eoiam_idp_hostname}/Shibboleth.sso/Logout', 
                                        proxies = proxies, 
                                        stream = True)
                self._log("Successfully logged out")
            except:
                self._log("Warning: Could not logout properly", 'warning')
        
        return {
            'downloaded': downloaded_files,
            'skipped': skipped_files,
            'failed': failed_files
        }

    def get_product_search_template(self):
        """Get the product search template for the specified collection."""
        url_osdd = 'https://eocat.esa.int/eo-catalogue/opensearch/description.xml'

        response = requests.get(url_osdd)
        root = ElementTree.fromstring(response.text)
        ns = {'os': 'http://a9.com/-/spec/opensearch/1.1/'}
        collection_url_atom = root.find('os:Url[@rel="collection"][@type="application/atom+xml"]', ns)

        collection_template = collection_url_atom.attrib['template']
        self._log(f'Selected collection: {self.collection}')

        osquerystring = {}
        osquerystring['geo:uid'] = str(self.collection)

        request_url = self.get_api_request(collection_template, osquerystring)
        response = requests.get(request_url)

        root = ElementTree.fromstring(response.text)
        el = root.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults')

        dataframe = self.load_dataframe(response)
        url_osdd_granules = dataframe.iat[0,3]

        response = requests.get(url_osdd_granules, headers={'Accept': 'application/opensearchdescription+xml'})
        root = ElementTree.fromstring(response.text)

        granules_url_atom = root.find('{http://a9.com/-/spec/opensearch/1.1/}Url[@rel="results"][@type="application/atom+xml"]')
        template = granules_url_atom.attrib['template']
        
        return template

    def get_product_list(self, template, **kwargs):
        """Get product list based on search parameters."""
        osquerystring = {}

        # Map all possible search parameters
        param_mapping = {
            'product_id_text': 'geo:uid',
            'sort_by_text': 'sru:sortKeys',
            'num_results_text': 'count',
            'start_time_text': 'time:start',
            'end_time_text': 'time:end',
            'poi_text': 'geo:geometry',
            'bbox_text': 'geo:box',
            'illum_angle_text': 'eo:illuminationElevationAngle',
            'frame_text': 'eo:frame',
            'orbit_number_text': 'eo:orbitNumber',
            'instrument_text': 'eo:instrument',
            'productType_text': 'eo:productType',
            'orbitDirection_text': 'eo:orbitDirection',
            'radius_text': 'geo:radius',
            'lat_text': 'geo:lat',
            'lon_text': 'geo:lon'
        }

        # Add parameters that are provided
        for param_name, opensearch_param in param_mapping.items():
            if param_name in kwargs and kwargs[param_name] is not None:
                osquerystring[opensearch_param] = kwargs[param_name]

        # make the product request to the catalogue
        request_url = self.get_api_request(template, osquerystring)
        response = requests.get(request_url)

        root = ElementTree.fromstring(response.text)
        el = root.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults')

        if el is not None:
            self._log(f'Total results: {el.text}')
        else:
            self._log('No results found for search parameters')
            self._log('Tip: try widening your search parameters')

        dataframe = self.load_dataframe(response)
        return dataframe

    def filter_by_baseline(self, dataframe):
        """Filter dataframe to only include products from a specific baseline."""
        if dataframe.empty:
            return dataframe, None
        
        dataframe = dataframe.copy()
        dataframe['baseline'] = dataframe['dc:identifier'].str.extract(r'ECA_EX([A-Z]{2})_')[0]
        
        if self.baseline is None:
            # Select the most common baseline if not specified
            baseline_counts = dataframe['baseline'].value_counts()
            if baseline_counts.empty:
                self._log("Warning: No valid baselines found in the data", 'warning')
                return pd.DataFrame(), None
            
            selected_baseline = baseline_counts.index[0]
            self._log(f"Auto-selected baseline: {selected_baseline} ({baseline_counts.iloc[0]} products)")
        else:
            selected_baseline = self.baseline
        
        # Filter by specified baseline
        filtered_df = dataframe[dataframe['baseline'] == selected_baseline].copy()
        
        if filtered_df.empty:
            available_baselines = dataframe['baseline'].unique()
            self._log(f"Warning: No products found for baseline '{selected_baseline}'", 'warning')
            self._log(f"Available baselines: {list(available_baselines)}")
            return pd.DataFrame(), None
        
        self._log(f"Filtered to {len(filtered_df)} products from baseline '{selected_baseline}'")
        return filtered_df.drop('baseline', axis=1), selected_baseline

    def download_from_csv(self, csv_file_path, products, download_directory, orbit_column=None, 
                         override=False, radius_search=None, bounding_box=None):
        """
        Download EarthCARE products based on a CSV file with dates and times.
        
        Parameters:
        - csv_file_path: str, path to CSV file with datetime columns
        - products: list, list of product names to download
        - download_directory: str, directory where files will be downloaded
        - orbit_column: str, optional column name containing orbit numbers
        - override: bool, whether to override existing files
        - radius_search: tuple, optional (radius_m, latitude, longitude) for spatial search
        - bounding_box: tuple, optional (latS, lonW, latN, lonE) for bounding box search
        
        Returns:
        - dict with execution summary
        """
        start_time = datetime.now()
        
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
        
        try:
            # Auto-detect CSV separator
            separator = self._detect_csv_separator(csv_file_path)
            self._log(f"Detected CSV separator: '{separator}'")
            
            # Load CSV file with detected separator
            df = pd.read_csv(csv_file_path, sep=separator)
            
            # Auto-detect datetime columns
            date_col, time_col = self._find_datetime_columns(df)
            
            if not date_col or not time_col:
                available_cols = list(df.columns)
                error_msg = f"Could not automatically detect date/time columns. Available columns: {available_cols}"
                self._log(error_msg, 'error')
                summary['errors'].append(error_msg)
                return summary
            
            self._log(f"Using date column: '{date_col}', time column: '{time_col}'")
            
            # Create download directory if it doesn't exist
            os.makedirs(download_directory, exist_ok=True)
            
            # Convert products to valid product names
            if isinstance(products, str):
                products = [products]
            product_names = [self.string_to_product_name(prod) for prod in products]
            
            # Get product search template
            template = self.get_product_search_template()
            
            summary['total_entries'] = len(df)
            
            # Progress bar setup
            if not self.verbose:
                print(f"Processing {len(df)} entries...")
                pbar = tqdm(total=len(df), desc="Processing entries", unit="entry")
            else:
                pbar = None
            
            try:
                for index, row in df.iterrows():
                    try:
                        date_str = str(row[date_col])
                        time_str = str(row[time_col])
                        
                        # Handle time string formatting
                        if '.' in time_str:
                            time_parts = time_str.split('.')
                            if len(time_parts[1]) > 3:
                                time_str = time_parts[0] + '.' + time_parts[1][:3]
                        
                        datetime_str = f"{date_str} {time_str}"
                        
                        self._log(f"Processing entry {index + 1}/{len(df)}: {datetime_str}")
                        
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
                        
                        # Add spatial search parameters
                        if radius_search:
                            search_params.update({
                                'radius_text': str(int(radius_search[0])),
                                'lat_text': str(float(radius_search[1])),
                                'lon_text': str(float(radius_search[2]))
                            })
                        
                        if bounding_box:
                            search_params['bbox_text'] = ','.join([str(float(x)) for x in bounding_box])
                        
                        # Search for products
                        dataframe = self.get_product_list(template, **search_params)
                        
                        # Apply baseline filtering
                        dataframe, selected_baseline = self.filter_by_baseline(dataframe)
                        
                        if dataframe.empty:
                            self._log(f"No products found for {datetime_str}")
                            if pbar:
                                pbar.update(1)
                            continue
                        
                        self._log(f"Found {len(dataframe)} products for {datetime_str} (baseline: {selected_baseline})")
                        
                        # Download products
                        download_result = self.download_products(dataframe, download_directory, override, pbar)
                        
                        # Update summary
                        summary['downloaded_files'].extend(download_result['downloaded'])
                        summary['skipped_files'].extend(download_result['skipped'])
                        summary['failed_files'].extend(download_result['failed'])
                        
                        summary['processed_entries'] += 1
                        
                    except Exception as e:
                        error_msg = f"Error processing entry {index + 1} ({datetime_str}): {str(e)}"
                        self._log(error_msg, 'error')
                        summary['errors'].append({
                            'entry': index + 1,
                            'datetime': datetime_str,
                            'error': str(e),
                            'orbit': row.get(orbit_column, 'N/A') if orbit_column and orbit_column in df.columns else 'N/A'
                        })
                        
                        if pbar:
                            pbar.update(1)
                
            finally:
                if pbar:
                    pbar.close()
            
        except Exception as e:
            error_msg = f"Critical error during execution: {str(e)}"
            self._log(error_msg, 'error')
            summary['errors'].append(error_msg)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = end_time - start_time
        summary['execution_time'] = str(execution_time)
        summary['end_time'] = end_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Save execution summary
        self._save_execution_summary(summary, download_directory)
        
        # Print final summary
        if not self.verbose:
            self._print_final_summary(summary)
        
        return summary
    
    def _save_execution_summary(self, summary, download_directory):
        """Save execution summary and logs to files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save summary
        summary_file = os.path.join(download_directory, f'download_summary_{timestamp}.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("EarthCARE Download Execution Summary\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Start time: {summary['start_time']}\n")
            f.write(f"End time: {summary['end_time']}\n")
            f.write(f"Execution time: {summary['execution_time']}\n\n")
            
            f.write(f"Total entries: {summary['total_entries']}\n")
            f.write(f"Processed entries: {summary['processed_entries']}\n")
            f.write(f"Downloaded files: {len(summary['downloaded_files'])}\n")
            f.write(f"Skipped files: {len(summary['skipped_files'])}\n")
            f.write(f"Failed files: {len(summary['failed_files'])}\n")
            f.write(f"Errors: {len(summary['errors'])}\n\n")
            
            if summary['downloaded_files']:
                f.write("Downloaded files:\n")
                for file in summary['downloaded_files']:
                    f.write(f"  - {file}\n")
                f.write("\n")
            
            if summary['skipped_files']:
                f.write("Skipped files (already exist):\n")
                for file in summary['skipped_files']:
                    f.write(f"  - {file}\n")
                f.write("\n")
            
            if summary['failed_files']:
                f.write("Failed downloads:\n")
                for file in summary['failed_files']:
                    f.write(f"  - {file}\n")
                f.write("\n")
            
            if summary['errors']:
                f.write("Errors encountered:\n")
                for error in summary['errors']:
                    if isinstance(error, dict):
                        f.write(f"  Entry {error['entry']} ({error['datetime']}): {error['error']}\n")
                    else:
                        f.write(f"  {error}\n")
        
        # Save detailed execution log
        log_file = os.path.join(download_directory, f'download_log_{timestamp}.txt')
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("EarthCARE Download Detailed Log\n")
            f.write("=" * 50 + "\n\n")
            for log_entry in self.execution_log:
                f.write(log_entry + "\n")
        
        # Save errors as CSV if any
        if summary['errors']:
            error_file = os.path.join(download_directory, f'download_errors_{timestamp}.csv')
            error_data = []
            for error in summary['errors']:
                if isinstance(error, dict):
                    error_data.append(error)
                else:
                    error_data.append({'entry': 'N/A', 'datetime': 'N/A', 'error': error, 'orbit': 'N/A'})
            
            if error_data:
                pd.DataFrame(error_data).to_csv(error_file, index=False)
        
        self._log(f"Execution summary saved to: {summary_file}")
        self._log(f"Detailed log saved to: {log_file}")
    
    def _print_final_summary(self, summary):
        """Print final execution summary to console."""
        print("\n" + "=" * 60)
        print("           EarthCARE Download Summary")
        print("=" * 60)
        print(f"Execution time: {summary['execution_time']}")
        print(f"Total entries processed: {summary['processed_entries']}/{summary['total_entries']}")
        print(f"Files downloaded: {len(summary['downloaded_files'])}")
        print(f"Files skipped (already exist): {len(summary['skipped_files'])}")
        print(f"Files failed: {len(summary['failed_files'])}")
        print(f"Errors encountered: {len(summary['errors'])}")
        
        if summary['downloaded_files']:
            print(f"\n✅ Successfully downloaded {len(summary['downloaded_files'])} files")
        
        if summary['skipped_files']:
            print(f"⏭️  Skipped {len(summary['skipped_files'])} files (already exist)")
        
        if summary['failed_files']:
            print(f"❌ Failed to download {len(summary['failed_files'])} files")
        
        if summary['errors']:
            print(f"⚠️  {len(summary['errors'])} errors encountered")
            print("   Check the error log file for details.")
        
        print("=" * 60)


# Example usage
if __name__ == "__main__":
    import getpass
    
    print("=== EarthCARE Data Downloader ===")
    print("Por favor, ingresa tus credenciales de OADS:")
    
    # Solicitar credenciales al usuario
    username = input("Usuario OADS: ")
    password = getpass.getpass("Contraseña OADS: ")  # getpass oculta la contraseña al escribir
    
    if not username or not password:
        print("Error: Usuario y contraseña son requeridos.")
        exit(1)
    
    print(f"Conectando como: {username}")
    
    # Example of how to use the class
    downloader = EarthCareDownloader(
        username=username,
        password=password, 
        collection='EarthCAREL2InstChecked',
        baseline='BA',
        verbose=False  # Set to True for detailed output
    )
    
    # Download products based on CSV file
    csv_file = r"C:\Users\usuario\Downloads\test_earthcare.csv"  # CSV with datetime columns (auto-detected)
    products = ['AALD']  # List of products to download
    download_dir = r"D:\EarthCARE\ESA_files\prueba" + "/" + products[0]
    
    print(f"Archivo CSV: {csv_file}")
    print(f"Productos a descargar: {products}")
    print(f"Directorio de descarga: {download_dir}")
    print("\nIniciando descarga...")
    
    # Run the download
    try:
        summary = downloader.download_from_csv(
            csv_file_path=csv_file,
            products=products,
            download_directory=download_dir,
            override=False
        )
        print("\n¡Descarga completada exitosamente!")
    except Exception as e:
        print(f"\nError durante la descarga: {e}")