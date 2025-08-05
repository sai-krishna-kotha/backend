from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.post(
    "/",
    response_model=schemas.PostSuccessResponse,
    status_code=status.HTTP_201_CREATED
)
def create_wheel_spec_form(
    spec: schemas.WheelSpecificationCreate, 
    db: Session = Depends(get_db)
):
    existing_spec = crud.get_wheel_specifications(
        db, 
        form_number=spec.formNumber, 
        submitted_by=None, 
        submitted_date=None
    )
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
    formNumber: Optional[str] = Query(default=None),
    submittedBy: Optional[str] = Query(default=None),
    submittedDate: Optional[date] = Query(default=None),
    db: Session = Depends(get_db)
):
    
    specs_from_db = crud.get_wheel_specifications(db, form_number=formNumber, submitted_by=submittedBy, submitted_date=submittedDate)
    
    response_data_list = []
    for spec in specs_from_db:
        response_data_list.append(
            schemas.GetResponseData(
                formNumber=spec.form_number,
                submittedBy=spec.submitted_by,
                submittedDate=spec.submitted_date,
                fields=spec.fields
            )
        )

    return schemas.GetSuccessResponse(
        message="Filtered wheel specification forms fetched successfully.",
        data=response_data_list
    )