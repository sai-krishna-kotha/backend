from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import wheel_specs

# Create the database tables if they don't already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KPA Form Data API",
    description="Backend API for KPA form submissions.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wheel_specs.router)

@app.get("/", tags=["Root"])
def read_root():
    """A default root endpoint to show that the API is running."""
    return {"message": "Welcome to the KPA Form Data API"}