#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: app_streamlit.py
Author: Onrona Functions
Created: 2025-11-20
Version: 1.0
Description:
    Streamlit web application for EarthCARE Data Downloader.
    Allows users to download EarthCARE products through a modern web interface.
"""

import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime
from pathlib import Path
import tempfile
import shutil

# Import the downloader class
from earthcare_downloader import EarthCareDownloader
from aux_data import aux_dict_L1, aux_dict_L2

# Page configuration
st.set_page_config(
    page_title="EarthCARE Data Downloader",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1em;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("# 🌍 EarthCARE Data Downloader")
st.markdown("""
Descarga productos de datos EarthCARE desde OADS de forma fácil y rápida.
""")

# ============================================================================
# SIDEBAR - CREDENTIALS AND CONFIGURATION
# ============================================================================
st.sidebar.markdown("## 🔐 Credenciales OADS")

username = st.sidebar.text_input(
    "Usuario OADS:",
    placeholder="Tu usuario de OADS",
    key="username"
)

password = st.sidebar.text_input(
    "Contraseña OADS:",
    type="password",
    placeholder="Tu contraseña de OADS",
    key="password"
)

# Collections
collections = {
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
product_categories = {
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

# Baselines
baselines = ['Auto-detect', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH', 'AI', 'AJ',
            'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ']

# Combine baseline dictionaries
all_baselines = {**aux_dict_L1, **aux_dict_L2}

st.sidebar.markdown("---")
st.sidebar.markdown("## ⚙️ Configuración")

collection_name = st.sidebar.selectbox(
    "Colección:",
    list(collections.keys()),
    index=0,
    key="collection_select"
)
collection_id = collections[collection_name]

# ============================================================================
# MAIN CONTENT - TABS
# ============================================================================
tab1, tab2, tab3 = st.tabs(["📥 Descargar", "ℹ️ Información", "📊 Ayuda"])

with tab1:
    # Create two columns for file upload
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Archivo CSV")
        uploaded_file = st.file_uploader(
            "Selecciona tu archivo CSV con fechas y horas",
            type=['csv'],
            help="El archivo debe contener columnas con fecha y hora. Se detectarán automáticamente."
        )
        
        # Show preview if file is uploaded
        if uploaded_file is not None:
            try:
                df_preview = pd.read_csv(uploaded_file, nrows=5)
                st.info(f"✅ Archivo cargado: **{uploaded_file.name}**")
                st.markdown("**Vista previa (primeras 5 filas):**")
                st.dataframe(df_preview, use_container_width=True)
                
                # Get all column names for orbit selection
                csv_columns = df_preview.columns.tolist()
            except Exception as e:
                st.error(f"❌ Error al leer el archivo: {e}")
                csv_columns = []
    
    with col2:
        st.markdown("### 📦 Selección de Producto")
        
        category = st.selectbox(
            "Categoría de Producto:",
            list(product_categories.keys()),
            key="category_select"
        )
        
        products_in_category = product_categories.get(category, [])
        selected_product = st.selectbox(
            "Producto:",
            products_in_category,
            key="product_select"
        )
        
        # Get available baselines for this product
        available_baselines = ['Auto-detect']
        if selected_product in all_baselines:
            available_baselines.extend(all_baselines[selected_product])
        
        baseline = st.selectbox(
            "Baseline:",
            available_baselines,
            key="baseline_select",
            help="Auto-detect seleccionará el baseline más común automáticamente"
        )
    
    # Advanced options
    with st.expander("⚙️ Opciones Avanzadas"):
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            if uploaded_file is not None and csv_columns:
                orbit_column = st.selectbox(
                    "Columna de Número de Órbita:",
                    ['Ninguno'] + csv_columns,
                    help="Selecciona si tu CSV tiene información de órbita"
                )
                if orbit_column == 'Ninguno':
                    orbit_column = None
            else:
                orbit_column = None
                st.info("Carga un archivo CSV para ver las columnas disponibles")
            
            override_files = st.checkbox(
                "Sobrescribir archivos existentes",
                value=False,
                help="Si está activado, descargará los archivos nuevamente incluso si ya existen"
            )
        
        with col_adv2:
            verbose_mode = st.checkbox(
                "Modo detallado",
                value=False,
                help="Muestra información detallada del proceso"
            )
            
            st.markdown("**Información de descargas:**")
            st.info(f"""
            📥 Los archivos se descargarán en una carpeta temporal.
            Podrás descargarlos como ZIP después de completar.
            """)
    
    # Validation and download button
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns([3, 1])
    
    with col_btn1:
        if st.button("🚀 Iniciar Descarga", type="primary", use_container_width=True):
            # Validate inputs
            errors = []
            
            if not username.strip():
                errors.append("❌ Usuario OADS requerido")
            if not password.strip():
                errors.append("❌ Contraseña OADS requerida")
            if uploaded_file is None:
                errors.append("❌ Archivo CSV requerido")
            
            if errors:
                st.error("\n".join(errors))
            else:
                # Create a placeholder for logs
                log_container = st.container(border=True)
                status_placeholder = log_container.status("Inicializando descarga...", expanded=True)
                log_placeholder = status_placeholder.empty()
                
                logs = []
                
                try:
                    with status_placeholder:
                        # Save uploaded file to temporary location
                        with tempfile.TemporaryDirectory() as temp_dir:
                            # Save CSV temp file
                            csv_temp_path = os.path.join(temp_dir, uploaded_file.name)
                            with open(csv_temp_path, 'wb') as f:
                                f.write(uploaded_file.getbuffer())
                            
                            logs.append(f"📄 Archivo CSV guardado")
                            
                            # Create download directory
                            download_dir = os.path.join(temp_dir, 'downloads')
                            os.makedirs(download_dir, exist_ok=True)
                            
                            logs.append(f"📁 Directorio de descarga preparado")
                            
                            # Create downloader instance
                            logs.append(f"🔐 Conectando como: {username}")
                            
                            baseline_filter = baseline if baseline != 'Auto-detect' else None
                            
                            downloader = EarthCareDownloader(
                                username=username.strip(),
                                password=password.strip(),
                                collection=collection_id,
                                baseline=baseline_filter,
                                verbose=verbose_mode
                            )
                            
                            logs.append(f"✅ Descargador inicializado")
                            logs.append(f"📦 Producto: {selected_product}")
                            logs.append(f"🎯 Baseline: {baseline}")
                            logs.append(f"🚀 Iniciando descarga de {uploaded_file.name}...")
                            
                            # Update log display
                            with log_placeholder.container():
                                for log in logs:
                                    st.write(log)
                            
                            # Run download
                            summary = downloader.download_from_csv(
                                csv_file_path=csv_temp_path,
                                products=[selected_product],
                                download_directory=download_dir,
                                orbit_column=orbit_column,
                                override=override_files
                            )
                            
                            logs.append(f"🎉 Descarga completada!")
                            logs.append(f"---")
                            logs.append(f"📊 **Resumen:**")
                            logs.append(f"  • Entradas procesadas: {summary['processed_entries']}/{summary['total_entries']}")
                            logs.append(f"  • Archivos descargados: {len(summary['downloaded_files'])}")
                            logs.append(f"  • Archivos omitidos: {len(summary['skipped_files'])}")
                            logs.append(f"  • Archivos fallidos: {len(summary['failed_files'])}")
                            logs.append(f"  • Tiempo total: {summary['execution_time']}")
                            
                            # Update log display
                            with log_placeholder.container():
                                for log in logs:
                                    st.write(log)
                            
                            status_placeholder.update(label="✅ Descarga completada", state="complete")
                            
                            # Show download button if files were downloaded
                            if os.listdir(download_dir):
                                st.markdown("---")
                                
                                # Create ZIP file
                                zip_path = os.path.join(temp_dir, 'earthcare_downloads.zip')
                                shutil.make_archive(
                                    zip_path.replace('.zip', ''),
                                    'zip',
                                    download_dir
                                )
                                
                                with open(zip_path, 'rb') as f:
                                    st.download_button(
                                        label="📥 Descargar archivos (ZIP)",
                                        data=f.read(),
                                        file_name=f"earthcare_downloads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                                        mime="application/zip",
                                        use_container_width=True
                                    )
                                
                                # Show summary table
                                st.markdown("### 📋 Resumen Detallado")
                                
                                summary_data = {
                                    'Métrica': ['Entradas procesadas', 'Archivos descargados', 'Archivos omitidos', 'Archivos fallidos', 'Tiempo total'],
                                    'Valor': [
                                        f"{summary['processed_entries']}/{summary['total_entries']}",
                                        len(summary['downloaded_files']),
                                        len(summary['skipped_files']),
                                        len(summary['failed_files']),
                                        summary['execution_time']
                                    ]
                                }
                                st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
                            else:
                                st.warning("⚠️ No se descargaron archivos. Verifica los parámetros de búsqueda.")
                
                except Exception as e:
                    status_placeholder.update(label="❌ Error en descarga", state="error")
                    logs.append(f"❌ Error: {str(e)}")
                    
                    with log_placeholder.container():
                        for log in logs:
                            st.write(log)
                    
                    st.error(f"**Error durante la descarga:**\n\n{str(e)}")

with tab2:
    st.markdown("""
    ### 📋 Información General
    
    **EarthCARE Data Downloader** te permite descargar productos de datos de EarthCARE
    desde el catálogo OADS (ESA Open Access Data Service) de forma fácil y automática.
    
    ### 🎯 Características
    
    - ✅ **Descarga automática** desde OADS
    - 🔄 **Detección automática** de ficheros CSV (separador, fecha, hora)
    - 📦 **Múltiples colecciones** disponibles
    - 🎯 **Filtrado por baseline**
    - ♻️ **Opción de sobrescribir** archivos existentes
    - 📥 **Descarga en ZIP** de todos los archivos
    
    ### 📚 Guía de uso
    
    1. **Credenciales**: Ingresa tu usuario y contraseña OADS
    2. **Archivo CSV**: Carga tu archivo con fechas y horas
    3. **Producto**: Selecciona la categoría y el producto específico
    4. **Inicio**: Haz clic en "Iniciar Descarga"
    5. **Resultados**: Descarga los archivos en ZIP
    
    ### ❓ Requisitos del archivo CSV
    
    Tu archivo CSV debe contener:
    - Una columna con **fechas** (formato: yyyy-mm-dd)
    - Una columna con **horas** (formato: hh:mm:ss.sss)
    
    El sistema detectará automáticamente estas columnas buscando:
    - Nombres como: "date", "fecha", "day", etc.
    - Nombres como: "time", "hora", "hh:mm:ss.sss", etc.
    
    Ejemplo de CSV válido:
    ```
    fecha,hora,extra
    2024-01-15,12:30:45.123,datos
    2024-01-16,14:15:30.456,datos
    ```
    
    ### 🔗 Enlaces útiles
    
    - [OADS Portal](https://eocat.esa.int/)
    - [EarthCARE Mission](https://www.esa.int/Applications/Observing_the_Earth/EarthCARE)
    - [Documentación EarthCARE](https://www.esa.int/Applications/Observing_the_Earth/EarthCARE)
    """)

with tab3:
    st.markdown("""
    ### ❓ Preguntas Frecuentes
    
    #### ¿Cuáles son los requisitos del archivo CSV?
    El archivo debe tener:
    - Una columna con fechas en formato YYYY-MM-DD
    - Una columna con horas en formato HH:MM:SS.SSS
    - Cualquier separador (coma, punto y coma, tabulación) se detecta automáticamente
    
    #### ¿Necesito instalar algo?
    No, todo funciona en el navegador. Solo necesitas:
    - Credenciales de OADS
    - Tu archivo CSV
    - Conexión a internet
    
    #### ¿Cuánto tiempo tarda una descarga?
    Depende de:
    - Número de entradas en tu CSV
    - Disponibilidad de productos
    - Tamaño de los archivos
    
    Típicamente entre minutos a horas.
    
    #### ¿Dónde puedo obtener credenciales OADS?
    Regístrate en [OADS](https://eocat.esa.int/) con tu cuenta ESA.
    
    #### ¿Qué hago si falla una descarga?
    - Verifica tus credenciales
    - Comprueba el formato de tu CSV
    - Intenta con un solo producto
    - Verifica tu conexión a internet
    
    #### ¿Puedo descargar múltiples productos?
    Por ahora se descarga uno a la vez. Si necesitas múltiples:
    - Ejecuta la app varias veces con diferentes productos
    - O usa la aplicación de escritorio
    
    #### ¿Qué pasa con mi contraseña?
    - Solo se envía a OADS para autenticación
    - No se almacena en el servidor
    - La sesión es anónima
    
    #### ¿Hay límite de descargas?
    Depende de tu cuenta OADS. Consulta sus términos de servicio.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.85em;'>
    <p>EarthCARE Data Downloader • Powered by <a href='https://streamlit.io/'>Streamlit</a></p>
    <p>Para problemas o sugerencias, contacta con el equipo de desarrollo.</p>
</div>
""", unsafe_allow_html=True)
