import discord
from discord.ext import commands
from datetime import datetime
import basededatos as bd
import utilidades
import config

encuadrar = '`'
prefijo = config.prefijo

# Si el mensaje supera los 2000 caracteres, lo separa en párrafos en medida de lo posible, sino corta por '.', sino corta por palabra.
async def enviarMensaje(ctx, mensaje):
	for msg in utilidades.split_message(mensaje):
			return await ctx.send(msg)


#######################################################################
# Bot para registrar películas y votos de las sesiones de DiscordFlix #
#######################################################################
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# Usuarios especiales que pueden:
#   - Crear películas
#   - Iniciar y cerrar encuestas
usuarios_admin = config.administradores
msg_usuario_no_admin = 'Usuario no autorizado para ejecutar comandos de administración'

bot = commands.Bot(command_prefix=prefijo, intents=intents)

@bot.event
async def on_message(message):
	# Por defecto, Pycord hace esto internamente:
  # if message.author.bot: return
	if message.author.id == bot.user.id:
		return # Para no procesar los mensajes de este mismo bot
	# Para habilitar que un bot pueda ejecutar alguno de los comandos
	if message.author.bot:
		ctx = await bot.get_context(message)
		if message.content == f'{prefijo}info':
			await _info(ctx, *ctx.args)
		if message.content.startswith(f'{prefijo}abrir'):
			await _abrir(ctx, *ctx.args)
		if message.content.startswith(f'{prefijo}cerrar'):
			await _cerrar(ctx, *ctx.args)
	else:
		await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
	# Si el error es que el comando no existe, lo ignoramos por completo
	if isinstance(error, commands.CommandNotFound):
		return
	# Para cualquier otro error (permisos, errores de código, etc.)
	raise error


# Comando !ayuda, para registrar un voto
@bot.command(name='ayuda')
async def _ayuda(ctx, *args):
	txt = f'## {config.msg_presentacion}\n'
	txt += f'\n### Comandos generales:\n'
	txt += f'* {encuadrar}{prefijo}listado{encuadrar} Mostrar un listado de todas las películas, de más reciente a más antigua.\n'
	txt += f'* {encuadrar}{prefijo}top{encuadrar} Mostrar un ranking de las mejores y peores películas.\n'
	txt += f'* {encuadrar}{prefijo}ranking{encuadrar} Mostrar el ranking de todas películas, por nota media.\n'
	txt += f'* {encuadrar}{prefijo}miranking{encuadrar} Mostrar un ranking de las mejores y peores películas según valoración personal.\n'
	txt += f'* {encuadrar}{prefijo}ultima{encuadrar} Mostrar información de la última película vista.\n'
	txt += f'* {encuadrar}{prefijo}puntua [0-10]{encuadrar} Cuando haya una votación abierta, permite aportar tu valoración de la misma.\n'
	txt += f'* {encuadrar}{prefijo}info [NombrePelicula]{encuadrar} Muestra la información de una película.\n'
	txt2 = f'### Comandos de administración:\n'
	txt2 += f'* {encuadrar}{prefijo}pelicula [Sesion] "[NombrePelicula]" "[URL Portada]" "<fecha>"{encuadrar} Crea una película para la sesión indicada, con el nombre indicado y opcionalmente para la fecha indicada, sino por defecto para la fecha actual. Por ejemplo: _{prefijo}pelicula 10 "Mi película" "https:www.urlImagen.com/img.jpg" "01-01-2026"_\n'
	txt2 += f'* {encuadrar}{prefijo}abrir <NombrePelicula>{encuadrar} Abre el periodo de calificación para la película designada, o la última si no se indica nada.\n'
	txt2 += f'* {encuadrar}{prefijo}cerrar{encuadrar} Cierra el periodo de calificación activo, en caso de haberlo.\n'
	txt2 += f'* {encuadrar}{prefijo}editar [NombrePeliculaAnterior] [Sesion] "[NombrePelicula]" "[URL Portada]" "[fecha]"{encuadrar} Actualiza los datos de una película.\n'
	txt2 += f'* {encuadrar}{prefijo}eliminar [NombrePelicula]{encuadrar} Elimina la película y todos sus votos.\n'
	await enviarMensaje(ctx, txt)
	if ctx.author.id in usuarios_admin:
		await ctx.author.send(txt2)


