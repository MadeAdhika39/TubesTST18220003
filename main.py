import uvicorn
from fastapi import FastAPI
from routes.motorRoutes import motor_router
from routes.userRoutes import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(motor_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

