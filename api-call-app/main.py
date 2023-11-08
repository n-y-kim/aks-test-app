from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel

import requests
import pyodbc

app = FastAPI()
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=<SERVER_NAME>;DATABASE=<DB_NAME>;UID=<USER_NAME>;PWD=<PWD>')

class Item(BaseModel):
    name: str
    email: str

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

@app.get('/callDB')
async def callDB():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data_table')
    rows = cursor.fetchall()
    
    result = []
    for row in rows:
        result.append({'name': row.name, 'email': row.email})
    
    print(result)
    return result

@app.post('/postDB')
async def postDB(item: Item):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO data_table (name, email) VALUES (?, ?)", (item.name, item.email))
    conn.commit()

    return {'status': 'success'}

# Mount the static files directory to the root path
app.mount("/", StaticFiles(directory="static"), name="static")