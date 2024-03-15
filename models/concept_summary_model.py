from pydantic import BaseModel, ValidationError

class ConceptSummaryModel(BaseModel):
    """Data Model for summarizing evidences"""
    AllEvidenceSummary: str
    AllEvidenceFeedback: str