from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

# Import our other local files
from . import models, schemas
from .database import engine, get_db

# Create the database tables if they don't already exist
models.Base.metadata.create_all(bind=engine)

# Create our main FastAPI application
app = FastAPI(
    title="KPA Form Data API",
    description="Backend API for KPA form submissions.",
    version="1.0.0"
)

# Add CORS middleware to allow our frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Functions 
# For a project of this size, keeping these functions here is clean and simple.

def create_wheel_specification_in_db(db: Session, spec: schemas.WheelSpecificationCreate):
    """Saves a wheel specification form to the database."""
    db_spec = models.WheelSpecification(
        form_number=spec.formNumber,
        submitted_by=spec.submittedBy,
        submitted_date=spec.submittedDate,
        fields=spec.fields.model_dump()
    )
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return db_spec

def get_wheel_specifications_from_db(db: Session, form_number: Optional[str], submitted_by: Optional[str], submitted_date: Optional[date]):
    """Gets wheel specification forms from the database, with optional filters."""
    query = db.query(models.WheelSpecification)
    if form_number:
        query = query.filter(models.WheelSpecification.form_number == form_number)
    if submitted_by:
        query = query.filter(models.WheelSpecification.submitted_by == submitted_by)
    if submitted_date:
        query = query.filter(models.WheelSpecification.submitted_date == submitted_date)
    return query.all()


# API Endpoints 

@app.get("/", tags=["Root"])
def read_root():
    """A default root endpoint to show that the API is running."""
    return {"message": "Welcome to the KPA Form Data API"}

@app.post(
    "/api/forms/wheel-specifications",
    response_model=schemas.PostSuccessResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Wheel Specifications"]
)
def create_wheel_spec_form(spec: schemas.WheelSpecificationCreate, db: Session = Depends(get_db)):
    """Handles the POST request to create a new wheel specification form."""
    # First, check if a form with this number already exists to avoid duplicates.
    existing_spec = get_wheel_specifications_from_db(db, form_number=spec.formNumber, submitted_by=None, submitted_date=None)
    if existing_spec:
        raise HTTPException(status_code=400, detail=f"Form with number '{spec.formNumber}' already exists.")

    # If it's new, save it to the database.
    new_spec = create_wheel_specification_in_db(db=db, spec=spec)

    # Prepare and return a successful response.
    response_data = schemas.PostSuccessData(
        formNumber=new_spec.form_number,
        submittedBy=new_spec.submitted_by,
        submittedDate=new_spec.submitted_date,
    )
    return schemas.PostSuccessResponse(
        message="Wheel specification submitted successfully.",
        data=response_data
    )

@app.get(
    "/api/forms/wheel-specifications",
    response_model=schemas.GetSuccessResponse,
    tags=["Wheel Specifications"]
)
def read_wheel_spec_forms(
    formNumber: Optional[str] = None,
    submittedBy: Optional[str] = None,
    submittedDate: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Handles the GET request to find wheel specification forms using filters."""
    # Get the forms from the database using our filter function.
    specs_from_db = get_wheel_specifications_from_db(db, form_number=formNumber, submitted_by=submittedBy, submitted_date=submittedDate)
    
    # Return the results in the correct format.
    # Pydantic automatically converts our database objects to the response model.
    return schemas.GetSuccessResponse(
        message="Filtered wheel specification forms fetched successfully.",
        data=specs_from_db
    )