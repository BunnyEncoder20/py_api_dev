from fastapi import FastAPI, status

# routes
from app.routes import post_v1 as post_v1_route
from app.routes import post_v2 as post_v2_route
from app.routes import user as user_v1_route
from app.routes import auth as auth_v1_route
from app.routes import votes as votes_v1_route

# database
# from app.database import Base, engine

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware


'''------------------------------------------------------------------'''


# making FastAPI class instance
app = FastAPI()

# lists of alllowed origins that can reach out backend
allowed_orgins = ['*']

# Adding the CORS middleware to our app
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Commented out because Alembic took over to making PgSQL tables
# Making connection to Postgres DB using SLQ Alchemy
# Base.metadata.create_all(bind=engine)   # needed in main to create tables at server startup


# Generic Path operation (routes)
@app.get("/")
async def root():
    return {"status_code": status.HTTP_200_OK , "msg": "Hellow World"}



# include routers
app.include_router(post_v1_route.router)
app.include_router(post_v2_route.router)
app.include_router(user_v1_route.router)
app.include_router(auth_v1_route.router)
app.include_router(votes_v1_route.router)
