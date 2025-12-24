from fastapi import APIRouter,Depends,Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from typing import List

from app.database import get_db
from app.core.security import get_Current_user
from app.models.expense import Expense
from app.models.user import User
from app.schemas.analytics import MonthlySummary,CategorySummary

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/monthly",response_model=List[MonthlySummary])
def monthly_summary(
    db:Session = Depends(get_db),
    user: User = Depends(get_Current_user)
):
    result = (
        db.query(
            func.strftime("%Y-%m",Expense.date).label("month"),
            func.sum(Expense.amount).label("total_amount")
        )
        .filter(Expense.user_id == user.id)
        .group_by("month")
        .order_by("month")
        .all()
    )
    return result


@router.get("/category", response_model=List[CategorySummary])
def category_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_Current_user)
):
    result = (
        db.query(
            Expense.category,
            func.sum(Expense.amount).label("total_amount")
        )
        .filter(Expense.user_id == user.id)
        .group_by(Expense.category)
        .all()
    )
    return result


@router.get("/range")
def expense_range(
    start_date: date = Query(...),
    last_date: date = Query(...),
    db:Session = Depends(get_db),
    user:User = Depends(get_Current_user)
):
    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user.id,
            Expense.date >= start_date,
            Expense.date <= last_date
        )
        .all()
    )

    total = sum(e.amount for e in expenses)
    return {
        "start_date": start_date,
        "end_date": last_date,
        "total_expense": total,
        "count": len(expenses),
        "expenses": expenses
    }