from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

# Home route
@app.get("/")
def home():
    return {"status": "Trading AI Backend Running"}

# Signal route (book + candle rules)
@app.get("/signal")
def signal():

    # Training candles (fake data, logic real)
    candle_1 = random.choice(["GREEN", "RED"])
    candle_2 = random.choice(["GREEN", "RED"])

    # Book-based rules
    if candle_1 == candle_2 == "GREEN":
        trade_signal = "BUY"
        confidence = "65%"
    elif candle_1 == candle_2 == "RED":
        trade_signal = "SELL"
        confidence = "65%"
    else:
        trade_signal = "NO TRADE"
        confidence = "0%"

    return {
        "pair": "EUR/USD",
        "last_candle": candle_1,
        "previous_candle": candle_2,
        "signal": trade_signal,
        "expiry": "1 minute",
        "confidence": confidence,
        "time": datetime.utcnow()
    }
