from fastapi import FastAPI
from routers import blogs, authentication

app = FastAPI()


app.include_router(blogs.router)
app.include_router(authentication.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Sunil Blog"}