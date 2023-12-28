DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS articulo;
DROP TABLE IF EXISTS lugar;

CREATE TABLE user (
  id_user INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE lugar (
    id_lugar INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_lugar TEXT UNIQUE NOT NULL,
    id_creador INTEGER NOT NULL,
    FOREIGN KEY (id_creador) REFERENCES user (id)
);

CREATE TABLE articulo (
    id_articulo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_articulo TEXT UNIQUE NOT NULL,
    cantidad INTEGER NOT NULL,
    id_lugar_articulo INTEGER NOT NULL,
    FOREIGN KEY (id_lugar_articulo) REFERENCES lugar (id_lugar)
);