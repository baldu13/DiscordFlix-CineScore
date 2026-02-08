#!/usr/bin/env bash

echo "Generando datos de ejemplo en la BBDD para pruebas..."
sqlite3 ../../sql/discordflix.db < ../../sql/cargaDatosEjemplo.sql

echo "Terminado"

echo "Presiona Enter para cerrar..."
read