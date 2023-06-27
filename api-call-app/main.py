from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import requests

app = FastAPI()

@app.get("/")
def home():
    #Return static file
    return FileResponse('static/index.html')

@app.get("/callapi")
def callapi():
    response = requests.get('https://external-api-backend-test.azurewebsites.net/')
    print(response)
    data = response.json()
    
    apiValue = data['message']
    
    return apiValue

# Mount the static files directory to the root path
app.mount("/", StaticFiles(directory="static"), name="static")