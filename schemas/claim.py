from pydantic import BaseModel, Field
from typing import List


class InsuranceClaim(BaseModel):

    claim_id: str

    customer_name: str

    claim_amount: float = Field(gt=0)

    policy_amount: float = Field(gt=0)

    policy_active: bool

    documents: List[str]

    required_documents: List[str]

    incident_description: str