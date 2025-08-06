from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
from .. import models, schemas, crud 
from ..database import get_db

router = APIRouter(
    prefix="/api/forms/wheel-specifications",
    tags=["Wheel Specifications"]
)

@router.post(
    "/",
    response_model=schemas.PostSuccessResponse,
    status_code=status.HTTP_201_CREATED
)
def create_wheel_spec_form(spec: schemas.WheelSpecificationCreate, db: Session = Depends(get_db)):
    """Handles the POST request to create a new wheel specification form."""
    existing_spec = crud.get_wheel_specifications(db, form_number=spec.formNumber, submitted_by=None, submitted_date=None)
    if existing_spec:
        raise HTTPException(status_code=400, detail=f"Form with number '{spec.formNumber}' already exists.")

    new_spec = crud.create_wheel_specification(db=db, spec=spec)

    response_data = schemas.PostSuccessData(
        formNumber=new_spec.form_number,
        submittedBy=new_spec.submitted_by,
        submittedDate=new_spec.submitted_date,
    )
    return schemas.PostSuccessResponse(
        message="Wheel specification submitted successfully.",
        data=response_data
    )


@router.get(
    "/",
    response_model=schemas.GetSuccessResponse
)
def read_wheel_spec_forms(
    formNumber: Optional[str] = None,
    submittedBy: Optional[str] = None,
    submittedDate: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Handles the GET request to find wheel specification forms using filters."""
    specs_from_db = crud.get_wheel_specifications(db, form_number=formNumber, submitted_by=submittedBy, submitted_date=submittedDate)
    
    if not specs_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No wheel specification forms found with the given filters."
        )
    return schemas.GetSuccessResponse(
        message="Filtered wheel specification forms fetched successfully.",
        data=specs_from_db
    )