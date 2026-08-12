from sqlalchemy import Column,Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column

class TodoDB(Base):
    __tablename__ = "todos" 

    id : Mapped[int] =  mapped_column(Integer, primary_key=True, index=True) 
    title : Mapped[str] = mapped_column(String, nullable=False)             
    description: Mapped[str | None] = mapped_column(String, nullable=True)        
    completed : Mapped[bool] = mapped_column(Boolean, default=False)