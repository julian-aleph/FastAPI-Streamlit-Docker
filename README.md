# Proyecto de Regresión B-Spline con FastAPI y Streamlit

Este proyecto implementa un modelo de **regresión B-spline** para el ajuste de datos y visualización de curvas suavizadas. La aplicación utiliza **FastAPI** como backend para manejar los cálculos de regresión, y **Streamlit** como frontend para interactuar con la API y visualizar resultados. El proyecto está configurado para ejecutarse con **Docker Compose** para facilitar su despliegue.

<h2>Estructura del Proyecto</h2>

<pre><code>project-root/
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

## Requisitos

- **Docker** y **Docker Compose** deben estar instalados en tu sistema.
