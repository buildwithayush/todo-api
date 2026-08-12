from pydantic import Field,BaseModel
from typing import Optional

class TodoBase(BaseModel):
    title :str = Field(...,min_length=1,max_length=100,description='Todo Title')
    description : Optional[str] = Field(None,max_length=300,description='Todo Description')
    completed: bool = Field(default=False)

class TodoCreate(TodoBase):
    pass

class UpdateTodo(BaseModel):
    title:Optional[str] = Field(None, min_length=3, max_length=100)
    description : Optional[str] = Field(None, max_length=300)
    completed : Optional[bool] = Field(None)

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool

    class Config:
        from_attributes = True