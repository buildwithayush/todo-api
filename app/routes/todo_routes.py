from fastapi import APIRouter,HTTPException,status,Depends,Query
from sqlalchemy.orm import Session
from typing import List,Optional

from app.models.todo import TodoCreate,TodoResponse,UpdateTodo
from app.models.user_pydantic import UserBase,UserCreate,UserResponse,Token
from app.database import get_db
from app.models.todo_db import TodoDB
from app.models.user_db import UserDB
from app.api.deps import get_current_user



from app.core.security import hash_password,create_access_token,verify_password

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# GET ALL TODOS
@router.get("/" ,response_model=List[TodoResponse])
def get_todos(
   completed:Optional[bool] =Query(None, description='Filter by completed status'),
   skip:int =Query(0, ge=0 ,description='Number of records to skip '),
   limit:int = Query(10,ge=1,le=100 ,description='Number Of records to fetch'),
   db:Session = Depends(get_db)):
    query = db.query(TodoDB)
    if completed is not None:
       query = query.filter(TodoDB.completed == completed)

    todos = query.offset(skip).limit(limit).all()    
    return todos


# CREATE A NEW TODO
@router.post('/' , response_model=TodoResponse , status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = TodoDB(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
    )

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get('/{todo_id}' ,response_model=TodoResponse)
def get_todos_by_id(todo_id:int,db: Session = Depends(get_db)):
     todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
     if not todo:
       raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Todo with ID {todo_id} not found"
    )
     return todo



@router.put('/{todo_id}', response_model=TodoResponse)
def update_todo(todo_id: int, todo_data: TodoCreate, db:Session = Depends(get_db)):
    todo = db.query(TodoDB).filter(TodoDB.id== todo_id).first()
    if not todo:
     raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='TODO NOT FOUND OR UPDATED'
    )
    todo.title = todo_data.title
    todo.description = todo_data.description
    todo.completed = todo_data.completed

    
  
    db.commit()
    db.refresh(todo)
    return todo

@router.delete('/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id:int,db:Session = Depends(get_db)):
   todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
   if not todo:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID {todo_id} not found"
    )

   db.delete(todo) 
   db.commit()

@router.patch('/{todo_id}' ,response_model=TodoResponse)
def update_todo_partial(todo_id:int,todo_data:UpdateTodo,db:Session= Depends(get_db)):
   todo = db.query(TodoDB).filter(TodoDB.id == todo_id).first()
   if not todo:
      raise HTTPException(
         status_code= status.HTTP_404_NOT_FOUND,
         detail=f'todo with {todo_id} not found'
      )
   update_dict = todo_data.model_dump(exclude_unset=True)
   for key,value in update_dict.items():
      setattr(todo,key,value)

   db.commit()
   db.refresh(todo)  
   return todo

@auth_router.post('/signup',response_model=UserResponse ,status_code=status.HTTP_201_CREATED)
def user_signup(user_data:UserCreate,db:Session=Depends(get_db)):
   user = db.query(UserDB).filter(UserDB.email == user_data.email).first()

   if user:
      raise HTTPException(
         status_code=status.HTTP_400_BAD_REQUEST,
         detail=' Email Already Registered'
      )
   hash_pwd = hash_password(user_data.password)

   new_user = UserDB(email=user_data.email, hashed_password=hash_pwd)

   db.add(new_user)
   db.commit()
   db.refresh(new_user)
   return new_user

@auth_router.post('/login',response_model=Token)
def user_login(login_data:UserCreate,db:Session= Depends(get_db)):
   login_user = db.query(UserDB).filter(UserDB.email == login_data.email).first()

   if not login_user or not verify_password(plain_password=login_data.password , hashed_password=login_user.hashed_password):
      raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail='Invalid Credentials'
      )
   access_token = create_access_token(data={"sub": str(login_user.id)})
   return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: UserDB = Depends(get_current_user)):
    
    return current_user  