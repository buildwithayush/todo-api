from fastapi import FastAPI
from app.routes.todo_routes import router as todo_router

app = FastAPI(
    title='Todo APi',
    version='1.0.0'
)

app.include_router(todo_router, prefix='/api/v1')

@app.get('/')
def root():
    return {'message': 'Server is running smoothly'}