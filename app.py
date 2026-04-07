# This is what's hosting our Python server!
import io
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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


class ReturnSpecies(BaseModel):
    results: dict[str, list[float]]

# Define our app
app = FastAPI()

allowed_origins = [
    "http://localhost:5173", # Vite
    "http://kinetics-editor.vercel.app", # Our vercel app
    "http://biobuilder.app", # Main domain
    "https://biobuilder.app", # Another secure domain
    "https://www.biobuilder.app", # Secure main domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
    allow_headers=['Content-Type', 'Authorization']
)

@app.get('/api/health')
async def root():
    return {"message": "Lookin Healthy!"}


@app.post('/api/simulate/v02')
async def run_simulation(payload: PayloadSchema) -> ReturnSpecies:

    # Put our simulation in JSON format
    json_payload = payload.model_dump(mode='json')

    # Run our simulation
    sim = Simulation()
    sim.initialize_simulation(json_payload)

    return_json = sim.get_json_solution()

    # Return this JSON
    return return_json