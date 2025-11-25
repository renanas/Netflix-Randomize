from fastapi import FastAPI

app = FastAPI(
    title="Netflix Clone API",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "Welcome to the Netflix Clone API!"}