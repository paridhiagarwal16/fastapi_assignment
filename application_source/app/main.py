import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from app.routers import books,user,login,reviews
from app.database import engine, Base
app = FastAPI(
    title="FastAPI Project Jksoft",
    description='Get details for all books',
    contact={
        "Developer Name": "Paridhi Agarwal",
        "email": "paridhiagarwal16@gmail.com",
    }
)

@app.on_event("startup")
async def on_startup():
    print("engine startup")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def on_shutdown():
    print("engine shutdown")
    await engine.dispose()

app.include_router(books.router)
app.include_router(reviews.router)
app.include_router(user.router)
app.include_router(login.router)

@app.post("/check")
async def index():
    return {"message": "Hello World"}



# uvicorn.run(app, host='localhost', port=8080)
if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)