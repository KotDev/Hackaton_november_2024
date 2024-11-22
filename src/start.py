from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

from database import BaseManager, DataBase
from middlewares import JWTMiddleware
from authorization.controllers.auth_controllers import auth_router
import logging
from middlewares import PrometheusMiddleware
from database import Base
from authorization.models.model import User
from profile.models.model import Profile, Photo
from profile.controllers.profile_conrollers import profile_router


LOG_COUNT: Counter = Counter(
    "log_messages_total",
    "Total number of log messages",
    ["log_level"]
)

class PrometheusLoggingHandler(logging.Handler):
    def emit(self, record):
        log_level = record.levelname.lower()
        LOG_COUNT.labels(log_level=log_level).inc()


db = DataBase()
base_manager = BaseManager(base=Base)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await base_manager.init_models()
    yield
    await base_manager.clear_models()


app = FastAPI(lifespan=lifespan)
app.add_middleware(JWTMiddleware)
app.add_middleware(PrometheusMiddleware)
app.include_router(auth_router)
app.include_router(profile_router)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(PrometheusLoggingHandler())

@app.get("/custom_metrics")
async def custom_metrics():
    metrics = generate_latest()
    return Response(content=metrics, media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)