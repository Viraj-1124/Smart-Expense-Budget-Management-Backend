from fastapi import FastAPI

app = FastAPI(
    title = "Smart Expense Management API",
    description = "Backend API for expense tracking and budgeting",
    version = "1.0.0"
)

@app.get("/")
def root():
    return {"message": "Expense Backend is running"}