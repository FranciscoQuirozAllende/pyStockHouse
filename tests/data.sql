INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO lugar (id_lugar, nombre_lugar, id_creador)
VALUES
  (1,'cocina',1);

INSERT INTO articulo (id_articulo, nombre_articulo, cantidad, id_lugar_articulo)
VALUES (1,'lavaloza',3,1);