# Comando !ayuda, para registrar un voto
@bot.command(name='info')
async def _info(ctx, *args):
	if len(args) == 0:
		await enviarMensaje(ctx, f'Uso: **{prefijo}info [NombrePelicula]**')
	else:
		nombrePeli = ' '.join(map(str, args))
		if bd.existePelicula(nombrePeli):
			peli = bd.recuperaPelicula(nombrePeli)
			await utilidades.pintaInfo(ctx, peli)
		else:
			await enviarMensaje(ctx, f'La película **{nombrePeli}** no existe.')


# Comando /voto, para registrar un voto
@bot.command(name='puntua')
async def _puntua(ctx, *args):
	if len(args) != 1:
		await enviarMensaje(ctx, f'Uso: **{prefijo}puntua [0-10]**')
	elif not args[0].isnumeric() or int(args[0])<0 or int(args[0])>10:
		await enviarMensaje(ctx, f'Calificación incorrecta. Uso: **{prefijo}puntua [0-10]**')
	elif '.' in args[0] or ',' in args[0]:
		await enviarMensaje(ctx, f'Por favor, introduce un número sin decimales. Uso: **{prefijo}puntua [0-10]**')
	elif bd.votacionActual() == -1:
		await enviarMensaje(ctx, f'No hay ninguna encuesta activa.')
	else:
		# Falta registrar el voto como tal
		votoAnterior = bd.registraVoto(bd.votacionActual(), ctx.author.id, args[0])
		if votoAnterior == -1:
			await enviarMensaje(ctx, f'Registrada calificación **{args[0]}/10** de **{ctx.author.display_name}**. ¡Gracias por tu aporte!')
		else:
			await enviarMensaje(ctx, f'Se ha modificado tu calificación anterior de **{votoAnterior}/10** a **{args[0]}/10**.')


# Comando /pelicula, para crear una película
@bot.command(name='pelicula')
async def _pelicula(ctx, *args):
	if len(args) < 3:
		await enviarMensaje(ctx, f'Uso: **{prefijo}pelicula [Sesion] [NombrePelicula] [URL Portada] <fecha>**')
	elif ctx.author.id in usuarios_admin:
		if len(args) == 4:
			fch = args[3]
		else:
			fch = datetime.today().strftime('%d-%m-%Y')
		sesion = args[0]
		nombrePeli = args[1]
		urlImg = args[2]
		if bd.existePelicula(nombrePeli):
			await enviarMensaje(ctx, f'La película **"{nombrePeli}"** ya existe.')
		else:
			bd.registraPelicula(nombrePeli, utilidades.fchStrANum(fch), sesion, urlImg)
			await enviarMensaje(ctx, f'Registrada la película de la sesión #{sesion}: **"{nombrePeli}"** en fecha **{fch}**')
	else:
		print(f'El usuario {ctx.author.display_name}:{ctx.author.id} ha intentado ejecutar un comando de administración, pero no tiene los permisos necesarios.')
		await enviarMensaje(ctx, msg_usuario_no_admin)


# Comando para abrir votación para una película
@bot.command(name='abrir')
async def _abrir(ctx, *args):
	if ctx.author.id in usuarios_admin:
		if len(args) < 1:
			nombrePeli = bd.recuperaPeliculas()[0][1]
		else:
			nombrePeli = ' '.join(map(str, args))
		if bd.idPeliculaNombre(nombrePeli) == -1:
			await enviarMensaje(ctx, f'No hay ninguna película con el nombre **"{nombrePeli}"**.')
		else:
			bd.setVotacionActiva(bd.idPeliculaNombre(nombrePeli))
			txt = '## :clapper: **Nueva votación abierta en CineScore**\n'
			await enviarMensaje(ctx, txt)
			await enviarMensaje(ctx, f'{bd.urlImg(nombrePeli)}')
			txt = f'- :projector: Película: **___{nombrePeli}___**\n'
			txt += f'- :pencil: Vota del **0 al 10** usando {encuadrar}{prefijo}puntua [0-10]{encuadrar}\n'
			txt += f'- :popcorn: ¡Gracias por participar en DiscordFlix!'
			await enviarMensaje(ctx, txt)
		# Borramos el mensaje original que nos ha invocado para limpiar
		await ctx.message.delete()
	else:
		print(f'El usuario {ctx.author.display_name}:{ctx.author.id} ha intentado ejecutar un comando de administración, pero no tiene los permisos necesarios.')
		await enviarMensaje(ctx, msg_usuario_no_admin)


