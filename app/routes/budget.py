from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.core.security import get_Current_user
from app.models.budget import Budget
from app.models.expense import Expense
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetResponse

router = APIRouter(prefix="/budget", tags=["Budget"])

@router.post("/",response_model=BudgetResponse)
def set_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_Current_user)
):
    existing_budget = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.month == budget.month
    ).first()

    if existing_budget:
        existing_budget.limit = budget.limit
        db.commit() 
        db.refresh(existing_budget)
        return existing_budget
    
    new_budget = Budget(
        month = budget.month,
        limit = budget.limit,
        user_id = current_user.id
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget


@router.get("/{month}")
def get_budget_status(
    month:str,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_Current_user)
):
    budget = db.query(Budget).filter(
        Budget.user_id ==current_user.id,
        Budget.month == month
    ).first()

    if not budget:
        raise HTTPException(status_code=404, detail="Budget not set for this month")
    
    total_spent = (
        db.query(func.sum(Expense.amount))
        .filter(
            Expense.user_id == current_user.id,
            func.strftime("%Y-%m",Expense.date)
        )
        .scalar()
    ) or 0.0

    overspent = total_spent > budget.limit

    return{
        "month": month,
        "budget_limit": budget.limit,
        "total_spent": total_spent,
        "remaining": budget.limit - total_spent,
        "Overspent": overspent,
        "alert": "Budget exceeded!" if overspent else "Within budget"
    }