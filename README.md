# Proyecto I - EDA / ETL

##### En este Proyecto trabajaremos y analizaremos un dataset de terremotos ocurridos en los ultimos años.

## Objetivos del proyecto.

##### Los objetivos a perseguir en heste proyecto han sido los siguientes:
- ETL:
- - Extracción de datos de internet a trevés de un script de web scraping de python.
- - Transformacion y limpieza de los datos utilizando otro script, eliminandr registros o columnas innecesarios y formatear correctamente los datos para posteriores analisis con diferentes programas.
- - Almacenar de forma separada los distintos datasets para distintos programas para evitar problemas de compatibilidad de los archivos entre distintos programas.

## Estructura del proyecto.
##### La estructura de este proyecto es la siguiente:
```plaintext
Proyecto1evolve/
├── data/                          # Carpeta donde se almacenan los datos.
│   ├── raw/                       # Aquí se encuentra el CSV obtenido mediante el script.
│   └── processed/                 # Aquí están los archivos procesados de distintas formas para distintos programas.
│
├── dashboards/                    # Archivo de PowerBI.
│
├── src/                           # En esta carpeta se encuentra todo el código dividido en diferentes scripts para cada tarea.
│   ├── scraping/                  # Carpeta con el código para el web scraping.
│   │   └── scraping_script.py     # Script que realiza el scraping para extraer y guardar los datos.
│   │
│   ├── transform/                 # Aquí está el código para limpiar, transformar y formatear los datos.
│   │   ├── etl.py                 # Archivo de Python que realiza la transformación.
│   │   └── test_etl.ipynb         # Notebook de pruebas y test previo al script final.
│   │
│   └── eda/                       # Carpeta que contiene el notebook para el análisis exploratorio.
│       └── eda_test.ipynb         # Notebook donde se lleva a cabo el análisis exploratorio de los datos,
│                                  # junto con algunas visualizaciones y contrastes de hipótesis.
│
├── README.md                      # Este mismo archivo explicativo del proyecto.
│
└── requirements.txt               # Archivo de texto con las librerías que deben ser instaladas para que todo funcione.
```
## Pasos previos.
##### Antes de ejecutar el código es importante instalar las dependencias. estas se encuentran en el archivo requirements.txt
Puedes instalarlas todas con el siguiente comando de bash: pip install -r requirements.txt
## Descripcion del Proyecto.

### 1 Dataset
El dataset con el que trabajaremos en este proyecto es un conjunto de datos de los terremotos registrados en los ultimos 19 años.
El dataset consta de las siguientes columnas:
- **Date & Time UTC** Esta columna muesta la fecha y hora a la que se produjo el terremoto en horario UTC.
- **Lat.degrees** y **Lon. degrees** Son dos columnas que muestran las coordenadas del terremoto.
- **Depth km** Profundidad estimada o medida del terremoto en kms. En algunos terremotos este valor tiene una letra "f" asociada, lo que significa que la profundidad fue estimada.
- **Region** Muestra el país o region de este en la que se produjo el terremoto o, en su defecto, la zona del oceano.
- **Type** Muestra dos posibles valores: *origin* o *mt*. *Origin* significa que se obtuvo la informacion básica del terremoto. *mt* significa que se realizo un análisis más detallado del terremoto.
- **A/M** Esta columna indica si el terremoto fue registrado de forma automática *A* o manual *M*.
- **Magnitude** En esta columna hay un dato numérico que expresa la magnitud y unas siglas que indican la escala en la que se hizo la medición. Hay varias.
- **Network** Es la red de sismógrafos que registraron el terremoto.

