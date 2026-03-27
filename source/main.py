# This is what's hosting our Python server!
from fastapi import FastAPI

app = FastAPI()

@app.get('/health/')
async def root():
    return {"message": "Lookin Healthy!"}