import discord
import config
import math
import basededatos as bd

#####################
# UTILIDADES VARIAS #
#####################

# Si el mensaje supera los 2000 caracteres, lo separa en párrafos en medida de lo posible, sino corta por '.', sino corta por palabra.
async def enviarMensaje(ctx, mensaje):
    for msg in split_message(mensaje):
        return await ctx.send(msg)


def fchStrANum(fchStr):
    campos = fchStr.split("-")
    return campos[2] + campos[1] + campos[0]


def fchNumAStr(fchNum):
    return fchNum[6:] + "-" + fchNum[4:6] + "-" + fchNum[:4]


def media(lista):
    if len(lista) == 0:
        return -1
    else:
        nota = 0
        for num in lista:
            nota += num[0]
        return f'{(nota / float(len(lista))):.2f}'


def pintaEstrellas(nota):
    redondeado = round(nota)
    txt = ""
    for i in range(5):
        evaluar = redondeado - (2 * i)
        if evaluar <= 0:
            txt += config.estrellaVacia
        elif evaluar == 1:
            txt += config.estrellaMedia
        else:
            txt += config.estrellaCompleta
    return txt


def split_message(text, limit=2000):
   
    # Divide un texto en fragmentos de máximo 'limit' caracteres, intentando no romper palabras.
    chunks = []
    while len(text) > limit:

        # Primero intentamos con saltos de línea
        split_index = text.rfind('\n', 0, limit)  
        
        # Si no hay, buscamos un punto
        if split_index == -1:
            split_index = text.rfind('.', 0, limit) 

        # Si no hay, buscamos un espacio
        if split_index == -1:
            split_index = text.rfind(' ', 0, limit) 

        # Si no hay espacios ni saltos (palabra larguísima), cortamos por el límite
        if split_index == -1:
            split_index = limit

        chunks.append(text[:split_index].strip())
        text = text[split_index:].strip()

    if text:
        chunks.append(text)

    return chunks


async def pintaInfo(ctx, peli):
    votos = bd.recuperaVotos(peli[1])
    nota = 0
    if len(votos) > 0:
        nota = f'{notaSobreDiez(media(votos))}'
    else:
        nota = 'Sin valoración'
    txt = f'## :bar_chart: Resultado de la sesión DiscordFlix #{peli[3]} del [{fchNumAStr(peli[2])}]\n'
    await enviarMensaje(ctx, txt)
    await enviarMensaje(ctx, f'{bd.urlImg(peli[1])}')
    txt = f'- :clapper: **___{peli[1]}___**\n'
    txt += f'- :trophy: Nota media: **{nota}** {pintaEstrellas(float(media(votos)))}\n'
    txt += f'- :busts_in_silhouette: Votos registrados: **{len(votos)}**\n'
    txt += f'- :heart: ¡Gracias por ver cine con nosotros!'
    await enviarMensaje(ctx, txt)


async def pintaListado(ctx, totalPeliculas, inicio = 0, message = None):
    inicio = max(min(len(totalPeliculas)-config.tam_pagina, inicio), 0)
    fin = inicio + min(len(totalPeliculas)-int(inicio), config.tam_pagina)
    numPag = math.ceil(fin / config.tam_pagina)
    maxPag = math.ceil(len(totalPeliculas) / config.tam_pagina)
    txt = "## :clapper: Historial de sesiones de DiscordFlix\n"
    for i in range(inicio, fin):
        peli = totalPeliculas[i]
        txt += f'* Sesión #{peli[3]} del [{fchNumAStr(peli[2])}] **"{peli[1]}"**\n'
    await gestionaMensaje(ctx, txt, numPag, maxPag, message)


async def pintaMiRanking(ctx, votosUsuario, autor, inicio = 0, message = None):
    inicio = max(min(len(votosUsuario)-config.tam_pagina, inicio), 0)
    fin = inicio + min(len(votosUsuario)-int(inicio), config.tam_pagina)
    numPag = math.ceil(fin / config.tam_pagina)
    maxPag = math.ceil(len(votosUsuario) / config.tam_pagina)
    txt = f'## Este es el ranking de películas vistas y valoradas por {autor.mention}: \n'
    for i in range(inicio, fin):
        voto = votosUsuario[i]
        txt += f'{i+1}. {pintaEstrellas(float(voto[1]))} **"{bd.nombrePeliculaId(voto[0])}"**, con una nota de **{notaSobreDiez(str(int(voto[1])))}**\n'
    await gestionaMensaje(ctx, txt, numPag, maxPag, message)


