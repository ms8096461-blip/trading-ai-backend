from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Trading AI Backend Running"}

@app.get("/signal")
def get_signal():
    signal = random.choice(["BUY", "SELL"])
    confidence = random.randint(65, 85)

    buy_reasons = [
        "RSI oversold",
        "EMA bullish crossover",
        "Uptrend confirmed",
        "Volume increasing"
    ]

    sell_reasons = [
        "RSI overbought",
        "EMA bearish crossover",
        "Downtrend confirmed",
        "Weak momentum"
    ]

    return {
        "signal": signal,
        "confidence": f"{confidence}%",
        "expiry": "2 minutes",
        "why": buy_reasons if signal == "BUY" else sell_reasons,
        "time": datetime.now().isoformat()
    }
