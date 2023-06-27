from fastapi import FastAPI

app = FastAPI()

#Write a simple GET method that returns 'Hello World' text
@app.get("/")
def root_get():
    return {"message": "Hello World"}