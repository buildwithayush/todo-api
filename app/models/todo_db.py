from sqlalchemy import Integer, String, Boolean,ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship

class TodoDB(Base):
    __tablename__ = "todos" 

    id : Mapped[int] =  mapped_column(Integer, primary_key=True, index=True) 
    title : Mapped[str] = mapped_column(String, nullable=False)             
    description: Mapped[str | None] = mapped_column(String, nullable=True)        
    completed : Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False)

    owner = relationship("UserDB", backref="todos")