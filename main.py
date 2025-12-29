from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Trading AI Backend Running"}

@app.get("/signal")
def signal():
    return {
        "pair": "EUR/USD",
        "signal": "BUY",
        "expiry": "1 minute",
        "confidence": "80%"
    }
