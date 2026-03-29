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

# Define our app
app = FastAPI()

allowed_origins = [
    "http://localhost:5173", # Vite
    "http://kinetics-editor.vercel.app", # Our vercel app
    "http://biobuilder.app", # Main domain
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


@app.post('/api/simulate', response_class=StreamingResponse)
async def run_simulation(payload: PayloadSchema):
    import matplotlib.pyplot as plt

    json_payload = payload.model_dump(mode='json')
    sim = Simulation()
    sim.initialize_simulation(json_payload)

    # Plot our result!
    y = sim.solution.y

    plt.plot(sim.t_eval, y.T)
    plt.xlabel('time')
    plt.ylabel('concentration')

    # Create sorted list of labels
    labels = [name for name, idx in sorted(sim.species_map.items(), key=lambda item: item[1])]
    plt.legend(labels, shadow=True)
    plt.savefig('fake_graph.png')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')

    # Seek beginning of buffer
    buf.seek(0)

    # plt.savefig('current_graph.png')

    return StreamingResponse(buf, media_type="image/png")

    # return {'message': 'successfully ran simulation'}

    # return payload

