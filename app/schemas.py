from pydantic import BaseModel
from datetime import date
from typing import Dict, Any, List, Optional

class WheelSpecFields(BaseModel):
    treadDiameterNew: str
    lastShopIssueSize: str
    condemningDia: str
    wheelGauge: str
    variationSameAxle: float
    variationSameBogie: int
    variationSameCoach: int
    wheelProfile: str
    intermediateWWP: str
    bearingSeatDiameter: str
    rollerBearingBoreDia: str
    rollerBearingOuterDia: str
    rollerBearingWidth: str
    axleBoxHousingBoreDia: str
    wheelDiscWidth: str

class WheelSpecificationCreate(BaseModel):
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: WheelSpecFields

class WheelSpecificationInDB(BaseModel):
    id: int
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: Dict[str, Any]

    class Config:
        from_attributes = True 

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
    formNumber: str
    submittedBy: str
    submittedDate: date
    fields: Dict[str, Any]

class GetSuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: List[GetResponseData]


# class DummyLoginRequest(BaseModel):
#     phoneNumber: str
#     password: str

# class DummyLoginResponseData(BaseModel):
#     user_id: str = "dummy_user_123"
#     token: str = "dummy_jwt_token_for_testing"
#     message: str = "Login successful"

# class DummyLoginSuccessResponse(BaseModel):
#     success: bool = True
#     data: DummyLoginResponseData