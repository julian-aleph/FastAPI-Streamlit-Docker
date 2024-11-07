import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# URL de la API de FastAPI
# API_URL = "http://localhost:8000" # para probar en local

API_URL = "http://api:8000" # para consumir la api en el contenedor

# Crear pestañas
tab1, tab2, tab3 = st.tabs(["Probar la API", "Explicación del Modelo", "Integración de API, Streamlit y Docker"])

with tab1:
    st.title("Regresión con Bases B-spline")

# Código de prueba para cargar archivos y ajustar el modelo
uploaded_file = st.file_uploader("Seleccione un archivo CSV con columnas 't' y 'y_observed'", type=["csv"])

if uploaded_file is not None:
    d = st.slider("Grado del B-spline (d)", 1, 10, 3)
    response = requests.post(f"{API_URL}/fit", files={"file": uploaded_file}, data={"d": d})

    if response.status_code == 200:
        st.success("Modelo ajustado exitosamente.")
        response_data = response.json()
        st.write(f"Parámetros óptimos encontrados: λ = {response_data['l_opt']:.4f}, c = {response_data['c_opt']}")
    else:
        st.error("Error al cargar el archivo o ajustar el modelo. Verifique el formato.")

st.header("Visualización de la curva de Ajuste")
if st.button("Mostrar Gráfica"):
    response = requests.get(f"{API_URL}/plot")
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        # Cambiado use_column_width=True a use_container_width=True
        st.image(image, caption="Gráfica del Ajuste de la Regresión", use_container_width=True)
    else:
        st.error("Error al generar la gráfica.")

with tab2:
    st.title("Explicación del Modelo de Regresión B-spline")

    st.markdown(r"""
    ## Descripción del Modelo de Regresión B-spline

    La **regresión B-spline** es una técnica de modelado no paramétrico que utiliza funciones base **B-spline** para ajustar una curva a un conjunto de datos. En lugar de asumir una forma específica para la relación entre las variables, la regresión B-spline utiliza una combinación lineal de funciones de base B-spline para capturar la variabilidad en los datos.

    La ecuación del modelo de regresión B-spline es:

    $$
    y = \sum_{j=1}^c \beta_j B_j(t)
    $$

    donde:
    - $y$  es la variable de respuesta.
    - $B_j(t)$ son las funciones de base B-spline de grado $ d $.
    - $\beta_j$ son los coeficientes del modelo que se ajustan a los datos.
    - $c$ es el número de funciones de base B-spline.

    ### Parámetros del Modelo

    - **Grado del B-spline ($ d $)**: Controla la suavidad de las funciones de base. Un grado mayor permite más flexibilidad.
    - **Número de funciones de base ($ c $)**: Define el número de funciones B-spline en la combinación lineal. Un valor mayor de $ c $ aumenta la complejidad del modelo.
    - **Parámetro de regularización ($ \lambda $)**: Penaliza la complejidad del modelo, controlando el ajuste excesivo. Un valor mayor de $ \lambda $ da como resultado una curva más suave.

    ### Criterio de Validación Generalizada (GCV)

    Para seleccionar los valores óptimos de los parámetros, se utiliza el **Criterio de Validación Generalizada (GCV)**, que mide la capacidad de generalización del modelo. La fórmula para el GCV es:

    $$
    \text{GCV} = \frac{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}{\left(1 - \frac{\text{tr}(S)}{n}\right)^2}
    $$

    donde:
    - $ y_i $ son los valores observados y $ \hat{y}_i $ son los valores predichos.
    - $ S $ es la matriz de suavización del modelo.
    - $ \text{tr}(S) $ es la traza de $ S $, que mide la complejidad del modelo.

    El valor de GCV se minimiza para encontrar los valores óptimos de los parámetros $ c $, y $ \lambda $.
    """)

with tab3:
    st.title("Integración de API, Streamlit y Docker")

    st.markdown("""
    ## Integración de API, Streamlit y Docker
    Como proyecto de la compañía para la que laboro actualmente, se utiliza este `ecosistema` de frameworks (fastAPI + Streamli + Docker) para probar los desarrollos del sistema
    de recomendación. Lo reutilizo aquí con un código de regresión en base de funciones Bspline con regularización usando el GCV automáticamente, para optimizar la capacidad de generalización del modelo.
                
    La aplicación utiliza **FastAPI** para manejar los cálculos de regresión y procesamiento de datos. Streamlit se utiliza como la interfaz de usuario, y **Docker** permite empaquetar y ejecutar todo en un entorno aislado y reproducible. Aquí tienes los pasos clave:

    ### 1. FastAPI como Backend

    FastAPI proporciona los endpoints necesarios para:
    - Subir archivos CSV.
    - Ajustar el modelo de regresión B-spline (este es un código reutilizado).
    - Generar y devolver una gráfica del ajuste.

    FastAPI maneja las solicitudes HTTP desde Streamlit y responde con los datos y gráficos solicitados.

    ### 2. Streamlit como Frontend

    Streamlit actúa como la interfaz gráfica del usuario, permitiendo:
    - Cargar archivos y ajustar parámetros.
    - Visualizar los resultados de la regresión en tiempo real.

    Streamlit envía solicitudes HTTP a los endpoints de FastAPI para realizar los cálculos y generar los gráficos.

    ### 3. Docker para Despliegue

    Docker permite empaquetar la aplicación completa (API y Streamlit) en un contenedor, asegurando que se ejecute de forma consistente en cualquier entorno. Los pasos generales son:

    - Crear un archivo `Dockerfile` para definir el entorno de FastAPI y Streamlit.
    - Crear un archivo `docker-compose.yml` para manejar múltiples contenedores, uno para FastAPI y otro para Streamlit.
    - Ejecutar `docker-compose up` para lanzar la aplicación completa en contenedores.

    ### Ejemplo de Comando Docker

    Con el archivo `docker-compose.yml`, puedes ejecutar la aplicación con:

    ```bash
    docker-compose up
    ```

    Esto ejecutará tanto la API de FastAPI como la aplicación de Streamlit en contenedores separados, facilitando la gestión y el despliegue.
    """)