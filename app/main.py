from fastapi import FastAPI
from app.database import engine
from app.models import budget,user,expense
from app.database import Base

app = FastAPI(
    title = "Smart Expense Management API",
    description = "Backend API for expense tracking and budgeting",
    version = "1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Expense Backend is running"}