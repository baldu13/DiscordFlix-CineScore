import sqlite3
import config

######################
# UTILIDADES DE BBDD #
######################
con = sqlite3.connect(config.base_datos)
cur = con.cursor()

def votacionActual():
  resultado = cur.execute("SELECT votacionActiva FROM configuracion")
  return resultado.fetchone()[0]


def idPeliculaNombre(pelicula):
	resultado = cur.execute("SELECT ROWID FROM peliculas WHERE nombre = ?", (pelicula,))
	fetched = resultado.fetchone()
	if fetched == None:
		return -1
	else:
		return fetched[0]


def nombrePeliculaId(idPelicula):
	resultado = cur.execute("SELECT nombre FROM peliculas WHERE ROWID = ?", (str(idPelicula),))
	fetched = resultado.fetchone()
	if fetched == None:
		return ''
	else:
		return fetched[0]


def registraPelicula(pelicula, fecha, sesion, urlImg = ''):
 	cur.execute("INSERT INTO peliculas VALUES (?, ?, ?, ?)", (pelicula, fecha, sesion, urlImg))
 	con.commit()


def recuperaVotos(pelicula):
	idPeli = idPeliculaNombre(pelicula)
	resultado = cur.execute("SELECT voto FROM votos WHERE idPelicula = ?", (idPeli,))
	return resultado.fetchall()


def recuperaVotosUsuario(usuario):
	resultado = cur.execute("SELECT idPelicula, voto FROM votos WHERE usuario = ? ORDER BY voto DESC", (usuario,))
	return resultado.fetchall()


def recuperaPeliculas():
	resultado = cur.execute("SELECT ROWID, nombre, fecha, sesion FROM peliculas ORDER BY fecha DESC")
	return resultado.fetchall()


def recuperaPelicula(nombrePeli):
	resultado = cur.execute("SELECT ROWID, nombre, fecha, sesion FROM peliculas WHERE nombre = ?", (nombrePeli,))
	return resultado.fetchone()


def registraVoto(pelicula, usuario, voto):
	resultado = cur.execute("SELECT voto FROM votos WHERE idPelicula = ? AND usuario = ?", (str(pelicula), usuario))
	valor = resultado.fetchone()
	existe = valor != None
	if (existe):
		cur.execute("UPDATE votos SET voto = ? WHERE idPelicula = ? AND usuario = ?", (str(voto), str(pelicula), usuario))
		con.commit()
		return valor[0]
	else:
	 	cur.execute("INSERT INTO votos VALUES (?, ?, ?)", (pelicula, usuario, str(voto)))
	 	con.commit()
	 	return -1


def setVotacionActiva(idPelicula):
	cur.execute("UPDATE configuracion SET votacionActiva = ?", (str(idPelicula),))
	con.commit()


def urlImg(nombrePeli):
	resultado = cur.execute("SELECT urlImg FROM peliculas WHERE nombre = ?", (nombrePeli,))
	fetched = resultado.fetchone()
	if fetched == None:
		return ''
	else:
		return fetched[0]


def modificaPelicula(nombreAnt, pelicula, fecha, sesion, urlImg = ''):
	cur.execute("UPDATE peliculas SET nombre = ?, fecha = ?, sesion = ?, urlImg = ? WHERE nombre = ?", (pelicula, fecha, sesion, urlImg, nombreAnt))
	con.commit()


def eliminaPelicula(nombrePelicula):
	idPelicula = idPeliculaNombre(nombrePelicula)
	cur.execute("DELETE FROM votos WHERE nombre = ?", (nombrePelicula,))
	cur.execute("DELETE FROM peliculas WHERE idPelicula = ?", (idPelicula,))
	con.commit()


def existePelicula(nombrePelicula):
	resultado = cur.execute("SELECT nombre FROM peliculas WHERE nombre = ?", (nombrePelicula,))
	fetched = resultado.fetchone()
	if fetched == None:
		return False
	else:
		return True