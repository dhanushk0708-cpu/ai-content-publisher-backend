import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.upload import router as upload_router
from app.routers.youtube import router as youtube_router


app = FastAPI(title="AI Content Publisher")


os.makedirs("storage/videos", exist_ok=True)

app.mount(
    "/videos",
    StaticFiles(directory="storage/videos"),
    name="videos",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-content-publisher-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(youtube_router)


@app.get("/")
def home():
    return {"message": "AI Content Publisher Running"}
