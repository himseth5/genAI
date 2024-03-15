from pydantic import BaseModel, ValidationError
from datetime import datetime

class PatientModel(BaseModel):
    """Data model for the Patient Details"""
    Patient_Name: str
    Patient_Gender: str
    Patient_DoB: datetime
    Patient_Address_line: str
    Patient_State: str
    Patient_Contact: str

class ProviderModel(BaseModel):
    """Data model for the Patient Details"""
    Provider_Name: str
    Provider_Address_line: str
    Provider_State: str
    Provider_Contact: str

