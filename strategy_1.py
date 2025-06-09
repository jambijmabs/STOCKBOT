# strategy_1.py
import numpy as np
from sklearn.linear_model import LinearRegression

def strategy_decision(current_price, recent_prices=None):
    """
    Usa regresión lineal para predecir tendencia.
    recent_prices: lista de los últimos precios (floats)
    current_price: último precio (float, sólo para compatibilidad con main)
    """
    # Si no se pasan precios recientes, genera 10 precios aleatorios simulados cerca de current_price
    if recent_prices is None:
        recent_prices = [current_price + np.random.normal(0, current_price*0.01) for _ in range(10)]

    X = np.arange(len(recent_prices)).reshape(-1, 1)
    y = np.array(recent_prices)

    # Ajusta modelo de regresión lineal
    model = LinearRegression()
    model.fit(X, y)
    slope = model.coef_[0]

    # Lógica: si la pendiente es positiva, BUY; si negativa, SELL
    if slope > 0:
        direction = "BUY"
    else:
        direction = "SELL"
    desc = "Regresión lineal sobre precios recientes (pendiente: {:.5f})".format(slope)
    return direction, desc

# --- PRUEBA rápida ---
if __name__ == "__main__":
    # Ejemplo de uso, con precios simulados (puedes comentar este bloque si lo importas en main)
    result = strategy_decision(105000)
    print(result)

