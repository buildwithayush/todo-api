from fastapi import FastAPI
from app.database import engine,Base
from app.routes.todo_routes import router as todo_router
from app.routes.todo_routes import auth_router as todo_auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title='Todo APi',
    version='1.0.0'
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_methods=["*"],            
    allow_headers=["*"],         
)

app.include_router(todo_router, prefix='/api/v1')
app.include_router(todo_auth_router ,prefix="/api/v1")

@app.get('/')
def root():
    return {'message': 'Server is running smoothly'}