from fastapi import FastAPI
import requests
import os
from datetime import datetime

app = FastAPI()

ALPHA_KEY = os.getenv("ALPHA_KEY")

PAIR = "EURUSD"
TIMEFRAME = "1min"

def get_candles():
    url = (
        "https://www.alphavantage.co/query?"
        f"function=FX_INTRADAY&from_symbol=EUR&to_symbol=USD"
        f"&interval={TIMEFRAME}&apikey={ALPHA_KEY}&outputsize=compact"
    )
    r = requests.get(url)
    data = r.json()

    candles = data.get("Time Series FX (1min)", {})
    keys = list(candles.keys())

    if len(keys) < 2:
        return None

    c1 = candles[keys[0]]  # latest closed
    c2 = candles[keys[1]]  # previous

    return c1, c2

def candle_color(c):
    if float(c["4. close"]) > float(c["1. open"]):
        return "GREEN"
    elif float(c["4. close"]) < float(c["1. open"]):
        return "RED"
    else:
        return "DOJI"

@app.get("/")
def signal():
    candles = get_candles()

    if not candles:
        return {"status": "NO TRADE", "reason": "No candle data"}

    c1, c2 = candles

    color1 = candle_color(c1)
    color2 = candle_color(c2)

    if color1 == "DOJI" or color2 == "DOJI":
        return {
            "pair": "EUR/USD",
            "signal": "NO TRADE",
            "confidence": "0%",
            "reason": "Doji candle"
        }

    if color1 == color2:
        signal = "BUY" if color1 == "GREEN" else "SELL"
        confidence = 65

        body1 = abs(float(c1["4. close"]) - float(c1["1. open"]))
        body2 = abs(float(c2["4. close"]) - float(c2["1. open"]))

        if body1 > body2:
            confidence += 5

        return {
            "pair": "EUR/USD",
            "signal": signal,
            "confidence": f"{confidence}%",
            "expiry": "1 MIN",
            "reason": "2 candle confirmation"
        }

    return {
        "pair": "EUR/USD",
        "signal": "NO TRADE",
        "confidence": "0%",
        "reason": "No confirmation"
    }
