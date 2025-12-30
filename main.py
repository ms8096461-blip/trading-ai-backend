from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Trading AI Backend", version="1.0")


# -----------------------------
# Candle strength function
# -----------------------------
def is_strong_candle(open_p, close_p, high_p, low_p):
    body = abs(close_p - open_p)
    wick = (high_p - low_p) - body

    if body <= 0:
        return False

    if body > wick:
        return True
    return False


# -----------------------------
# API root
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Trading AI backend is live"
    }


# -----------------------------
# Signal endpoint
# -----------------------------
@app.get("/signal")
def get_signal():
    """
    STEP-1:
    Candle strength + basic BUY / SELL / NO TRADE
    (Dummy data for now – real market data later)
    """

    # -------- Dummy candle data (safe for now) --------
    open_p = 1.1000
    close_p = 1.1012
    high_p = 1.1016
    low_p = 1.0994

    # -------- Candle check --------
    if not is_strong_candle(open_p, close_p, high_p, low_p):
        return {
            "pair": "EUR/USD",
            "signal": "NO TRADE",
            "confidence": 40,
            "expiry": None,
            "reason": "Weak candle",
            "time": datetime.utcnow()
        }

    # -------- Direction --------
    if close_p > open_p:
        signal = "BUY"
    else:
        signal = "SELL"

    return {
        "pair": "EUR/USD",
        "signal": signal,
        "confidence": 65,
        "expiry": "1M",
        "reason": "Strong candle",
        "time": datetime.utcnow()
    }
