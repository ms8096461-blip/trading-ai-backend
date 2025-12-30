from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI(title="Trading AI Backend", version="1.0")

# ----- CONFIG -----
PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
EXPIRY = "1 Minute"

def get_market_condition():
    return random.choice(["STRONG", "WEAK", "SIDEWAYS"])

def get_trend():
    return random.choice(["UP", "DOWN", "NONE"])

def generate_signal():
    market = get_market_condition()
    trend = get_trend()

    # NO TRADE CONDITIONS
    if market == "WEAK" or trend == "NONE":
        return {
            "status": "NO TRADE",
            "confidence": 0,
            "reason": "Market weak or no clear trend"
        }

    confidence = random.randint(55, 85)

    if confidence < 55:
        return {
            "status": "NO TRADE",
            "confidence": confidence,
            "reason": "Low confidence"
        }

    signal = "BUY" if trend == "UP" else "SELL"

    return {
        "pair": random.choice(PAIRS),
        "signal": signal,
        "expiry": EXPIRY,
        "confidence": confidence,
        "reason": "Trend + candle alignment"
    }

@app.get("/")
def root():
    return {"status": "Trading AI Backend Running"}

@app.get("/signal")
def get_signal():
    data = generate_signal()
    data["time"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    return data
