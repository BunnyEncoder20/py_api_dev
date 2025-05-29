from fastapi import FastAPI, status

# routes
from app.routes import post_v1 as postv1_route          
from app.routes import post_v2 as postv2_route          
from app.routes import user as userv1_route
from app.routes import auth as authv1_route
           
# models
from app.models import post as post_model
from app.models import user as user_model

# database
from app.database import Base, engine       

'''------------------------------------------------------------------'''


# making FastAPI class instance
app = FastAPI()

# Making connection to Postgres DB using SLQ Alchemy
Base.metadata.create_all(bind=engine)   # needed in main to create tables at server startup


# Generic Path operation (routes)
@app.get("/")
async def root():
    return {"status_code": status.HTTP_200_OK , "msg": "Hellow World"}



# include routers
app.include_router(postv1_route.router)
app.include_router(postv2_route.router)
app.include_router(userv1_route.router)
app.include_router(authv1_route.router)