async def pintaRanking(ctx, pelis, estilo = 'Total', inicio = 0, message = None):
    # Ordenamos las películas juntos con su calificación
    inicio = max(min(len(pelis)-config.tam_pagina, inicio), 0)
    ordenadas = []
    while len(pelis) > 0:
        i = 0 # Indice actual de la iteracion
        topIdx = -1 # Indice de la mejor pelicula
        topVal = -5 # Valoracion de la mejor película
        for peli in pelis:
            votos = bd.recuperaVotos(peli[1])
            nota = media(votos)
            if float(nota) > float(topVal):
                topIdx = i
                topVal = nota
            i += 1
        ordenadas.append([pelis[topIdx], topVal])
        del pelis[topIdx]
        topIdx = -1 # Reset
        topVal = -5 # Reset
    # Obtenemos las películas que están valoradas
    ordenadasValoradas = []
    for peli in ordenadas:
        if peli[1] != -1:
            ordenadasValoradas.append(peli)

    if estilo == 'Total':
        # Si hay menos de 7 películas valoradas, pintamos todas en orden (las no valoradas al final)
        txt = "## :projector: Películas vistas en DiscordFlix, ordenadas por valoración de los usuarios:\n\n"
        fin = inicio + min(len(ordenadas)-int(inicio), config.tam_pagina)
        numPag = math.ceil(fin / config.tam_pagina)
        maxPag = math.ceil(len(ordenadas) / config.tam_pagina)
        for i in range(inicio, fin):
            valoracion = "Sin valoraciones" if ordenadas[i][1] == -1 else f"{notaSobreDiez(str(ordenadas[i][1]))}"
            valoracionNum = 0 if ordenadas[i][1] == -1 else ordenadas[i][1]
            txt += f'* {i+1}. {pintaEstrellas(float(ordenadas[i][1]))} **"{ordenadas[i][0][1]}"**. Nota media: **{valoracion}**.\n'
        await gestionaMensaje(ctx, txt, numPag, maxPag, message)
    elif estilo == 'Top':
        # Pintamos las 3 mejor valoradas y las 3 peor valoradas, pasando de las no valoradas
        top3 = ordenadasValoradas[:3]
        txt = "## :medal: Mejores 3 películas vistas en DiscordFlix, ordenadas por valoración de los usuarios\n\n"
        i = 0
        while i < len(top3):
            valoracion = str(top3[i][1])
            txt += f'{i+1}. {pintaEstrellas(float(top3[i][1]))} **"{top3[i][0][1]}"**: Nota media: **{notaSobreDiez(top3[i][1])}**\n'
            i += 1
        
        bot3 = ordenadasValoradas[-3:]
        txt += "\n## :poop: Peores 3 películas vistas en DiscordFlix, ordenadas por valoración de los usuarios\n\n"
        i = len(bot3) - 1
        while i >= 0:
            valoracion = str(bot3[i][1])
            txt += f'{3-i}. {pintaEstrellas(float(bot3[i][1]))} **"{bot3[i][0][1]}"**: Nota media: **{notaSobreDiez(bot3[i][1])}**\n'
            i -= 1
        await enviarMensaje(ctx, txt)
    else:
        await enviarMensaje(ctx, 'Estilo de Ranking desconocido...')
        

# Para enviar o gestionar el mensaje por páginas con todo lo necesario
async def gestionaMensaje(ctx, txt, numPag, maxPag, message):
    txt += f'-# Página {numPag}/{maxPag}'
    if message == None:
        mensaje = await enviarMensaje(ctx, txt)
    else:
        mensaje = await message.edit(txt)

    # Limpiamos las reacciones anteriores y creamos las nuevas que correspondan
    if isinstance(mensaje.channel, discord.DMChannel):
        # Por msg privado, solo puede eliminar sus propias reacciones
        await mensaje.remove_reaction(config.pag_anterior, mensaje.author)
        await mensaje.remove_reaction(config.pag_siguiente, mensaje.author)
    else:
        # Canal de servidor, puede eliminar todas
        await mensaje.clear_reaction(config.pag_anterior)
        await mensaje.clear_reaction(config.pag_siguiente)
    if numPag != 1:
        await mensaje.add_reaction(config.pag_anterior)
    if numPag != maxPag:
        await mensaje.add_reaction(config.pag_siguiente)

async def reaccionaSegunNota(message, nota):
    emoji = ''
    match float(nota):
        case t if float(nota) >= 0.0 and float(nota) < 5.0:
            emoji = '😬'
        case t if float(nota) >= 5.0 and float(nota) < 7.0:
            emoji = '🤔'
        case t if float(nota) >= 7.0 and float(nota) < 9.0:
            emoji = '😄'
        case t if float(nota) >= 9.0 and float(nota) <= 10.0:
            emoji = '🔥'

    if emoji != '':
        await message.add_reaction(emoji)


def notaSobreDiez(nota):
    if float(nota).is_integer():
        return f'{int(float(nota))}/10'
    else:
        return f'{str(round(float(nota), 2))}/10'


def esNumero(valor):
    if valor is None:
        return False
    try:
        float(str(valor).replace(',', '.').strip())
        return True
    except ValueError:
        return False
