# strategy_2.py
import numpy as np
from sklearn.neural_network import MLPClassifier

def strategy_decision(current_price, recent_prices=None):
    """
    Usa un perceptrón multicapa (MLP) para predecir la dirección.
    Entrena rápido sobre datos simulados (prototipo).
    """
    # Si no se pasan precios recientes, genera 15 precios random alrededor de current_price
    if recent_prices is None:
        recent_prices = [current_price + np.random.normal(0, current_price*0.01) for _ in range(15)]

    # Preparar X e y: la red aprende si el siguiente precio subió o bajó
    X = np.array([recent_prices[i:i+5] for i in range(len(recent_prices)-5)])
    y = np.array([
        1 if recent_prices[i+5] > recent_prices[i+4] else 0
        for i in range(len(recent_prices)-5)
    ])
    if len(X) == 0:  # Fallback, por si recent_prices es muy corta
        return "BUY", "MLP (default BUY: pocos datos)"
    model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=200)
    model.fit(X, y)
    # Predice con el último vector de características
    pred = model.predict([recent_prices[-5:]])[0]
    direction = "BUY" if pred == 1 else "SELL"
    desc = "MLPClassifier sobre ventana de precios recientes"
    return direction, desc

# --- PRUEBA rápida ---
if __name__ == "__main__":
    result = strategy_decision(105000)
    print(result)

