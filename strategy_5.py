# strategy_5.py
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def strategy_decision(current_price, recent_prices=None):
    """
    Usa una red LSTM para predecir la dirección del siguiente precio.
    """
    # Genera 30 precios simulados alrededor de current_price si no se pasan reales
    if recent_prices is None:
        recent_prices = [current_price + np.random.normal(0, current_price*0.01) for _ in range(30)]

    # Preparamos datos para LSTM
    X, y = [], []
    look_back = 5
    for i in range(len(recent_prices) - look_back - 1):
        window = recent_prices[i:(i + look_back)]
        target = 1 if recent_prices[i + look_back] > recent_prices[i + look_back - 1] else 0
        X.append(window)
        y.append(target)
    if len(X) == 0:
        return "BUY", "LSTM (default BUY: pocos datos)"

    X = np.array(X)
    y = np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # Modelo LSTM pequeño
    model = Sequential()
    model.add(LSTM(8, input_shape=(look_back, 1)))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Entrenamiento muy corto para demo
    model.fit(X, y, epochs=5, batch_size=1, verbose=0)

    # Inferencia: ventana más reciente
    X_last = np.array(recent_prices[-look_back:]).reshape((1, look_back, 1))
    pred = model.predict(X_last)[0][0]
    direction = "BUY" if pred > 0.5 else "SELL"
    desc = "LSTM sobre secuencia de precios recientes"
    return direction, desc

# --- PRUEBA rápida ---
if __name__ == "__main__":
    result = strategy_decision(105000)
    print(result)

