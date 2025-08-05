from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import schemas
from .database import engine, Base
from .routers import wheel_specs

Base.metadata.create_all(bind=engine)

app = FastAPI()

# @app.post(
#     "/api/user/login",
#     response_model=schemas.DummyLoginSuccessResponse,
#     tags=["Dummy Auth"]
# )
# def dummy_user_login(request: schemas.DummyLoginRequest):
#     print(f"Dummy login attempt for user: {request.phoneNumber}")
#     return schemas.DummyLoginSuccessResponse(
#         data=schemas.DummyLoginResponseData()
#     )

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
    return {"message": "Welcome to the KPA Form Data API"}



