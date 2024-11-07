import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(42)

num_points = 100
t = np.linspace(0, 10, num_points)


def true_function(t):
    return 0.3*np.sin(t-1) + 0.5 * np.cos(2 * t)

xx = np.linspace(0, 10, 80)
y_true = true_function(xx) 


noise = np.random.normal(0, 0.3, num_points) 
y_observed = true_function(t) + noise  


data = pd.DataFrame({"t": t, "y_observed": y_observed})
data.to_csv("simulated_data.csv", index=False)
print("Archivo 'simulated_data.csv' generado correctamente")


plt.figure(figsize=(10, 5))
plt.plot(xx, y_true, linewidth=2)
plt.scatter(t, y_observed, color='red', alpha=0.6, s=5)
plt.grid(True)
plt.show()

