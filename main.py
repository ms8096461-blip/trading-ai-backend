from fastapi import FastAPI
import random
from datetime import datetime

app = FastAPI()

PAIR = "USD/BRL (OTC)"
EXPIRY_SECONDS = 5
CONFIDENCE_THRESHOLD = 55

def generate_signal():
    direction = random.choice(["BUY", "SELL", "NO TRADE"])
    confidence = random.randint(45, 90)

    if direction == "NO TRADE" or confidence < CONFIDENCE_THRESHOLD:
        return {
            "pair": PAIR,
            "signal": "NO TRADE",
            "confidence": confidence,
            "expiry": EXPIRY_SECONDS,
            "time": datetime.utcnow().strftime("%H:%M:%S")
        }

    return {
        "pair": PAIR,
        "signal": direction,
        "confidence": confidence,
        "expiry": EXPIRY_SECONDS,
        "time": datetime.utcnow().strftime("%H:%M:%S")
    }

@app.get("/signal")
def signal():
    # EVERY REFRESH = NEW SIGNAL (5 sec expiry demo)
    return generate_signal()

@app.get("/")
def root():
    return {
        "status": "Trading AI Running",
        "pair": PAIR,
        "expiry": f"{EXPIRY_SECONDS} sec",
        "mode": "Demo | refresh-based signal"
    }