### 2 Web scraping.
El archivo encargado de extraer los datos de la web y guardarlos en un archivo .csv es **scraping_script.py** se encuentra en **src/scraping/**.
A continuación se explica brevemente cómo funciona:

El programa accede a la url donde se encuentra la tabla con los datos. Pero hay un problema en cómo se muestran los datos.

En la web hay botones para pasar de pagina y botones para cambiar de dia. Esto es asi porque en una sola página no caben todos los terremotos de un solo dia, por eso hay botones para cambiar de pagina.

El problema esta en que si avanzamos de pagina muchas veces, eventualmente pasamos a los terremotos del dia siguiente. Esto podría servir para extraer datos indefinidamente, pero si intentamos pasar de pagina demasiadas veces hay un momento en el que la web deja de pasar las paginas y no podemos guardar mas registros.

Para solucionar esto el código sigue el siguiente flujo:

- Se empieza a scrapear en un dia determinado en una variable.
- Se comprueban los datos para ver si son del mismo dia que el de la variable, si lo son, se guardan usando *beautifulsuop* en un df de pandas. Cuando se acaba la tabla de la pagina. Se utiliza *selenium* para pasar de página.
- En el momento en el que el código detecta que el dia de un registro de la web no coincide con el del programa este no se guarda. En cambio, se cambia el dia estipulado en nuestra variable por un dia menos y se comienza el proceso de nuevo.
- Este flujo se puede iterar un numero indeterminado de veces cambiando en la iteración el número de dias que queremos scrapear.
- Por último, cuando la iteracion termina, los datos guardados como df de pandas se trasnforman en un archivo csv y se guardan en **data/raw/**

Este scraping es algo lento, tarda entre 2 y 3 horas en completarse para obtener un dataset como el que ya se encuentra en la carpeta del proyecto.

### 2 Transformación de los datos.
A continucacion se explica que datos se han transformado o eliminado y por qué.

El archivo etl.py ejecuta distintas transformaciones:
- Primero se transforma la columna **Date & Time UTC** a tipo datetime para trabajar con ella con pandas mas adelante.
- Se intenta separar la columna de **Region**. En esta columna, por lo general se especifica la región y luego el pais, separado por una coma y un espacio ", ".
En todos los casos no es asi, asi que el codigo intenta dividirlo por ", " si hay exito, la primera parte de la division se queda en region y la segunda en una nueva columna llamada **Country**. Si la división no es exitosa todo se queda como está.
- Despues eliminamos columnas como **Type** y **A/M**. Estas columnas no nos siren porque en nuestro contexto y con nuestros datos no aportan mucho valor.
- Eliminamos los terremotos de magnitud menor a 0.5 y mayores a 9.2 Eliminamos los menores para aligerar el dataset y los mayores porque no son fiables.
- Eliminamos los registros con valores nulos en las coordenadas o en la magnitud.
- Ahora hacemos una transformación importante para representar los datos mas adelante en visualizaciones. Aqui sumoamos a las coordenadas un numero decimal único muy pequeño. De esta forma nos podemos asegurar de que cada registro tiene coordenadas únicas (en las coordenadas originales se repetian) pero sin alterar apenas el valor de la latitud o longitud. Asi se evitan problemas en la representacion gráfica de Power Bi sin perder precisión.
- Una vez finalizados estos ajustes se guardan varias copias del nuevo df para que sean usadas por distintos programas y asi evitar posibles interferencias.


### 3 EDA
##### El analisis exploratorio de los datos Junto con las formulaciones y contrastes de hipótesis y algunas visualizaciones se encuentran en el archivo **eda_test.ipynb** En el anáisis exploratorio de los datos se plantean y analizan varias preguntas como:
- ¿Estan la profundidad y la magnitud correlacionadas?
- ¿Donde hay más terremotos? ¿Cerca del ecuador o cerca de los polos?
- ¿Cómo se distribuyen los terremotos segun su magnitud?
##### En ese archivo se encuentran todas las explicaciones redactadas junto con el código y las visualizaciones por lo que noo es necesario explicarlo aqui.


### 4 Dashboard
##### Aqui se encuentra el archivo de Power **BI Dashboard_terremotos.pbix**. En el Se encuentran algunas visualizaciones más con un formato mas vistoso.
