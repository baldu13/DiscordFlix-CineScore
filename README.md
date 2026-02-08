# DiscordFlix-CineScore

Bot para Discord creado para gestionar las películas y las puntuaciones que dan los usuarios a las mismas, con el objetivo de poder llevar un registro de la actividad y tener la posibilidad de sacar estadísticas.

La aplicación está en formato portable. Moviendo la carpeta raiz, se puede cambiar de ubicación incluso ejecutarlo en distinta máquina, incluso entre distintos sistemas operativos.

Se facilitan las instrucciones para su instalación, configuración y ejecución tanto para entornos Windows como Linux.

## Descripción de los scripts proporcionados
* `ejecutaBot`: Lanza el Bot en cuestión.
* `resetBBDD`: Crea la base de datos, o la regenera en caso de que existiera previamente.
* `creaBackupBBDD`: Crea un backup del estado actual de la base de datos.
* `cargaDatosEjemplo`: Da de alta unos datos de ejemplo en la base de datos para testear. Se pueden cambiar estos ejemplos desde el fichero `/sql/cargaDatosEjemplo.sql`

## Para Windows (ejecutables en la carpeta windows):
1. Instalar python3 (desde Microsoft Store mismamente)
2. Instalar librería necesaria para el bot (`python3 -m pip install -U py-cord`)
3. Ejecutar Script que genera la BBDD de la aplicación, `resetBBDD.bat`
4. Opcionalmente, cargar los datos de ejemplo, ejecutando el script `cargaDatosEjemplo.bat`
5. Ejecutar el Script para lanzar el bot, `ejecutaBot.bat`


## Para Linux (ejecutables en la carpeta linux):
1. Dar permisos de ejecución a los 3 scripts del directorio `/linux`
1. Ejecutar Script que genera la BBDD de la aplicación y configura el entorno para la aplicación (instala dependencias y configura el entorno virtual), `./resetBBDD.sh`
2. Opcionalmente, cargar los datos de ejemplo, ejecutando el script `./cargaDatosEjemplo.sh`
3. Ejecutar el Script para lanzar el bot, `./ejecutaBot.sh`

## Librerías y dependencias de terceros:
* [Python3](https://www.python.org)
* [Py-cord](https://pycord.dev)
* [sqlite3](https://sqlite.org)