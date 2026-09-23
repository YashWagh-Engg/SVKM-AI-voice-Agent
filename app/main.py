from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.intent import detect_intent
from app.services.response import get_response
from app.services.language import detect_language
from app.services.session import (
    create_session,
    add_message,
    get_session
)

app = FastAPI(
    title="College AI Calling Agent",
    description="Deterministic multilingual AI calling agent for SVKM NMIMS Global University",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {
        "message": "College AI Calling Agent API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0"
    }


@app.post("/api/chat")
def chat(request: ChatRequest):

    # Detect language automatically if caller does not provide it
    language = detect_language(request.message)

    # Detect user's intent
    intent = detect_intent(request.message)

    # Get deterministic approved response
    response = get_response(
    intent=intent,
    language=language,
    message=request.message
)
    return {
        "message": request.message,
        "language": language,
        "intent": intent,
        "response": response
    }
@app.post("/api/session")
def start_session():

    session_id = create_session()

    return {
        "session_id": session_id,
        "message": "Session created successfully"
    }


@app.post("/api/session/{session_id}/message")
def session_message(session_id: str, request: ChatRequest):

    session = get_session(session_id)

    if session is None:
        return {
            "error": "Session not found"
        }

    language = detect_language(request.message)

    intent = detect_intent(request.message)

    response = get_response(
    intent=intent,
    language=language,
    message=request.message
)

    # Store user message
    add_message(
        session_id,
        "user",
        request.message
    )

    # Store assistant response
    add_message(
        session_id,
        "assistant",
        response
    )

    return {
        "session_id": session_id,
        "language": language,
        "intent": intent,
        "response": response,
        "message_count": len(session["messages"])
    }


@app.get("/api/session/{session_id}")
def conversation_history(session_id: str):

    session = get_session(session_id)

    if session is None:
        return {
            "error": "Session not found"
        }

    return {
        "session_id": session_id,
        "messages": session["messages"],
        "message_count": len(session["messages"])
    }