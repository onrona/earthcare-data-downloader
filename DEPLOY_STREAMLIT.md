# 📚 Guía Completa: Desplegar EarthCARE Web en Streamlit Cloud

## 🎯 Objetivo Final

Tu aplicación web disponible en: `https://earthcare-downloader-tu-usuario.streamlit.app`

## 📋 Pre-requisitos

- [ ] Cuenta GitHub (gratis en https://github.com)
- [ ] Cuenta Streamlit (gratis en https://share.streamlit.io)
- [ ] Repositorio con los archivos de la app

---

## ⚡ Despliegue Rápido (5 minutos)

### Paso 1: Preparar el repositorio

```bash
# 1. Asegúrate de estar en la rama main
git branch -a
git checkout main

# 2. Verifica que estos archivos existan:
ls -la app_streamlit.py
ls -la requirements_streamlit.txt
ls -la .streamlit/config.toml
ls -la earthcare_downloader.py
ls -la aux_data.py
```

### Paso 2: Hacer commit y push

```bash
# 1. Agrega todos los cambios
git add .

# 2. Haz commit
git commit -m "Add Streamlit web version of EarthCARE Downloader"

# 3. Push a GitHub
git push origin main
```

### Paso 3: Desplegar en Streamlit Cloud

1. **Ve a https://share.streamlit.io**
2. **Haz clic en "Create app"**
3. **Completa los datos:**
   - **GitHub repo**: `onrona/earthcare-data-downloader`
   - **Branch**: `main`
   - **File path**: `app_streamlit.py`
4. **Haz clic en "Deploy"**

✅ **¡Listo!** La app se desplegará en 2-3 minutos

---

## 🔧 Prueba Local

### Instalación de Streamlit

```bash
# Instala solo Streamlit
pip install streamlit

# O instala todas las dependencias
pip install -r requirements_streamlit.txt
```

### Ejecutar la app localmente

```bash
# En la carpeta del proyecto
streamlit run app_streamlit.py
```

**Resultado:**

- La app se abrirá en `http://localhost:8501`
- Puedes usar tu navegador para acceder

### Pruebas

1. Abre http://localhost:8501
2. Ingresa usuario/contraseña OADS (prueba)
3. Carga un archivo CSV de prueba
4. Selecciona producto
5. Haz clic en "Iniciar Descarga"

---

## 🐛 Solución de Problemas

### "Module not found" error

```bash
# Reinstala las dependencias
pip install --upgrade -r requirements_streamlit.txt
```

### App no arranca locally

```bash
# Borra cache de Streamlit
rm -rf ~/.streamlit/cache
streamlit run app_streamlit.py
```

### Error en Streamlit Cloud

1. Verifica que `requirements_streamlit.txt` tenga todas las dependencias
2. Comprueba que `app_streamlit.py` esté en la raíz del repo
3. Revisa los logs en Streamlit Cloud
4. Intenta redeplegar

---

## 📁 Estructura esperada del repo

```
earthcare-data-downloader/
├── app_streamlit.py              # 🌐 App web (NUEVO)
├── earthcare_downloader.py        # Core downloader
├── earthcare_downloader_gui.py    # GUI desktop
├── aux_data.py                   # Datos auxiliares
├── README.md                     # README principal
├── README_STREAMLIT.md          # 📚 Guía Streamlit (NUEVO)
├── requirements.txt              # Dependencias base
├── requirements_streamlit.txt   # 📦 Dependencias web (NUEVO)
├── requirements_gui.txt         # Dependencias GUI
├── .streamlit/                  # 📁 Config Streamlit (NUEVO)
│   └── config.toml              # Configuración
├── examples/
│   ├── basic_usage.py
│   ├── advanced_usage.py
│   └── gui_example.py
└── tests/
    ├── __init__.py
    └── test_downloader.py
```

---

## 🔐 Consideraciones de Seguridad

### Credenciales OADS

✅ **SEGURO PORQUE:**

- Solo se envían a OADS en cada solicitud
- No se almacenan en Streamlit Cloud
- Cada sesión es independiente
- No hay cookies persistentes

### Datos descargados

✅ **SEGURO PORQUE:**

- Se procesan en directorios temporales
- Se limpian automáticamente
- Los ZIP se generan bajo demanda
- No se almacenan en el servidor

---

## 📈 Monitoreo de tu app

En Streamlit Cloud:

1. Ve a tu dashboard
2. Selecciona tu app
3. Verás:
   - Últimas descargas
   - Errores recientes
   - Uso de recursos
   - Logs en tiempo real

---

## 🚀 Próximos Pasos

### Optimizaciones sugeridas:

1. **Cacheo de productos:**

   ```python
   @st.cache_data
   def get_available_products():
       # Cache de productos para faster load
   ```

2. **Histórico de descargas:**
   - Guarda resumen en base de datos
   - Permite comparación entre ejecuciones

3. **Autenticación GitHub:**
   - Login optional para salvar preferencias
   - Histórico personalizado

4. **Integración con Drive:**
   - Guardar descargas en Google Drive
   - Compartir directamente

### Compartir con colaboradores:

Simplemente envía esto:

``` Descarga datos EarthCARE aquí:
https://earthcare-downloader-tu-usuario.streamlit.app
```

¡Solo necesitan el enlace, sin instalaciones!

---

## 📞 Soporte

### Si algo no funciona:

1. **Verifica logs locales:**

   ```bash
   streamlit run app_streamlit.py --logger.level=debug
   ```

2. **Verifica logs en Cloud:**
   - Dashboard de Streamlit Cloud → App logs

3. **Abre un issue en GitHub:**
   - Incluye el error exacto
   - Versión de Python
   - Sistema operativo

---

## ✅ Checklist Final

- [ ] Archivos creados: `app_streamlit.py`, `requirements_streamlit.txt`, `.streamlit/config.toml`
- [ ] Cambios commiteados a `main`
- [ ] Push realizado a GitHub
- [ ] Cuenta Streamlit creada
- [ ] App desplegada en Streamlit Cloud
- [ ] URL generada y funcional
- [ ] Credenciales OADS probadas
- [ ] Archivo CSV de prueba descargado
- [ ] Link compartido con colaboradores 🎉

---

## 🎓 Recursos

- [Documentación Streamlit](https://docs.streamlit.io/)
- [Streamlit Cloud Docs](https://docs.streamlit.io/deploy/streamlit-community-cloud)
- [EarthCARE Mission](https://www.esa.int/Applications/Observing_the_Earth/EarthCARE)
- [OADS Portal](https://eocat.esa.int/)

---

**¡Tu app web está lista para usar! 🚀**

*Hecho por Onrona Functions - 2025*