# Comando para que si hay una votación activa, se cierre
@bot.command(name='cerrar')
async def _cerrar(ctx, *args):
	if ctx.author.id in usuarios_admin:
		if bd.votacionActual() == -1:
			await enviarMensaje(ctx, f'Actualmente no hay ninguna votación activa para cerrar.')
		else:
			nombrePeli = bd.nombrePeliculaId(bd.votacionActual())
			bd.setVotacionActiva(-1)
			txt = '## :clapper: **Votación cerrada en CineScore**\n'
			txt += '- :popcorn: ¡Gracias por participar!\n'
			votos = bd.recuperaVotos(nombrePeli)
			nota = 0
			if len(votos) > 0:
				nota = utilidades.media(votos)
				txt += f'- :projector: La película **{nombrePeli}** ha obtenido una valoración de...\n'
				txt += f'|| ## **{nota}/10** {utilidades.pintaEstrellas(float(nota))}||'
			else:
				txt += f'- :projector: La película **{nombrePeli}** no ha recibido ningún voto...'
			await enviarMensaje(ctx, txt)
		# Borramos el mensaje original que nos ha invocado para limpiar
		await ctx.message.delete()
	else:
		print(f'El usuario {ctx.author.display_name}:{ctx.author.id} ha intentado ejecutar un comando de administración, pero no tiene los permisos necesarios.')
		await enviarMensaje(ctx, msg_usuario_no_admin)


# Comando para ver un resumen de las estadísticas de la última película
@bot.command(name='ultima')
async def _ultima(ctx, *args):
	pelis = bd.recuperaPeliculas()
	if len(pelis) == 0:
		await enviarMensaje(ctx, f'No hay ninguna película aún.')
	else:
		peli = pelis[0]
		await utilidades.pintaInfo(ctx, peli)


# Comando para ver un listado de todas las películas ordenadas de más reciente a más antigua
@bot.command(name='listado')
async def _listado(ctx, *args):
	peliculas = bd.recuperaPeliculas()
	if len(args) == 1 and args[0].isnumeric():
		await utilidades.pintaListado(ctx, peliculas, int(args[0]))
	else:
		await utilidades.pintaListado(ctx, peliculas, 0)


# Comando para ver un listado de las mejores y peores películas por voloración global
@bot.command(name='ranking')
async def _ranking(ctx, *args):
	pelis = bd.recuperaPeliculas()
	await utilidades.pintaRanking(ctx, pelis, 'Total')


# Comando para ver un listado de las mejores y peores películas por valoración personal del usuario
@bot.command(name='miranking')
async def _miranking(ctx, *args):
	votosUsuario = bd.recuperaVotosUsuario(ctx.author.id)
	autor = ctx.author
	if len(args) == 1 and args[0].isnumeric():
		await utilidades.pintaMiRanking(ctx, votosUsuario, autor, int(args[0]))
	else:
		await utilidades.pintaMiRanking(ctx, votosUsuario, autor)


# Comando para editar la información de una película existente
@bot.command(name='editar')
async def _editar(ctx, *args):
	if ctx.author.id in usuarios_admin:
		if len(args) >= 4:
			nombreAnt = args[0]
			nombreNew = args[2]
			sesion = args[1]
			urlImg = args[3]
			fch = datetime.today().strftime('%d-%m-%Y')
			if len(args) >= 5:
				fch = args[4]
			# Si no existe la peli, no podemos editar nada
			if bd.existePelicula(nombreAnt) == False:
				await enviarMensaje(ctx, f'La película **{peli}** no existe.')
				return
			bd.modificaPelicula(nombreAnt, nombreNew, utilidades.fchStrANum(fch), sesion, urlImg)
			await enviarMensaje(ctx, f'Película **{nombreAnt}** modificada.')
		else:
			await enviarMensaje(ctx, f'Uso: {encuadrar}{prefijo}editar "[NombrePeliculaAnterior]" [Sesion] "[NombrePeliculaNuevo]" "[UrlImg]" <Fecha>{encuadrar}')
	else:
		print(f'El usuario {ctx.author.display_name}:{ctx.author.id} ha intentado ejecutar un comando de administración, pero no tiene los permisos necesarios.')
		await enviarMensaje(ctx, msg_usuario_no_admin)


