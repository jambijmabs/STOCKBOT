# strategy_4.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def compute_rsi(prices, period=5):
    """Calcula RSI simple para una lista de precios."""
    deltas = np.diff(prices)
    up = deltas[deltas > 0].sum() / period if len(deltas[deltas > 0]) > 0 else 0
    down = -deltas[deltas < 0].sum() / period if len(deltas[deltas < 0]) > 0 else 0
    rs = up / down if down != 0 else 0
    return 100 - (100 / (1 + rs)) if down != 0 else 100

def compute_sma(prices, period=5):
    """Calcula media móvil simple."""
    return np.mean(prices[-period:])

def strategy_decision(current_price, recent_prices=None):
    """
    Calcula indicadores técnicos y predice dirección con RandomForest.
    """
    # Genera 15 precios simulados cerca de current_price si no se pasan reales
    if recent_prices is None:
        recent_prices = [current_price + np.random.normal(0, current_price*0.01) for _ in range(15)]

    # Calcula features para cada punto de la serie
    X, y = [], []
    for i in range(len(recent_prices) - 6):
        window = recent_prices[i:i+6]
        sma = compute_sma(window, period=5)
        rsi = compute_rsi(window, period=5)
        pct_change = (window[-1] - window[0]) / window[0]
        # Target: 1 si subió siguiente tick, 0 si bajó o se mantuvo
        target = 1 if recent_prices[i+6] > window[-1] else 0
        X.append([window[-1], sma, rsi, pct_change])
        y.append(target)

    if len(X) == 0:
        return "BUY", "Random Forest (default BUY: pocos datos)"
    
    model = RandomForestClassifier(n_estimators=10)
    model.fit(X, y)

    # Features para el último punto disponible
    sma = compute_sma(recent_prices[-6:], period=5)
    rsi = compute_rsi(recent_prices[-6:], period=5)
    pct_change = (recent_prices[-1] - recent_prices[-6]) / recent_prices[-6]
    features = [recent_prices[-1], sma, rsi, pct_change]
    pred = model.predict([features])[0]
    direction = "BUY" if pred == 1 else "SELL"
    desc = "Random Forest sobre indicadores técnicos (SMA, RSI, cambio %)"
    return direction, desc

# --- PRUEBA rápida ---
if __name__ == "__main__":
    result = strategy_decision(105000)
    print(result)

