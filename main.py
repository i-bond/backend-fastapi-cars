import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.users import users_router
from routers.cars import cars_router
from routers.newsletters import newsletter_router
from database.db_worker import connect_db
from fastapi.staticfiles import StaticFiles
from decouple import config


app = FastAPI(title='Cars API')
app.mount("/static", StaticFiles(directory="static"), name="static")
APP_HOST = config('APP_HOST', default='127.0.0.1', cast=str)


@app.get('/')
async def home():
    return {'title': 'Hello Coder!'}


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    '''Connect to MongoDB'''
    await connect_db()


@app.on_event("shutdown")
async def shutdown_db_client():
    '''Shut down MongoDB connection'''



app.include_router(users_router)
app.include_router(cars_router)
app.include_router(newsletter_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=8000, reload=True)

