import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database.db_helper import DataBase
from app.routes.auth import router as router_auth
from app.routes.basket import router as router_basket
from app.routes.admin import router as router_admin
from app.routes.rabbitmq import router as router_rabbitmq


logger = logging.getLogger()
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Запуск сервера")
    app.state.db_helper = DataBase()
    logging.info("База готова к работе")
    yield
    logging.info("Выключение")
    app.state.db_helper.client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router_auth)
app.include_router(router_basket)
app.include_router(router_admin)
app.include_router(router_rabbitmq)

