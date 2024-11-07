# Proyecto de Regresión B-Spline con FastAPI y Streamlit

Este proyecto implementa un modelo de **regresión B-spline** para el ajuste de datos y visualización de curvas suavizadas. La aplicación utiliza **FastAPI** como backend para manejar los cálculos de regresión, y **Streamlit** como frontend para interactuar con la API y visualizar resultados. El proyecto está configurado para ejecutarse con **Docker Compose** para facilitar su despliegue.

## Configuración y Ejecución

### 1. Clonar el repositorio

   ```bash
   git clone https://github.com/julian-aleph/FastAPI-Streamlit-Docker.git
   cd FastAPI-Streamlit-Docker
   ```

### 2. Ejecutar docker Compose

   ```bash
   docker-compose up --build
   ```

### 3. Acceder a la aplicación

   ```bash
   - API de FastAPI: http://localhost:8000
   - Aplicación de Streamlit: http://localhost:8501
   ```


## Requisitos

- **Docker** y **Docker Compose** deben estar instalados en tu sistema.

## Nota

Este proyecto implementa un módulo de regresión B-spline con regularización (reciclado de un proyecto anterior), utilizando el método de validación cruzada generalizada (GCV) para determinar los parámetros óptimos de suavización y el tamaño de la base. El modelo se despliega mediante FastAPI, y los endpoints se consumen en una interfaz construida con Streamlit.
