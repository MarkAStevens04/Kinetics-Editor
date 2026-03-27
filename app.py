# This is what's hosting our Python server!
from fastapi import FastAPI

app = FastAPI()

@app.get('/api/health/')
async def root():
    return {"message": "Lookin Healthy!"}