from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('lugar', __name__)

@bp.route('/')
def index():
    db = get_db()
    lugares = db.execute('SELECT l.id_lugar, l.nombre_lugar, l.id_creador, u.username '
                       'FROM lugar l JOIN user u ON l.id_creador = u.id_user '
                       'ORDER BY l.nombre_lugar ').fetchall()
    return render_template('lugar/index.html', lugares=lugares)

@bp.route('/crear_lugar', methods=('GET', 'POST'))
@login_required
def crear_lugar():
    if request.method == 'POST':
        nombre_lugar = request.form['nombre_lugar']
        error = None

        if not nombre_lugar:
            error = 'Nombre de lugar requerido'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('INSERT INTO lugar (nombre_lugar, id_creador) '
                       'VALUES (?,?)',
                       (nombre_lugar, g.user['id_user'])
                       )
            db.commit()
            return redirect(url_for('lugar.index'))
    return render_template('lugar/create.html')

def get_lugar(id_lugar, check_author=True):
    lugar = get_db().execute(
        'SELECT l.id_lugar, l.nombre_lugar, l.id_creador, u.username '
        'FROM lugar l JOIN user u ON l.id_creador = u.id_user '
        'WHERE l.id_lugar = ?',
        (id_lugar,)
        ).fetchone()
    if lugar is None:
        abort(404,f"Lugar con id {id_lugar} no existe")
    if check_author and lugar['id_creador'] != g.user['id_user']:
        abort(403)
    return lugar

@bp.route('/<int:id_lugar>/actualizar_lugar', methods=('GET','POST'))
@login_required
def actualizar_lugar(id_lugar):
    lugar = get_lugar(id_lugar)

    if request.method == 'POST':
        nombre_lugar = request.form['nombre_lugar']
        error = None

        if not nombre_lugar:
            error = 'Nombre de lugar requerido'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE lugar SET nombre_lugar = ?'
                       'WHERE id_lugar = ?',
                       (nombre_lugar, id_lugar)
                       )
            db.commit()
            return redirect(url_for('lugar.index'))
    return render_template('lugar/update.html', lugar=lugar)

@bp.route('/<int:id_lugar>/eliminar_lugar', methods=('POST',))
@login_required
def eliminar_lugar(id_lugar):
    get_lugar(id_lugar)
    db = get_db()
    db.execute(
        'DELETE FROM lugar WHERE id_lugar = ?',(id_lugar,)
    )
    db.commit()
    return redirect(url_for('lugar.index'))