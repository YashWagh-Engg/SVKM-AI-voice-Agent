# SVKM Information Desk - Backend

FastAPI backend for the SVKM Information Desk AI voice assistant.

## Features
- SVKM university information
- Engineering program information
- Commerce program information
- Pharmacy program information
- Program intake information
- Eligibility information
- Facilities and campus information
- Multilingual response support
- Deterministic backend responses

## Run locally

`ash
uvicorn app.main:app --reload
`"
"


### Health Check
GET /health

### Chat
POST /api/chat

Example request:

`json
{
  "message": "How many seats are there in Computer Engineering?"
}
`"
"


Phone / ElevenLabs Agent
→ FastAPI
→ Intent Detection
→ SVKM Knowledge Base
→ Approved Response
→ ElevenLabs Voice
