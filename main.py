from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
import schemas
import utils
# from .schemas import Post,PostCreate,UserCreate,UserOut
from  database import engine,sessionmaker,SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import List
from routers import posts,users,auth
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

app.include_router(posts.router)

app.include_router(users.router)

app.include_router(auth.router)














