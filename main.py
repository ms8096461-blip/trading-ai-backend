from fastapi import FastAPI
import threading, time, random
from collections import deque

app = FastAPI()

# =========================
# GLOBAL STATE
# =========================
STATE = {
    "pair": "EUR/USD",
    "signal": "NO TRADE",
    "confidence": 0,
    "expiry": "1 minute",
    "trend": "NEUTRAL",
    "momentum": "NEUTRAL",
    "volatility": "NORMAL",
    "reason": "Waiting for candle close",
    "last_update": ""
}

# Rolling candles (mock market engine for demo/logic)
# Each candle: (open, high, low, close)
candles = deque(maxlen=20)

# =========================
# HELPER LOGIC (BOOK-STYLE)
# =========================
def ema(values, period):
    if len(values) < period:
        return None
    k = 2 / (period + 1)
    e = values[0]
    for v in values[1:]:
        e = v * k + e * (1 - k)
    return e

def rsi(values, period=14):
    if len(values) < period + 1:
        return None
    gains, losses = 0, 0
    for i in range(-period, -1):
        diff = values[i+1] - values[i]
        if diff > 0: gains += diff
        else: losses -= diff
    if losses == 0: return 100
    rs = gains / losses
    return 100 - (100 / (1 + rs))

def candle_strength(c):
    o,h,l,cl = c
    body = abs(cl - o)
    wick = (h - l) - body
    if body == 0: return 0
    return body / max(wick, 0.0001)

# =========================
# MOCK MARKET (1-MIN AUTO)
# =========================
def make_candle(prev_close):
    # simple stochastic move
    o = prev_close
    move = random.uniform(-0.0006, 0.0006)
    cl = o + move
    h = max(o, cl) + random.uniform(0, 0.0003)
    l = min(o, cl) - random.uniform(0, 0.0003)
    return (o, h, l, cl)

# =========================
# CORE SIGNAL ENGINE
# =========================
def engine():
    # seed
    price = 1.1000
    for _ in range(5):
        c = make_candle(price)
        candles.append(c)
        price = c[3]

    while True:
        # 1) build new 1-minute candle
        c = make_candle(candles[-1][3])
        candles.append(c)
        closes = [x[3] for x in candles]

        # 2) indicators
        ema5 = ema(closes[-5:], 5)
        ema13 = ema(closes[-13:], 13)
        r = rsi(closes, 14)
        strength = candle_strength(c)

        # 3) trend & momentum
        trend = "NEUTRAL"
        if ema5 and ema13:
            if ema5 > ema13: trend = "UP"
            elif ema5 < ema13: trend = "DOWN"

        momentum = "NEUTRAL"
        if r is not None:
            if r > 60: momentum = "BULLISH"
            elif r < 40: momentum = "BEARISH"

        # 4) volatility proxy
        vol = "NORMAL"
        if strength > 2.2: vol = "HIGH"
        elif strength < 0.6: vol = "LOW"

        # 5) decision matrix (BOOK-STYLE)
        confidence = 50
        signal = "NO TRADE"
        reasons = []

        if trend == "UP" and momentum == "BULLISH":
            confidence += 18; reasons.append("Trend+Momentum aligned (UP)")
        if trend == "DOWN" and momentum == "BEARISH":
            confidence += 18; reasons.append("Trend+Momentum aligned (DOWN)")
        if vol == "HIGH":
            confidence += 8; reasons.append("Strong candle")
        if vol == "LOW":
            confidence -= 10; reasons.append("Low volatility")
        if r is not None and (r > 70 or r < 30):
            confidence -= 6; reasons.append("Overbought/Oversold risk")

        confidence = max(0, min(95, confidence))

        if confidence >= 70:
            if trend ==
