# strategy_3.py
from textblob import TextBlob

def strategy_decision(current_price, news_headlines=None):
    """
    Analiza sentimiento de titulares de noticias sobre BTC.
    BUY si el sentimiento promedio es positivo, SELL si negativo.
    """
    # Titulares simulados si no se pasa lista real
    if news_headlines is None:
        news_headlines = [
            "Bitcoin hits new record high as institutions buy in",
            "BTC plummets after regulatory warning",
            "Crypto markets steady after volatile week",
            "Experts say Bitcoin could see new growth",
            "Hackers target crypto exchange in major theft"
        ]

    # Calcula sentimiento de cada noticia
    sentiments = [TextBlob(headline).sentiment.polarity for headline in news_headlines]
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0

    direction = "BUY" if avg_sentiment > 0 else "SELL"
    desc = f"Análisis de sentimiento en noticias (avg: {avg_sentiment:.2f})"
    return direction, desc

# --- PRUEBA rápida ---
if __name__ == "__main__":
    result = strategy_decision(105000)
    print(result)

