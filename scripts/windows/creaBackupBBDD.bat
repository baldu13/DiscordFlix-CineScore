@echo off

REM Creamos una variable con la fecha y hora actuales para añadirlo al fichero de backup
set "t=%time: =0%"
set "dia=%date:~0,2%"
set "mes=%date:~3,2%"
set "anio=%date:~6,4%"
set "hh=%t:~0,2%"
set "mm=%t:~3,2%"
set "ss=%t:~6,2%"
set "fecha_final=%dia%-%mes%-%anio%_%hh%_%mm%_%ss%"

REM Intenta copiar, si no existe el fichero de origen dará error, pero estamos redirigiendo tanto la salida a NUL asi que no se muestra nada
echo Haciendo Backup de la Base de Datos...
if not exist "..\..\sql\backups" (
	echo Generando directorio de backups...
	mkdir ..\..\sql\backups
)
copy /Y ..\..\sql\discordflix.db ..\..\sql\backups\discordflix_backup_%fecha_final%.db >nul

echo Terminado
pause