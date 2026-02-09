# Prefijo para los comandos del bot
prefijo = '!'

# Mensaje de presentación del bot
msg_presentacion = 'Bot creado por Baldu para registrar información sobre las sesiones de DiscordFlix. Tenemos pensado llevar un registro de las películas que hemos visto, y cuanto ha gustado en general.'

# ID de los usuarios que pueden ejecutar los comandos de administración
# Incluir también a los Bots que se quiera permitir ejecutar comandos de administración para automatizaciones
administradores = []

# Token de la aplicación de discord
api_token = 'inserta-aqui-tu-api-token'

# Nombre de la BBDD a usar, por defecto, la que se genera con los scripts de inicialización. (Modificar si se quiere cambiar la ruta, o usar un backup...)
base_datos = "../../sql/discordflix.db"

# Configura los emojis para usar para las puntuaciones basadas en estrellas.
# Se recomienda crear un emoji de media estrella y otro de estrella negra, pero se puede usar perfectamente con alternativas por defecto
estrellaCompleta = ':full_moon:'
estrellaMedia    = ':last_quarter_moon:' # Si es igual que la estrella vacía, la puntuación redondea hacia abajo, si es igual a la completa, hacia arriba, y si se pone otra cosa, se usará eso
estrellaVacia    = ':new_moon:'

# Tamaño máximo de página para los comandos que listan películas
tam_pagina = 10

# Emojis para página anterior y posterior
pag_anterior = "⬅️"
pag_siguiente = "➡️"

# Restringir las calificaciones a usuarios que posean un rol específico
calificacionRestrictiva = True
rolCalificador = 1021090746205479065