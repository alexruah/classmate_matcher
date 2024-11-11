from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import get_db, Base, engine
from app.api.main import api_router
from app.api.routes import users, classes

app = FastAPI()

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

app.include_router(api_router, dependencies=[Depends(get_db)])

