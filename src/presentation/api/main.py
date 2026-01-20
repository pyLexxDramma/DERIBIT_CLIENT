from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.database.connection import Database
from src.presentation.api.routes import prices

_db_instance = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _db_instance.connect()
    yield
    await _db_instance.close()


app = FastAPI(title="Deribit Client API", lifespan=lifespan)
app.state.db = _db_instance

app.include_router(prices.router, prefix="/api/prices", tags=["prices"])