# Comando para eliminar una película y sus votos
@bot.command(name='eliminar')
async def _eliminar(ctx, *args):
	if ctx.author.id in usuarios_admin:
		if len(args) > 0:
			peli = ' '.join(map(str, args))
			# Si no existe la peli, no podemos borrar nada
			if bd.existePelicula(peli) == False:
				await enviarMensaje(ctx, f'La película **{peli}** no existe.')
				return
			votos = bd.recuperaVotos(peli)
			await enviarMensaje(ctx, f'Película **{peli}** eliminada junto con sus **{len(votos)}** votos.')
		else:
			await enviarMensaje(ctx, f'Uso: {encuadrar}{prefijo}eliminar [NombrePelicula]{encuadrar}')
	else:
		print(f'El usuario {ctx.author.display_name}:{ctx.author.id} ha intentado ejecutar un comando de administración, pero no tiene los permisos necesarios.')
		await enviarMensaje(ctx, msg_usuario_no_admin)


# Comando para ver el top
@bot.command(name='top')
async def _top(ctx, *args):
	await utilidades.pintaRanking(ctx, bd.recuperaPeliculas(), 'Top')


@bot.event
async def on_raw_reaction_add(payload):
	
	canal = bot.get_channel(payload.channel_id)
	usuario = await bot.fetch_user(payload.user_id)
	mensaje = await canal.fetch_message(payload.message_id)
	ctx = await bot.get_context(mensaje)

	# Evitar que el bot reaccione a sus propias reacciones
	if payload.user_id == bot.user.id:
		return

	# Solo reacciona a reacciones de sus propios menasjes
	if mensaje.author.id != bot.user.id:
		return

	#Miramos que emoji ha sido para actuar en consecuencia
	modIdx = 0
	if str(payload.emoji) == config.pag_siguiente:
		modIdx = 0
	elif str(payload.emoji) == config.pag_anterior:
		modIdx = int(config.tam_pagina)*-2
	else:
		# Emoji desconocido o sin función
		return

	if mensaje.content.startswith('## Lista de películas vistas en DiscordFlix:'):
		# Es el comando de listado, buscamos la página actual y subimos o bajamos una si corresponde
		numPag = mensaje.content[mensaje.content.rfind(' ')+1:mensaje.content.rfind('/')]
		inicio = int(int(numPag)*int(config.tam_pagina)) + modIdx
		await utilidades.pintaListado(ctx, bd.recuperaPeliculas(), inicio, mensaje)
	
	elif mensaje.content.startswith('## Este es el ranking de películas vistas y valoradas por'):
		# Es el comando de miranking, buscamos la página actual y subimos o bajamos una si corresponde
		numPag = mensaje.content[mensaje.content.rfind(' ')+1:mensaje.content.rfind('/')]
		inicio = int(int(numPag)*int(config.tam_pagina)) + modIdx
		idUsuario = mensaje.content[mensaje.content.find('@')+1:mensaje.content.find(' ', mensaje.content.find('@'))-2]
		usuarioMsg = await bot.fetch_user(idUsuario)
		await utilidades.pintaMiRanking(ctx, bd.recuperaVotosUsuario(idUsuario), usuarioMsg, inicio, mensaje)

	elif mensaje.content.startswith('## :projector: Películas vistas en DiscordFlix'):
		# Es el comando de ranking total, buscamos la página actual y subimos o bajamos una si corresponde
		numPag = mensaje.content[mensaje.content.rfind(' ')+1:mensaje.content.rfind('/')]
		inicio = int(int(numPag)*int(config.tam_pagina)) + modIdx
		await utilidades.pintaRanking(ctx, bd.recuperaPeliculas(), 'Total', inicio, mensaje)


# Iniciar el bot como tal
bot.run(config.api_token)
