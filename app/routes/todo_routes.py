from fastapi import APIRouter,HTTPException,status
from typing import List

from app.models.todo import TodoCreate,TodoResponse
from app.data.todos import todos_db

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

# GET ALL TODOS
@router.get("/" ,response_model=List[TodoResponse])
def get_todos():
    return todos_db


# CREATE A NEW TODO
@router.post('/' , response_model=TodoResponse , status_code=status.HTTP_201_CREATED)
def create_todo(todo : TodoCreate):
    new_id = todos_db[-1]["id"] + 1 if todos_db else 1

    new_todo = {
        'id' : new_id,
        'title': todo.title,
        'description': todo.description,
        'completed': False

    }

    todos_db.append(new_todo)
    return new_todo

@router.get('/{todo_id}' ,response_model=TodoResponse)
def get_todos_by_id(todo_id:int):
    for todo in todos_db:
       if todo['id'] == todo_id:
           return todo
    raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Todo with ID {todo_id} not found"
    )


@router.put('/{todo_id}', response_model=TodoResponse)
def update_todo(todo_id: int, todo_data: TodoCreate):
    for todo in todos_db:
        if todo['id'] == todo_id:
            todo['title'] = todo_data.title
            todo['description'] = todo_data.description
            todo['completed'] = todo_data.is_Completed
            return todo

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='TODO NOT FOUND OR UPDATED'
    )

@router.delete('/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id:int):
    for index,todo in enumerate(todos_db) :
        if todo['id'] == todo_id:
            todos_db.pop(index)
            return 
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID {todo_id} not found"
    )
