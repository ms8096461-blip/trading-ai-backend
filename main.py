from fastapi import FastAPI
import random
import time
from datetime import datetime

app = FastAPI()

PAIR = "USD/BRL (OTC)"
EXPIRY_SECONDS = 40
CONFIDENCE_THRESHOLD = 70

last_candle_minute = None
current_signal = {
    "pair": PAIR,
    "signal": "NO TRADE",
    "confidence": 0,
    "expiry": EXPIRY_SECONDS,
    "reason": "Waiting for new candle"
}

def analyze_market():
    """
    Fake candle logic (demo AI)
    Replace later with real indicators if needed
    """
    direction = random.choice(["BUY", "SELL", "NO TRADE"])
    confidence = random.randint(55, 90)

    if confidence < CONFIDENCE_THRESHOLD:
        return "NO TRADE", confidence, "Low confidence"

    if direction == "BUY":
        return "BUY", confidence, "Bullish candle pressure"
    elif direction == "SELL":
        return "SELL", confidence, "Bearish candle pressure"
    else:
        return "NO TRADE", confidence, "Market unclear"

@app.get("/signal")
def get_signal():
    global last_candle_minute, current_signal

    now = datetime.utcnow()
    current_minute = now.minute

    # Detect new candle
    if last_candle_minute != current_minute:
        last_candle_minute = current_minute

        signal, confidence, reason = analyze_market()

        current_signal = {
            "pair": PAIR,
            "signal": signal,
            "confidence": confidence,
            "expiry": EXPIRY_SECONDS,
            "reason": reason,
            "candle_time": now.strftime("%H:%M:%S")
        }

    return current_signal

@app.get("/")
def root():
    return {
        "status": "Trading AI Running",
        "pair": PAIR,
        "expiry": f"{EXPIRY_SECONDS} sec",
        "rule": "Trade only in first 5 sec of new candle"
    }
