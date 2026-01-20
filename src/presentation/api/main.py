from fastapi import FastAPI
from src.presentation.api.routes import prices

app = FastAPI(title="Deribit Client API")

app.include_router(prices.router, prefix="/api/prices", tags=["prices"])
