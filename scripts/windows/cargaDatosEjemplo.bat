@echo off

REM Generamos la BBDD nuevamente con el Script de creación. Sobreescribe el fichero anterior si existía, por eso hacemos backup antes
echo Generando datos de ejemplo en la BBDD para pruebas...
sqlite3 ..\..\sql\discordflix.db < ..\..\sql\cargaDatosEjemplo.sql

echo Terminado
pause