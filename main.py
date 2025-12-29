from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Trading AI Backend Running"}
