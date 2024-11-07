<h2>Estructura del Proyecto</h2>

<pre><code>Proyecto/
├── api/                           # Código y configuración de la API (FastAPI)
│   ├── main.py                    # Código principal de la API de FastAPI
│   ├── Dockerfile                 # Dockerfile para el contenedor de FastAPI
│   ├── requirements.txt           # Requerimientos de Python para FastAPI
├── streamlit_app/                 # Código y configuración de la app de Streamlit
│   ├── app.py                     # Código principal de la app de Streamlit
│   ├── Dockerfile                 # Dockerfile para el contenedor de Streamlit
│   ├── requirements.txt           # Requerimientos de Python para Streamlit
├── docker-compose.yml             # Archivo para ejecutar ambos servicios (FastAPI y Streamlit)
</code></pre>