from fastapi import FastAPI
import random
from datetime import datetime, timedelta

app = FastAPI(title="Trading AI Backend", version="3.0")

PAIRS = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
EXPIRY_OPTIONS = ["1M", "3M"]

# ---- Signal Lock Memory ----
LAST_SIGNAL_TIME = None
LAST_SIGNAL_DATA = None
LOCK_SECONDS = 60


def generate_signal_logic():
    market = random.choice(["STRONG", "WEAK", "SIDEWAYS"])
    trend = random.choice(["UP", "DOWN", "NONE"])

    # NO TRADE filters
    if market != "STRONG" or trend == "NONE":
        return {
            "status": "NO TRADE",
            "confidence": random.randint(40, 55),
            "reason": "Market weak or no clear trend"
        }

    confidence = random.randint(60, 85)
    if confidence < 60:
        return {
            "status": "NO TRADE",
            "confidence": confidence,
            "reason": "Low confidence"
        }

    signal = "BUY" if trend == "UP" else "SELL"
    expiry = "3M" if confidence >= 75 else "1M"

    return {
        "pair": random.choice(PAIRS),
        "signal": signal,
        "expiry": expiry,
        "confidence": confidence,
        "reason": "Trend aligned + confidence OK"
    }


@app.get("/")
def root():
    return {"status": "Trading AI Backend Running (Live-Like Demo)"}


@app.get("/signal")
def get_signal():
    global LAST_SIGNAL_TIME, LAST_SIGNAL_DATA

    now = datetime.utcnow()

    # ---- Signal Lock (1 minute) ----
    if LAST_SIGNAL_TIME and (now - LAST_SIGNAL_TIME).seconds < LOCK_SECONDS:
        locked = LAST_SIGNAL_DATA.copy()
        locked["locked"] = True
        locked["time"] = LAST_SIGNAL_TIME.strftime("%Y-%m-%d %H:%M:%S UTC")
        return locked

    # ---- Generate New Signal ----
    data = generate_signal_logic()
    data["locked"] = False
    data["time"] = now.strftime("%Y-%m-%d %H:%M:%S UTC")

    LAST_SIGNAL_TIME = now
    LAST_SIGNAL_DATA = data

    return data
