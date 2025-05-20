from fastapi import FastAPI

app = FastAPI()

# Path operation (routes)
@app.get("/")
async def root():
    return {"message": "Hello World"}