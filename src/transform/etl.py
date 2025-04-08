#Importamos las librerias necesarias para el etl.
import pandas as pd
import os
from pathlib import Path

#Cargamos el archivo csv en un dataframe de pandas.

import pandas as pd

# Obtener la ruta del archivo .py
current_dir = Path(__file__).resolve().parent

# Construir la ruta relativa al archivo CSV
csv_path = current_dir.parents[1] / 'data' / 'raw' / 'scraped_earthquakes.csv'

# Leer el archivo CSV
df = pd.read_csv(csv_path)


#convertimos la columna Date & Time UTC a un objeto datetime.
df['Date & Time UTC'] = pd.to_datetime(df['Date & Time UTC'], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')


# Intentamos dividir la columna 'Region' por la coma y el espacio
split_columns = df['Region'].str.split(', ', expand=True)

# Verificamos si la división fue exitosa
if 1 in split_columns.columns:
    df['Country'] = split_columns[1]
else:
    df['Country'] = split_columns[0]  # Si no hubo división, mantenemos el valor original en 'Country'

df['Region'] = split_columns[0].fillna(df['Region'])  # Si no hubo división, mantenemos el valor original en 'Region'

#Eliminamos columnas innecesarias.
clean_df = df.drop(columns=['Type', 'A/M'])
#Eliminamos de la columna Magnitude los valores menores a 0 y mayores a 9.4
clean_df = clean_df[(clean_df['Magnitude'] >= 0.5) & (clean_df['Magnitude'] <= 9.2)]

#Guardamos el dataframe limpio en un archivo csv.
clean_csv_path = current_dir.parents[1] / 'data' / 'processed' / 'clean_earthquakes.csv'
clean_df.to_csv(clean_csv_path, index=False)
print("Data cleaned and saved to:", clean_csv_path)