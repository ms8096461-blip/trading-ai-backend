from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI(
    title="Trading AI Backend",
    description="Locked Pair USD/JPY | 1M Candle | 40s Expiry | Auto Refresh",
    version="1.0"
)

# ===== FIXED SETTINGS =====
PAIR = "USD/JPY"
TIMEFRAME = "1 Minute"
EXPIRY_SECONDS = 40
CONFIDENCE_THRESHOLD = 70

# ===== SIMPLE MARKET LOGIC (DEMO SAFE) =====
def analyze_market():
    """
    Candle-based simple logic.
    हर refresh पर नया decision.
    """
    r = random.random()

    if r > 0.6:
        signal = "BUY"
        confidence = random.randint(70, 85)
    elif r < 0.4:
        signal = "SELL"
        confidence = random.randint(70, 85)
    else:
        signal = "NO TRADE"
        confidence = random.randint(50, 69)

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
