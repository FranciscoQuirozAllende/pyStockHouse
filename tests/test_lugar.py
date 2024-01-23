import pytest
from PyStockHouse.db import get_db


def test_index(client, auth):
    response = client.get("/")
    assert b"Iniciar Sesion" in response.data
    assert b"Registrarse" in response.data

    auth.login()
    response = client.get("/")
    assert b"Cerrar Sesion" in response.data
    assert b"cocina" in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/crear_lugar",
        "/1/actualizar_lugar",
        "/1/eliminar_lugar",
    ),
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute("UPDATE lugar SET id_lugar=2 WHERE id_creador=1")
        db.commit()

        auth.login()
        assert client.post("/1/actualizar_lugar").status_code == 403
        assert client.post("/1/eliminar_lugar").status_code == 403
        assert b'href="/1/actualizar_lugar"' not in client.get("/").data


@pytest.mark.parametrize(
    "path",
    (
        "/2/actualizar_lugar",
        "/2/eliminar_lugar",
    ),
)
def test_exist_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get("/crear_lugar").status_code == 200
    client.post("/crear_lugar", data={"nombre_lugar": "creado"})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id_lugar) FROM lugar").fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get("/actualizar_lugar").status_code == 200
    client.post("/1/actualizar_lugar", data={"nombre_lugar": "actualizado"})

    with app.app_context():
        db = get_db()
        post = db.execute("SELECT * FROM lugar WHERE id_lugar = 1").fetchone()
        assert post["nombre_lugar"] == "actualizado"


@pytest.mark.parametrize(
    "path",
    (
        "/crear_lugar",
        "/1/actualizar_lugar",
    ),
)
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={"nombre_lugar": ""})
    assert b"El titulo es necesario" in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/1/eliminar_lugar")
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        lugar = db.execute("SELECT * FROM lugar WHERE id_lugar = 1").fetchone()
        assert lugar is None
