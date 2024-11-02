from fastapi import FastAPI

app = FastAPI()


@app.get("/olamundo")
def read_root():
    return {"message": "Olar mundo!"}
