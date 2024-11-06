from fastapi import FastAPI

from fast_zero import schemas

app = FastAPI()


@app.get("/", response_model=schemas.Message)
def read_root():
    return {"message": "Olar mundo!!"}
