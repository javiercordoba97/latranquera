from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chat import router as chat_router

app = FastAPI()

# Habilitar CORS para permitir llamadas desde el frontend (Vite en puerto 5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Podés restringirlo después
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat")