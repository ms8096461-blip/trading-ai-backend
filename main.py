from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Trading AI Backend", version="2.0")


# =========================
# Utility Functions
# =========================

def is_strong_candle(open_p, close_p, high_p, low_p):
    body = abs(close_p - open_p)
    wick = (high_p - low_p) - body
    if body <= 0:
        return False
    return body > wick


def candle_direction(open_p, close_p):
    if close_p > open_p:
        return "BUY"
    elif close_p < open_p:
        return "SELL"
    return None


# =========================
# Root
# =========================

@app.get("/")
def root():
    return {"status": "running", "message": "Trading AI Backend Live"}


# =========================
# SIGNAL ENGINE
# =========================

@app.get("/signal")
def get_signal():
    """
    STEP-1: 1M candle strength
    STEP-2: 3M trend confirmation
    STEP-3: Confidence engine
    STEP-4: Expiry decision
    """

    # -------- DUMMY DATA (safe, real data later) --------
    # 1 Minute candle
    o1, c1, h1, l1 = 1.1000, 1.1012, 1.1016, 1.0994

    # 3 Minute candle (trend)
    o3, c3, h3, l3 = 1.0985, 1.1015, 1.1020, 1.0978

    # =========================
    # STEP-1: 1M Candle Check
    # =========================
    if not is_strong_candle(o1, c1, h1, l1):
        return {
            "signal": "NO TRADE",
            "confidence": 40,
            "reason": "Weak 1M candle",
            "time": datetime.utcnow()
        }

    dir_1m = candle_direction(o1, c1)

    # =========================
    # STEP-2: 3M Trend Check
    # =========================
    if not is_strong_candle(o3, c3, h3, l3):
        return {
            "signal": "NO TRADE",
            "confidence": 45,
            "reason": "Weak 3M trend",
            "time": datetime.utcnow()
        }

    dir_3m = candle_direction(o3, c3)

    if dir_1m != dir_3m:
        return {
            "signal": "NO TRADE",
            "confidence": 50,
            "reason": "1M & 3M direction mismatch",
            "time": datetime.utcnow()
        }

    # =========================
    # STEP-3: Confidence Engine
    # =========================
    confidence = 65

    # Extra strength bonus
    if abs(c1 - o1) > abs(o3 - c3) * 0.5:
        confidence += 10

    if confidence < 60:
        return {
            "signal": "NO TRADE",
            "confidence": confidence,
            "reason": "Low confidence",
            "time": datetime.utcnow()
        }

    # =========================
    # STEP-4: Expiry Decision
    # =========================
    expiry = "1M"
    if confidence >= 75:
        expiry = "3M"

    return {
        "pair": "EUR/USD",
        "signal": dir_1m,
        "confidence": confidence,
        "expiry": expiry,
        "reason": "1M + 3M aligned strong trend",
        "time": datetime.utcnow()
    }
