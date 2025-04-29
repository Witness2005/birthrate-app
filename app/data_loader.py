import pandas as pd
import aiohttp
import io

CSV_URL = "https://ourworldindata.org/grapher/crude-birth-rate.csv?v=1&csvType=full&useColumnShortNames=false"
DATAFRAME = pd.DataFrame()

async def fetch_csv():
    global DATAFRAME
    async with aiohttp.ClientSession() as session:
        async with session.get(CSV_URL) as resp:
            if resp.status == 200:
                content = await resp.read()
                print(f"Contenido descargado, tamaño: {len(content)} bytes")  # Imprime el tamaño del contenido descargado
                try:
                    df = pd.read_csv(io.BytesIO(content))
                    DATAFRAME = df
                    print(f"Datos cargados correctamente, tamaño del DataFrame: {len(DATAFRAME)}")  # Imprime el tamaño del DataFrame
                except Exception as e:
                    print(f"Error al procesar los datos CSV: {e}")
            else:
                print(f"Error al descargar datos: {resp.status}")
