from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Trading AI Backend Running"}

@app.get("/signal")
def signal():
    now = datetime.utcnow()
    seconds = now.second

    # Book rule: last 30 sec = NO TRADE
    if seconds >= 30:
        return {
            "pair": "EUR/USD",
            "signal": "NO TRADE",
            "reason": "Wait for candle close",
            "confidence": "0%",
            "time": now
        }

    # Training candles (fake data, logic real)
    candle_1 = random.choice(["GREEN", "RED"])
    candle_2 = random.choice(["GREEN", "RED"])

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
        "time": now
    }
