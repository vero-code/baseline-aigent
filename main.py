# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    """This endpoint returns a welcome message."""
    return {"message": "Baseline AIgent server is running! 🚀"}