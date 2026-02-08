CREATE TABLE IF NOT EXISTS 'peliculas' (
  'nombre' TEXT NOT NULL,
  'fecha' TEXT DEFAULT NULL,
  'sesion' TEXT DEFAULT NULL,
  'urlImg' TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS 'votos' (
  'idPelicula' INTEGER NOT NULL,
  'usuario' TEXT DEFAULT NULL,
  'voto' INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS 'configuracion' (
  'votacionActiva' INTEGER DEFAULT NULL
);
INSERT INTO configuracion VALUES (-1);