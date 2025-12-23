from fastapi import FastAPI
from app.database import engine, Base
from app.routes import auth
from app.routes import expense as exp
from app.models import budget,user,expense
from app.database import Base

app = FastAPI(
    title = "Smart Expense Management API",
    description = "Backend API for expense tracking and budgeting",
    version = "1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(exp.router)

@app.get("/")
def root():
    return {"message": "Expense Backend is running"}