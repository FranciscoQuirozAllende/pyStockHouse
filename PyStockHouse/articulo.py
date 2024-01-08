from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

bp = Blueprint('articulo', __name__)

@bp.route('/<int:id_lugar>/articulos')
def listar_articulos(id_lugar):
    db = get_db()
    articulos = db.execute('SELECT a.id_articulo, a.nombre_articulo, a.cantidad, a.id_lugar_articulo, l.nombre_lugar, u.id_user, u.username '
                           'FROM articulo a JOIN lugar l ON a.id_lugar_articulo = l.id_lugar '
                           'JOIN user u ON l.id_creador = u.id_user '
                           'WHERE a.id_lugar_articulo = ?'
                           'ORDER BY a.id_articulo DESC',(id_lugar,)).fetchall()
    
    return render_template('articulo/index.html', articulos=articulos)

@bp.route('/crear_articulo', methods=('GET','POST'))
@login_required
def crear_articulo():
    db = get_db()
    lugares = db.execute('SELECT id_lugar, nombre_lugar FROM lugar').fetchall()

    if request.method == 'POST':
        nombre_articulo = request.form['nombre_articulo']
        cantidad_articulo = request.form['cantidad']
        id_lugar_articulo = request.form['id_lugar_articulo']
        error = None

        if not nombre_articulo:
            error = 'Nombre de articulo obligatorio'

        if not cantidad_articulo:
            error = 'Cantidad de articulos obligatoria'

        if not id_lugar_articulo:
            error = 'Seleccione un lugar donde guardar su articulo'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('INSERT INTO articulo (nombre_articulo, cantidad, id_lugar_articulo) '
                       'VALUES (?,?,?)',(nombre_articulo, cantidad_articulo, id_lugar_articulo))
            db.commit()
            return redirect(url_for('lugar.index'))
    return render_template('articulo/create.html',lugares=lugares)

def get_articulo(id_articulo):
    db = get_db()
    articulo = db.execute('SELECT a.id_articulo, a.nombre_articulo, a.cantidad, a.id_lugar_articulo,l.nombre_lugar '
                          'FROM articulo a JOIN lugar l ON a.id_lugar_articulo = l.id_lugar '
                          'WHERE id_articulo = ?',(id_articulo,)).fetchone()
    
    if articulo is None:
        abort(404,f"Articulo con id {id_articulo} no existe")

    return articulo

@bp.route('/<int:id_articulo>/actualizar_articulo', methods=('GET','POST'))
@login_required
def actualizar_articulo(id_articulo):
    articulo = get_articulo(id_articulo)
    db = get_db()
    lugares = db.execute('SELECT id_lugar, nombre_lugar FROM lugar').fetchall()

    if request.method == 'POST':
        nombre_articulo = request.form['nombre_articulo']
        cantidad_articulo = request.form['cantidad']
        id_lugar_articulo = request.form['id_lugar_articulo']
        error = None

        if not nombre_articulo:
            error = 'Nombre de articulo obligatorio'

        if not cantidad_articulo:
            error = 'Cantidad de articulos obligatoria'

        if not id_lugar_articulo:
            error = 'Seleccione un lugar donde guardar su articulo'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE articulo '
                       'SET nombre_articulo = ?, cantidad = ?, id_lugar_articulo = ?'
                       'WHERE id_articulo = ?',
                       (nombre_articulo,cantidad_articulo,id_lugar_articulo,id_articulo)
                       )
            db.commit()
            return redirect(url_for('lugar.index'))
    return render_template('articulo/update.html', articulo=articulo, lugares=lugares)

@bp.route('/<int:id_articulo>/eliminar_articulo', methods=('POST',))
@login_required
def eliminar_articulo(id_articulo):
    get_articulo(id_articulo)
    db = get_db()
    db.execute('DELETE FROM articulo WHERE id_articulo = ? ',(id_articulo,))
    db.commit()
    return redirect(url_for('lugar.index'))