[![N|Solid](source/assets/Engine_Banner.png)](https://kinetics-editor.vercel.app/)

<div align="center">

[![N|Solid](https://img.shields.io/website?url=https%3A%2F%2Fbiobuilder.app%2F&label=frontend)](https://biobuilder.app/)
[![N|Solid](https://img.shields.io/website?url=https%3A%2F%2Fkinetics-editor.vercel.app%2Fapi%2Fhealth&label=backend&cacheSeconds=600)](https://kinetics-editor.vercel.app/api/health)
[![N|Solid](https://img.shields.io/badge/github-frontend-blue?logo=github)](https://github.com/MarkAStevens04/cloudflare-kinetics-editor)

[![N|Solid](https://badgen.net/badge/icon/discord?icon=discord&label)](https://discord.gg/GmsKryYDGN) 
[![N|Solid](https://img.shields.io/badge/-mark@biobuilder.app-blue?logo=gmail&label=Email)](mailto:mark@biobuilder.app)

[![N|Solid](https://img.shields.io/badge/Give%20us%20feedback!!-magenta
)](https://tally.so/r/VLYDpa)

</div>


# Overview

Project for PHY426 Course! Web-Based Biochemical kinetics editor.

**Backend Simulation** Engine for BioBuilder.

This is the repo for the BACKEND for the BioBuilder App (built for PHY426). The frontend is accessible [HERE](https://github.com/MarkAStevens04/cloudflare-kinetics-editor).

# Get Started
1) run `pip install -r requirements.txt`
2) run `fastapi dev`
3) Go on a web browser and go to the website `localhost:8000/api/health`

You can view docs at: localhost:8000/docs

### Check if API calls are working
curl -d "{ 'Species': [], 'Reactions': [], 'Simulation': {'t_end': 300, 'dt': 1, 'method': 'Euler'}}" -X POST localhost:8000/api/simulate

curl -X GET localhost:8000/api/health

curl -X 'POST' 'localhost:8000/api/simulate' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{ "Species": [{"id": "string", "initial": 0 }], "Reactions": [{"id": "string", "Reactants": ["string"], "Products": ["string"], "rate_law": "string", "Parameters": { "additionalProp1": 0, "additionalProp2": 0, "additionalProp3": 0 } }], "Simulation": {"t_end": 0, "dt": 0, "method": "string"}}'


# Ideas
### Connect to enzyme databases
From uniprot https://www.uniprot.org/uniprotkb/P00724/entry
Go to Brenda Database https://www.brenda-enzymes.org/enzyme.php?ecno=3.2.1.26&UniProtAcc=P00724&OrganismID=984 (Look for Km values)
Or SabioRK Database

Look at enzyme in diff conditions, extrapolate some relation between them?
