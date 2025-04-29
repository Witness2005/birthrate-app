from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio
import pandas as pd

from app.data_loader import fetch_csv, DATAFRAME

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
CSV_URL = "https://ourworldindata.org/grapher/crude-birth-rate.csv?v=1&csvType=full&useColumnShortNames=false"
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    df = pd.read_csv(CSV_URL)
    # Tomamos las primeras 100 filas por simplicidad
    data = df.head(100).to_dict(orient="records")
    columns = df.columns.tolist()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "Tasas de Natalidad",
        "data": data,
        "columns": columns
    })
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
