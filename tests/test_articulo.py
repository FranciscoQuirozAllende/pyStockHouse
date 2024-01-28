import pytest
from PyStockHouse.db import get_db


def test_index_articulo(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute("SELECT * FROM articulo WHERE articulo = ").fetchone()
    print("a")
