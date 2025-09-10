from fastapi import FastAPI
from app.routers import userRouter, articleRouter

app = FastAPI()

## inclusion des routes dans le main
app.include_router(userRouter.router)
app.include_router(articleRouter.router)


@app.get("/")
async def root():
  return {"message": "Bonjour Ali !"}

