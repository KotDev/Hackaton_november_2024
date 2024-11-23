from contextlib import asynccontextmanager

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
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
from profile.models.model import Profile, Photo, BuisnessForm
from ml.models.models import BuisnessSupport, News, Tag
from apscheduler.triggers.cron import CronTrigger
from pars_news import run_parsing_news
from pars_support_buisnes import run_parsing_support_business
from profile.controllers.profile_conrollers import profile_router
from ml.controllers.news_controllers import router_news
from ml.controllers.supprot_business_controllers import router_support_business
from ml.logic.news_logic import NewsLogic
from ml.logic.support_business_logic import BusinessSupportLogic
from profile.controllers.buisness_form_controllers import business_form_router


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
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):

    await base_manager.init_models()
    data_news = await run_parsing_news()
    await NewsLogic.format_parse_data(parse_data=data_news)
    data_support = await run_parsing_support_business()
    await BusinessSupportLogic.format_data_parser(data_support)
    #scheduler.add_job(
    #    run_parsing_news,
    #    CronTrigger(hour=3, minute=0),  # Ежедневно в 03:00
    #    id="daily_parser_news",
    #    replace_existing=True,
    #)
    #scheduler.add_job(
    #    run_parsing_support_business,
    #    CronTrigger(hour=4, minute=0),
    #    id="daily_parser_support_business",
    #    replace_existing=True,
    #)
    scheduler.start()
    yield
    scheduler.shutdown()
    await base_manager.clear_models()


app = FastAPI(lifespan=lifespan)
app.add_middleware(JWTMiddleware)
app.add_middleware(PrometheusMiddleware)
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(router_news)
app.include_router(business_form_router)
app.include_router(router_support_business)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(PrometheusLoggingHandler())

@app.get("/custom_metrics")
async def custom_metrics():
    metrics = generate_latest()
    return Response(content=metrics, media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)