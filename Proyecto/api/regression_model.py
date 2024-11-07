import numpy as np
from scipy.interpolate import BSpline
from scipy.linalg import inv
from scipy.optimize import minimize
import pickle

class BasisRegression:
    """
    Clase para realizar regresión usando bases de funciones B-splines.
    """

    def __init__(self, d=3):
        """
        Inicializa el modelo con el grado de los B-splines.
        
        Parámetros:
        - d: Grado del B-spline (por defecto es 3).
        """
        self.coefficients = None     # Coeficientes del modelo ajustado
        self.A = None                # Matriz de ajuste utilizada en el modelo
        self.Sl_matrix = None        # Matriz de suavización
        self.c = None                # Número de funciones de base
        self.l = None                # Parámetro de regularización lambda
        self.d = d                   # Grado del B-spline
        self.knots_ = None           # Nodos (knots) calculados para los B-splines

    def knots(self, t, num_knots=None):
        """
        Calcula los nodos (knots) para los B-splines, extendiéndolos en los extremos
        para soportar el ajuste en el rango de datos.
        
        Parámetros:
        - t: Vector de datos de entrada (eje x).
        - num_knots: Número total de nodos (knots) a calcular. Si no se proporciona, se calcula en función de `c` y `d`.
        
        Retorna:
        - extended_knots: Vector de nodos extendidos en los extremos.
        """
        if num_knots is None:
            num_knots = self.c + self.d + 1  # Número total de nodos basado en `c` y `d`
        
        # Calcular posiciones de los nodos internos usando cuantiles de los datos
        quantiles = np.linspace(0, 1, num_knots - self.d * 2)
        knots = np.quantile(t, quantiles)
        
        # Extender los nodos en los extremos para soportar B-splines de orden superior
        spacing_start = knots[1] - knots[0]
        spacing_end = knots[-1] - knots[-2]
        extended_knots = np.concatenate((
            [knots[0] - i * spacing_start for i in range(self.d, 0, -1)],
            knots,
            [knots[-1] + i * spacing_end for i in range(1, self.d + 1)]
        ))
        return extended_knots

    def build_design_matrix(self, t, knots, degree):
        """
        Construye la matriz de diseño utilizando B-splines como funciones de base.
        
        Parámetros:
        - t: Vector de datos de entrada (eje x).
        - knots: Vector de nodos para los B-splines.
        - degree: Grado de los B-splines.
        
        Retorna:
        - Matriz de diseño evaluada en los puntos `t`.
        """
        bspline = BSpline(knots, np.eye(len(knots) - degree - 1), degree)
        return bspline(t)

    def fit(self, X, y, l=0, c=None):
        """
        Ajusta el modelo de regresión a los datos proporcionados usando B-splines y regularización.
        
        Parámetros:
        - X: Vector de datos de entrada (eje x).
        - y: Vector de datos de salida (eje y).
        - l: Parámetro de regularización lambda.
        - c: Número de funciones de base (si no se especifica, se calcula).
        
        Almacena:
        - Los coeficientes ajustados, nodos y matriz de suavización en los atributos de la clase.
        """
        if c is None:
            c = int(len(X) / 4) + 4  # Calcular `c` por defecto en función de los datos
        self.c = c
        self.l = l  # Almacenar el valor de lambda

        # Validar que el número de funciones de base `c` sea mayor que el grado `d`
        if self.c <= self.d:
            raise ValueError("El número de funciones de base `c` debe ser mayor que el grado `d`.")
        
        # Calcular nodos y matriz de diseño
        self.knots_ = self.knots(X, num_knots=self.c + self.d + 1)
        Phi = self.build_design_matrix(X, self.knots_, self.d)

        # Calcular la matriz de ajuste utilizando regularización
        lambda_eye = l * np.eye(Phi.shape[1])
        self.A = inv(Phi.T @ Phi + lambda_eye) @ Phi.T
        self.Sl_matrix = Phi @ self.A  # Matriz de suavización
        self.coefficients = self.A @ y  # Calcular y almacenar los coeficientes

    def predict(self, x):
        """
        Realiza predicciones en nuevos datos usando el modelo ajustado.
        
        Parámetros:
        - x: Vector de datos de entrada para predicción.
        
        Retorna:
        - Vector de predicciones.
        """
        return np.dot(self.coefficients, self.build_design_matrix(x, self.knots_, self.d).T)

    def calculate_gcv(self, X, y):
        """
        Calcula el Criterio de Validación Generalizada (GCV) para el modelo ajustado.
        
        Parámetros:
        - X: Vector de datos de entrada (eje x).
        - y: Vector de datos de salida (eje y).
        
        Retorna:
        - gcv_value: Valor del GCV calculado.
        """
        y_pred = self.predict(X)
        residuals = y - y_pred
        mse = np.mean(residuals**2)  # Error cuadrático medio

        # Grados de libertad del modelo (traza de la matriz de suavización)
        df = np.trace(self.Sl_matrix)
        n = len(X)  # Número de muestras

        # Calcular el valor de GCV
        gcv_value = mse / (1 - df / n)**2
        return gcv_value

    def optimize_parameters(self, X, y, l_range=(0.0, 1.0), c_range=(5, 15)):
        """
        Encuentra los valores óptimos de l y c minimizando el GCV.
        
        Parámetros:
        - X: Vector de datos de entrada (eje x).
        - y: Vector de datos de salida (eje y).
        - l_range: Rango de valores posibles para `l` (lambda).
        - c_range: Rango de valores posibles para `c` (número de funciones de base).
        
        Retorna:
        - l_opt: Valor óptimo de `l`.
        - c_opt: Valor óptimo de `c`.
        """
        def objective(params):
            l, c = params
            self.fit(X, y, l=l, c=int(c))
            return self.calculate_gcv(X, y)

        # Usar minimización para encontrar los mejores valores de `l` y `c`
        result = minimize(objective, x0=[0.1, 10], bounds=[l_range, c_range])
        l_opt, c_opt = result.x
        return l_opt, int(c_opt)

    def save_model(self, filepath):
        """
        Guarda el modelo ajustado en un archivo .pkl.
        
        Parámetros:
        - filepath: Ruta del archivo donde se guardará el modelo.
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(filepath):
        """
        Carga un modelo ajustado desde un archivo .pkl.
        
        Parámetros:
        - filepath: Ruta del archivo desde el cual se cargará el modelo.
        
        Retorna:
        - Modelo cargado desde el archivo.
        """
        with open(filepath, 'rb') as f:
            return pickle.load(f)