import random

signals = [
    "EUR/USD ВВЕРХ 5 минут",
    "GBP/USD ВНИЗ 3 минуты",
    "USD/JPY ВВЕРХ 1 минута",
    "AUD/USD ВНИЗ 5 минут"
]

def get_signal():
    return random.choice(signals)
