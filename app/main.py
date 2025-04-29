from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio

from app.data_loader import fetch_csv, DATAFRAME

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    await fetch_csv()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    df = DATAFRAME.head(100)  # Mostrar solo los primeros 100 registros
    table_html = df.to_html(classes="table table-striped", index=False)
    return templates.TemplateResponse("index.html", {"request": request, "table": table_html})

@app.get("/refresh")
async def refresh_data():
    await fetch_csv()
    return {"message": "Datos actualizados correctamente"}
