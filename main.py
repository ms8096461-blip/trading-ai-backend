from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

PAIR = "USD/BRL (OTC)"
EXPIRY_SECONDS = 10
CONFIDENCE_THRESHOLD = 60

def generate_signal():
    direction = random.choice(["BUY", "SELL", "NO TRADE"])
    confidence = random.randint(50, 90)

    if direction == "NO TRADE" or confidence < CONFIDENCE_THRESHOLD:
        return {
            "pair": PAIR,
            "signal": "NO TRADE",
            "confidence": confidence,
            "expiry": EXPIRY_SECONDS,
            "reason": "Low confidence / unclear market",
            "time": datetime.utcnow().strftime("%H:%M:%S")
        }

    return {
        "pair": PAIR,
        "signal": direction,
        "confidence": confidence,
        "expiry": EXPIRY_SECONDS,
        "reason": "OTC fast scalp signal",
        "time": datetime.utcnow().strftime("%H:%M:%S")
    }

@app.get("/signal")
def signal():
    # EVERY REFRESH = NEW SIGNAL
    return generate_signal()

@app.get("/")
def root():
    return {
        "status": "Trading AI Running",
        "pair": PAIR,
        "expiry": f"{EXPIRY_SECONDS} sec",
        "mode": "Refresh-based signal (fast OTC)"
    }
