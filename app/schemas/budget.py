from pydantic import BaseModel

class BudgetCreate(BaseModel):
    month: str
    limit: float


class BudgetResponse(BaseModel):
    month: str
    limit: float

    class Config:
        from_attributes = True
