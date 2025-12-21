from sqlalchemy import Column,Integer,String,Float,ForeignKey,Date
from app.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float,nullable=False)
    category = Column(String,index=True)
    description = Column(String)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))