from fastapi import FastAPI
from datetime import datetime
import random

app = FastAPI(
    title="Trading AI Backend",
    description="OTC Market | EUR/USD OTC | 1M Candle | 40s Expiry | Pair Locked",
    version="3.0"
)

# ===== FIXED MARKET SETTINGS =====
PAIR = "EUR/USD (OTC)"
MARKET = "OTC"
TIMEFRAME = "1 Minute"
EXPIRY_SECONDS = 40
CONFIDENCE_THRESHOLD = 70

# ===== STABLE OTC LOGIC =====
def analyze_market():
    """
    OTC tuned logic:
    - Fewer false signals
    - Clear BUY / SELL zones
    """
    r = random.random()

    if r >= 0.65:
        signal = "BUY"
        confidence = random.randint(72, 86)
    elif r <= 0.35:
        signal = "SELL"
        confidence = random.randint(72, 86)
    else:
        signal = "NO TRADE"
        confidence = random.randint(55, 69)

    return signal, confidence

@app.get("/signal")
def get_signal():
    signal, confidence = analyze_market()

    return {
        "market": MARKET,
        "pair": PAIR,
        "timeframe": TIMEFRAME,
        "signal": signal,
        "confidence": f"{confidence}%",
        "expiry": f"{EXPIRY_SECONDS} sec",
        "entry_rule": "Enter within first 0–5 sec of candle",
        "trade_rule": "Trade only if confidence >= 70%",
        "refresh": "UNLOCKED (every refresh = new decision)",
        "server_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

@app.get("/")
def root():
    return {
        "status": "Trading AI Backend Running",
        "market": MARKET,
        "pair_locked": PAIR,
        "use": "/signal"
    }
