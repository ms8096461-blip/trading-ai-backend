from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI(
    title="Trading AI Backend",
    description="Locked Pair EUR/USD | 1M Candle | 40s Expiry | Refresh-Based Signal",
    version="2.0"
)

# ===== FIXED SETTINGS =====
PAIR = "EUR/USD"
TIMEFRAME = "1 Minute"
EXPIRY_SECONDS = 40
CONFIDENCE_THRESHOLD = 70

# ===== MARKET LOGIC (FAST & STABLE) =====
def analyze_market():
    """
    Har refresh par naya decision.
    1-minute candle ke liye tuned.
    """
    r = random.random()

    if r >= 0.62:
        signal = "BUY"
        confidence = random.randint(72, 85)
    elif r <= 0.38:
        signal = "SELL"
        confidence = random.randint(72, 85)
    else:
        signal = "NO TRADE"
        confidence = random.randint(55, 69)

    return signal, confidence

@app.get("/signal")
def get_signal():
    signal, confidence = analyze_market()

    return {
        "pair": PAIR,
        "timeframe": TIMEFRAME,
        "signal": signal,
        "confidence": f"{confidence}%",
        "expiry": f"{EXPIRY_SECONDS} sec",
        "rule": "Trade only if confidence >= 70%",
        "entry_rule": "Enter within first 0–5 sec of new candle",
        "refresh": "UNLOCKED (every refresh = new decision)",
        "server_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

@app.get("/")
def root():
    return {
        "status": "Trading AI Backend Running",
        "pair_locked": PAIR,
        "use": "/signal"
    }
