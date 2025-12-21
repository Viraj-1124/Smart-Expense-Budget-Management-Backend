from sqlalchemy import Integer,Column,String,Float,ForeignKey
from app.database import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer,primary_key=True,index=True)
    month = Column(String,index=False)
    limit = Column(Float,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"))