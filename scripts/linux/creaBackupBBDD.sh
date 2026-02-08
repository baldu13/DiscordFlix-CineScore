#!/usr/bin/env bash

fecha=$(date +"%Y-%m-%d_%H_%M_%S")

if [ -f "../../sql/discordflix.db" ]; then
	echo "Haciendo Backup de la Base de Datos anterior..."
	if ![ -d "../../sql/backups" ]; then
		echo "Generando directorio de backups..."
		mkdir ../../sql/backups
	fi
	cp ../../sql/discordflix.db ../../sql/backups/discordflix_backup_${fecha}.db
else
	echo "No hay ninguna base de datos de la cual hacer backup."
fi

echo "Terminado"
echo "Presiona Enter para cerrar..."
read
