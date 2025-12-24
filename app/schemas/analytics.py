from pydantic import BaseModel

class MonthlySummary(BaseModel):
    month: str
    total_amount : float


class CategorySummary(BaseModel):
    category: str
    total_amount : float