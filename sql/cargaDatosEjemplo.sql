INSERT INTO peliculas VALUES ('El Vengador Tóxico', '20260131', '49', 'https://i.imgur.com/SzdN6Kx.jpeg');
INSERT INTO peliculas VALUES ('El Increíble Hulk (2008)', '20260124', '48', 'https://imgur.com/z5dyCiC');
INSERT INTO peliculas VALUES ('Predator: Badlands (2025)', '20260117', '47', 'https://imgur.com/G99nTHq');
INSERT INTO peliculas VALUES ('Iron Man 2 (2010)', '20260110', '46', 'https://i.imgur.com/UGpwua8.jpeg');
INSERT INTO peliculas VALUES ('Iron Man (2008)', '20260103', '45', 'https://imgur.com/smIF6HE');

INSERT INTO votos VALUES ((SELECT ROWID FROM peliculas WHERE nombre='El Vengador Tóxico'), 12, 4);
INSERT INTO votos VALUES ((SELECT ROWID FROM peliculas WHERE nombre='El Vengador Tóxico'), 12, 3);
INSERT INTO votos VALUES ((SELECT ROWID FROM peliculas WHERE nombre='Predator: Badlands (2025)'), 13, 9);
INSERT INTO votos VALUES ((SELECT ROWID FROM peliculas WHERE nombre='Iron Man 2 (2010)'), 11, 10);
INSERT INTO votos VALUES ((SELECT ROWID FROM peliculas WHERE nombre='Iron Man 2 (2010)'), 12, 8);
INSERT INTO votos VALUES ((SELECT ROWID FROM peliculas WHERE nombre='Iron Man 2 (2010)'), 13, 7);