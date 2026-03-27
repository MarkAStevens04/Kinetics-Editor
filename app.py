# This is what's hosting our Python server!
from fastapi import FastAPI
from pydantic import BaseModel
from source.base_simulation import Simulation

# Define required schema for our API requests
class SpeciesSchema(BaseModel):
    id: str
    initial: float

class ReactionSchema(BaseModel):
    id: str
    Reactants: list[str]
    Products: list[str]
    rate_law: str
    Parameters: dict[str, float]

class SimulationSchema(BaseModel):
    t_end: float
    dt: float
    method: str

class PayloadSchema(BaseModel):
    Species: list[SpeciesSchema]
    Reactions: list[ReactionSchema]
    Simulation: SimulationSchema

app = FastAPI()

@app.get('/api/health')
async def root():
    return {"message": "Lookin Healthy!"}


@app.post('/api/simulate')
async def run_simulation(payload: PayloadSchema):
    json_payload = payload.model_dump_json()
    sim = Simulation()
    sim.initialize_simulation(json_payload)

    return {'message': 'successfully ran simulation'}

    # return payload

