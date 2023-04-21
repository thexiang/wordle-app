from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wordle.apis.game_api import game
from wordle.config import wordle_settings


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(game)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = create_application()


@app.get("/ping")
def pong():
    return {
        "ping": "pong!",
        "environment": wordle_settings.environment,
    }
