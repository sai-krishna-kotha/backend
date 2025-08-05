# In app/schemas.py

from pydantic import BaseModel, ConfigDict, alias_generators
from datetime import date
from typing import Dict, Any, List

# Pydantic model for the nested 'fields' object.
class WheelSpecFields(BaseModel):
    treadDiameterNew: str
    lastShopIssueSize: str
    condemningDia: str
    wheelGauge: str
    variationSameAxle: str
    variationSameBogie: str
    variationSameCoach: str
    wheelProfile: str
    intermediateWWP: str
    bearingSeatDiameter: str
    rollerBearingOuterDia: str
    rollerBearingBoreDia: str
    rollerBearingWidth: str
    axleBoxHousingBoreDia: str
    wheelDiscWidth: str

# Pydantic model for the incoming POST request body.
class WheelSpecificationCreate(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: WheelSpecFields

# Schemas for specific API responses 

class PostSuccessData(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    status: str = "Saved"

class PostSuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: PostSuccessData

class GetResponseData(BaseModel):
    # These fields are camelCase for the JSON API response
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: Dict[str, Any]

    # This configuration tells Pydantic how to read from our database model.
    model_config = ConfigDict(
        from_attributes=True,  # Allow creating from an object with attributes (like our DB model)
        alias_generator=alias_generators.to_snake, # When looking for 'formNumber', create an alias 'form_number'
        populate_by_name=True, # Allow populating the model by its alias
    )

class GetSuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: List[GetResponseData]