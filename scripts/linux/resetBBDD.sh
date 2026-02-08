#!/usr/bin/env bash

fecha=$(date +"%Y-%m-%d_%H_%M_%S")

echo "Verificando dependencias..."
if command -v python3 &> /dev/null; then
	echo "python3 ya está instalado."
else
        echo "python3 no está instalado. Instalando..."
    	sudo apt update && sudo apt install -y python3
fi

if ! command -v sqlite3 &> /dev/null; then
	echo "sqlite3 no está instalado. Instalando..."
    	sudo apt update && sudo apt install -y sqlite3
else
        echo "sqlite3 ya está instalado."
fi

if [ -f "../../sql/discordflix.db" ]; then
	echo "Haciendo Backup de la Base de Datos anterior..."
	if ![ -d "../../sql/backups" ]; then
		echo "Generando directorio de backups..."
		mkdir ../../sql/backups
	fi
	cp ../../sql/discordflix.db ../../sql/backups/discordflix_backup_${fecha}.db
	rm ../../sql/discordflix.db
fi

echo "Generando la base de datos..."
if [ -d "../../aplicacion/venv" ]; then
	echo "Ya existe el entorno virtual de python3"
else
	python3 -m venv ../../aplicacion/venv &> /dev/null
	source ../../aplicacion/venv/bin/activate &> /dev/null
	pip install -U py-cord &> /dev/null
	echo "Entorno virtual de python3 generado"
fi

sqlite3 ../../sql/discordflix.db < ../../sql/crearBBDD.sql

echo "Terminado"
echo "Presiona Enter para cerrar..."
read
