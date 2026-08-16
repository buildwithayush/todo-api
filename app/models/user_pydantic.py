from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
    email:EmailStr

class UserCreate(UserBase):
    password :str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(UserBase):
    id:int
    is_active:bool = True

    class Config:
        from_attributes = True
