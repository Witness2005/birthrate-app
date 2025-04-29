import pandas as pd
import aiohttp
import io
from datetime import datetime

CSV_URL = "https://ourworldindata.org/grapher/crude-birth-rate.csv?v=1&csvType=full&useColumnShortNames=false"
DATAFRAME = None
LAST_UPDATE = None

async def fetch_csv():
    global DATAFRAME, LAST_UPDATE
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(CSV_URL) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    DATAFRAME = pd.read_csv(io.BytesIO(content))
                    LAST_UPDATE = datetime.now()
                    print(f"Datos cargados correctamente. Registros: {len(DATAFRAME)}")
                else:
                    print(f"Error HTTP: {resp.status}")
                    # Mantener los datos anteriores si existen
                    if DATAFRAME is None:
                        DATAFRAME = pd.DataFrame()
    except Exception as e:
        print(f"Error crítico: {str(e)}")
        if DATAFRAME is None:
            DATAFRAME = pd.DataFrame()