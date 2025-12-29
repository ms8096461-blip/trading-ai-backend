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
            "reason": "Waiting for candle close",
            "confidence": "0%",
            "time": now
        }

    # Training candles (fake data, logic real)
    candle_1 = random.choice(["GREEN", "RED"])
    candle_2 = random.choice(["GREEN", "RED"])

    confidence_score = 0

    # Rule 1: 2 candle confirmation
    if candle_1 == candle_2:
        confidence_score += 30

    # Rule 2: Good timing
    confidence_score += 20

    # Decision
    if candle_1 == candle_2 == "GREEN":
        trade_signal = "BUY"
    elif candle_1 == candle_2 == "RED":
        trade_signal = "SELL"
    else:
        trade_signal = "NO TRADE"
        confidence_score = 0

    # Final confidence (cap)
    confidence = f"{min(confidence_score, 70)}%"

    return {
        "pair": "EUR/USD",
        "last_candle": candle_1,
        "previous_candle": candle_2,
        "signal": trade_signal,
        "expiry": "1 minute",
        "confidence": confidence,
        "time": now
    }
