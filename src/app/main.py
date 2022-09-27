import copy
import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.api import v1
from app.models import *  # noqa: F401
from app.settings import Settings, settings


def create_app(conf: Settings) -> FastAPI:
    app = FastAPI()

    configure_logging(conf)
    add_middlewares(app, conf)
    include_routers(app, conf)

    return app


def configure_logging(conf: Settings) -> None:
    log_conf = copy.deepcopy(conf.LOGGING_CONFIG)

    if "handlers" in log_conf:
        sinks = {
            "sys.stderr": sys.stderr,
            "sys.stdout": sys.stdout,
        }
        for h in log_conf["handlers"]:
            h["sink"] = sinks.get(h["sink"], h["sink"])

    logger.configure(**log_conf)


def add_middlewares(app: FastAPI, conf: Settings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def include_routers(app: FastAPI, conf: Settings) -> None:
    app.include_router(v1.router, prefix=conf.API_PREFIX)


app = create_app(settings)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, debug=True)
