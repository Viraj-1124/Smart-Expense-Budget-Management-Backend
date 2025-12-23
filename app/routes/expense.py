from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate,ExpenseResponse
from app.core.security import get_Current_user
from app.models.user import User

router = APIRouter(prefix="/expenses",tags=["Expenses"])

@router.post("/",response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user : User= Depends(get_Current_user)
):
    new_expense = Expense(
        amount = expense.amount,
        category = expense.category,
        description = expense.description,
        date = expense.date,
        user_id = current_user.id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/",response_model=List[ExpenseResponse])
def get_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_Current_user)
):
    return db.query(Expense).filter(Expense.user_id==current_user.id).all()


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user : User =Depends(get_Current_user)
):
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id==current_user.id).first()
    
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}