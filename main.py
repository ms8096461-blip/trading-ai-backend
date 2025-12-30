from fastapi import FastAPI
import time, random

app = FastAPI()

STATE = {
    "pair": "EUR/USD",
    "signal": "NO TRADE",
    "confidence": 0,
    "expiry": "1 minute",
    "last_update": ""
}

last_minute = None

def generate_signal():
    confidence = random.randint(40, 90)
    if confidence >= 70:
        signal = random.choice(["BUY", "SELL"])
    else:
        signal = "NO TRADE"

    STATE.update({
        "pair": random.choice([
            "EUR/USD", "GBP/USD", "USD/JPY",
            "EUR/USD OTC", "GBP/USD OTC"
        ]),
        "signal": signal,
        "confidence": confidence,
        "expiry": "1 minute",
        "last_update": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.get("/")
def root():
    return {"status": "Trading AI Backend Running"}

@app.get("/signal")
def signal():
    global last_minute
    current_minute = int(time.time() / 60)

    # 🔥 AUTO UPDATE EVERY NEW MINUTE (NO THREAD, NO CRASH)
    if last_minute != current_minute:
        generate_signal()
        last_minute = current_minute

    return STATE
