# 🌍 EarthCARE Data Downloader - Versión Web (Streamlit)

Esta es la versión web de EarthCARE Data Downloader, diseñada para facilitar descargas de datos desde cualquier dispositivo sin necesidad de instalar software.

## 🚀 Despliegue Rápido en Streamlit Cloud

### Opción 1: Despliegue Automático (Recomendado)

La forma más fácil es usar **Streamlit Cloud** (totalmente GRATIS):

1. **Requisitos previos:**
   - Cuenta GitHub con el repositorio (`earthcare-data-downloader`)
   - Cuenta Streamlit (gratis en https://share.streamlit.io)

2. **Pasos:**
   - Ve a https://share.streamlit.io
   - Haz clic en "Crear una app"
   - Selecciona tu repositorio GitHub: `earthcare-data-downloader`
   - Rama: `main`
   - Archivo principal: `app_streamlit.py`
   - Haz clic en "Deploy"

3. **Espera 2-3 minutos** y ¡listo! Tu app estará en vivo:
   ```
   https://earthcare-downloader-tuperfil.streamlit.app
   ```

### Opción 2: Ejecución Local

Si prefieres ejecutar la app localmente:

```bash
# 1. Clona el repositorio
git clone https://github.com/onrona/earthcare-data-downloader.git
cd earthcare-data-downloader

# 2. Instala las dependencias
pip install -r requirements_streamlit.txt

# 3. Ejecuta la app
streamlit run app_streamlit.py
```

La app se abrirá en `http://localhost:8501`

## 📋 Requisitos

### Para usar la app web:
- Credenciales OADS ([Regístrate aquí](https://eocat.esa.int/))
- Archivo CSV con fechas y horas
- Conexión a internet

### Para desplegar en Streamlit Cloud:
- Repositorio GitHub actualizado
- Cuenta Streamlit (gratis)
- Archivo `requirements_streamlit.txt` en el repositorio

## 💻 Características de la Versión Web

✅ **Sin instalaciones** - Funciona desde el navegador  
✅ **Interfaz intuitiva** - Fácil de usar para todos  
✅ **Respuesta en tiempo real** - Ve el progreso mientras se descarga  
✅ **Descarga en ZIP** - Todos los archivos comprimidos  
✅ **Multi-dispositivo** - Acceso desde móvil, tablet, pc  
✅ **Compartible** - Solo envía un URL a colaboradores  
✅ **Extra seguro** - Credenciales no se almacenan  

## 🔐 Seguridad

- Las credenciales **solo se envían a OADS** para autenticación
- **No se almacenan** en el servidor de Streamlit
- Cada sesión es **independiente y anónima**
- Los datos se procesan en **directorios temporales**

## 📝 Uso

### Paso 1: Credenciales
Introduce tu usuario y contraseña de OADS en la barra lateral

### Paso 2: Cargar CSV
Sube tu archivo CSV con columnas de fecha y hora. El sistema detectará automáticamente:
- El separador (coma, punto y coma, tabulación)
- La columna de fecha
- La columna de hora

**Ejemplo de CSV válido:**
```csv
fecha,hora
2024-01-15,12:30:45.123
2024-01-16,14:15:30.456
```

### Paso 3: Configurar Descarga
1. Selecciona la colección (L1, L2, etc.)
2. Elige la categoría de producto
3. Selecciona el producto específico
4. Elige el baseline (o Auto-detect)

### Paso 4: Descargar
- Haz clic en "🚀 Iniciar Descarga"
- Espera el procesamiento
- Descarga los archivos en ZIP

## ⚙️ Opciones Avanzadas

- **Columna de Órbita**: Si tu CSV tiene números de órbita
- **Sobrescribir archivos**: Para forzar la descarga aunque existan
- **Modo detallado**: Para información más específica del proceso

## 🐛 Solución de Problemas

### "Error de autenticación"
- Verifica que tu usuario y contraseña OADS sean correctos
- Asegúrate de tener acceso a la colección seleccionada

### "No se encontraron productos"
- Verifica el formato de fecha/hora en tu CSV
- Intenta con diferentes tipos de productos
- Asegúrate de que el baseline es compatible

### "Error al leer el CSV"
- Verifica que el archivo sea válido
- Comprueba que tenga columnas de fecha y hora
- Intenta abrir en Excel para verificar el contenido

### "Descarga lenta"
- Depende del tamaño de los archivos
- Verifica tu conexión a internet
- Es normal que tarde minutos u horas según los datos

## 📚 Colecciones Disponibles

- **EarthCARE L1 Products** - Productos nivel 1 calibrados
- **EarthCARE L2 Products** - Productos nivel 2 procesados
- **EarthCARE Auxiliary Data** - Datos auxiliares
- **EarthCARE Orbit Data** - Información de órbita
- **JAXA L2 Products** - Productos JAXA nivel 2

## 🔗 Enlaces Útiles

- [OADS Portal](https://eocat.esa.int/)
- [Documentación EarthCARE](https://www.esa.int/Applications/Observing_the_Earth/EarthCARE)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Repository](https://github.com/onrona/earthcare-data-downloader)

## 📦 Versión de Desktop

Si prefieres la interfaz gráfica de escritorio, usa:
```bash
python earthcare_downloader_gui.py
```

## 📧 Soporte

Para problemas, preguntas o sugerencias, por favor abre un issue en GitHub.

---

**Hecho con ❤️ para facilitar el acceso a datos EarthCARE**
