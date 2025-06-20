from fastapi import FastAPI
from app.api.v1 import libraries

app = FastAPI()

app.include_router(libraries.router, prefix="/v1/libraries", tags=["libraries"])

@app.get("/")
def read_root():
    return {"message": "Vector DB API is running. Add /docs to access the Swagger UI."}
