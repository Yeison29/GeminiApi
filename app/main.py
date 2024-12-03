from fastapi import FastAPI
from app.gemini.gemeni import Gemini
from app.schema.prompt import RequestBodyPrompt
from fastapi.middleware.cors import CORSMiddleware
import os
from app.config.db import create_db

app = FastAPI()
port = int(os.getenv("PORT", 8000))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Bienvenido al sistema"}


@app.post("/gemini/prompt")
async def gemini_pront(request: RequestBodyPrompt):
    response = await Gemini().gemini_response(request)
    return response


@app.post("/gemini/chat")
async def gemini_chat(request: str):
    response = await Gemini().gemini_chat(request)
    return response


@app.get("/gemini/clear-chat")
async def gemini_clear_chat():
    response = await Gemini().gemini_clear_chat()
    return response
