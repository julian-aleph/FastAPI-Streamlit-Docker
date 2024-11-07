from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
from regression_model import BasisRegression
import pickle

app = FastAPI()

# Variables globales para almacenar datos
X_data, y_observed_data = None, None
MODEL_PATH = "model.pkl"  # Ruta para guardar el modelo ajustado

@app.post("/fit")
async def fit_model(file: UploadFile = File(...), d: int = 3):
    """
    Endpoint para ajustar el modelo de regresión a los datos observados.
    El archivo CSV debe tener columnas 't' y 'y_observed'.
    
    Parámetros:
    - file: Archivo CSV con columnas 't' y 'y_observed'.
    - d: Grado del B-spline.
    """
    global X_data, y_observed_data

    try:
        # Leer el archivo CSV en un DataFrame
        df = pd.read_csv(file.file)
        
        # Verificar que el archivo contenga las columnas necesarias
        if not {'t', 'y_observed'}.issubset(df.columns):
            raise ValueError("El archivo CSV debe tener columnas 't' y 'y_observed'.")

        # Guardar los datos en variables globales
        X_data = df['t'].values
        y_observed_data = df['y_observed'].values

        # Crear el modelo de regresión
        model = BasisRegression(d=d)
        
        # Optimizar los parámetros l y c
        l_opt, c_opt = model.optimize_parameters(X_data, y_observed_data)
        
        # Ajustar el modelo con los parámetros óptimos
        model.fit(X_data, y_observed_data, l=l_opt, c=c_opt)
        
        # Guardar el modelo en un archivo .pkl
        model.save_model(MODEL_PATH)
        
        return {
            "message": "Modelo ajustado y guardado exitosamente con parámetros óptimos.",
            "l_opt": l_opt,
            "c_opt": c_opt
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el archivo: {str(e)}")

@app.get("/plot")
def plot():
    """
    Endpoint para generar y devolver la gráfica con el ajuste de regresión.
    Muestra los datos observados y la curva ajustada.
    """
    global X_data, y_observed_data
    if X_data is None or y_observed_data is None:
        raise HTTPException(status_code=400, detail="Primero debe cargar los datos observados y ajustar el modelo.")

    # Cargar el modelo desde el archivo .pkl
    model = BasisRegression.load_model(MODEL_PATH)

    # Crear puntos para la predicción en un rango basado en los datos originales
    t_values = np.linspace(min(X_data), max(X_data), 100)
    y_pred = model.predict(t_values)

    # Crear la gráfica
    fig, ax = plt.subplots()
    
    # Graficar los datos observados con ruido
    ax.scatter(X_data, y_observed_data, color="red", label="Datos Observados")
    
    # Graficar la curva ajustada
    ax.plot(t_values, y_pred, label="Curva de Ajuste", color="blue")
    
    # Configuración de la gráfica
    ax.set_title(f"Ajuste de Regresión con B-Splines (l={model.l:.4f}, c={model.c})")
    ax.set_xlabel("t")
    ax.set_ylabel("y")
    ax.legend()

    # Guardar la imagen en un buffer
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    # Devolver la imagen como una respuesta de tipo streaming
    return StreamingResponse(buf, media_type="image/png")
