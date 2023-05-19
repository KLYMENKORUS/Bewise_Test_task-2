import uvicorn
from fastapi import FastAPI
from api.urls import router


app = FastAPI(title='Task #2',
              description='Test tasks for bewise.ai')


app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

