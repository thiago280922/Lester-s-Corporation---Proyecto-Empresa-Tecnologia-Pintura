from flask import Blueprint, request, jsonify, session, render_template
from database.bd import get_db
from flask import redirect, url_for
from datetime import datetime
posteos = Blueprint('posteos', __name__)

# ============ FRONTEND ============


@posteos.route("/posteos")
def ver_posteos():
    if "empleado_id" not in session:
        return redirect(url_for("login.login"))  # o la vista de login que tengas
    return render_template("posteos.html")


@posteos.route("/posteo/<int:id_posteo>")
def ver_posteo_detalle(id_posteo):
    if "empleado_id" not in session:
        return redirect(url_for("login.login"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.titulo, p.descripcion, e.usuario
        FROM posteo p
        JOIN empleado e ON p.empleado_id = e.id
        WHERE p.id = ?
    """, (id_posteo,))
    posteo = cursor.fetchone()
    conn.close()

    if not posteo:
        return "Posteo no encontrado", 404

    # Enviamos los datos del posteo a la plantilla
    return render_template("posteo.html", posteo={
        "id": posteo[0],
        "titulo": posteo[1],
        "descripcion": posteo[2],
        "usuario": posteo[3]
    })

# ============ API ============
@posteos.route("/api/posteos", methods=["GET"])
def listar_posteos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.id, p.titulo, p.descripcion, e.usuario, p.fecha_creacion
    FROM posteo p
    JOIN empleado e ON p.empleado_id = e.id
    ORDER BY p.id DESC
    """)
    posteos = cursor.fetchall()
    conn.close()

    resultados = []
    for p in posteos:
        resultados.append({
            "id": p[0],
            "titulo": p[1],
            "descripcion": p[2],
            "usuario": p[3],
            "fecha": p[4]
        })

    return jsonify(resultados)


@posteos.route("/empleado/posteo", methods=["POST"])
def crear_posteo():
    if "empleado_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    empleado_id = session["empleado_id"]
    data = request.json
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")

    conn = get_db()
    cursor = conn.cursor()
    fecha_creacion = datetime.now().isoformat()  

    cursor.execute(
    "INSERT INTO posteo (titulo, descripcion, fecha_creacion, empleado_id) VALUES (?, ?, ?, ?)",
    (titulo, descripcion, fecha_creacion, empleado_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Posteo creado correctamente"})

@posteos.route("/empleado/comentario", methods=["POST"])
def agregar_comentario():
    if "empleado_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    id_posteo = data.get("id_posteo")
    contenido = data.get("contenido")
    empleado_id = session["empleado_id"]

    conn = get_db()
    cursor = conn.cursor()
    fecha_creacion = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO comentario (id_posteo, id_usuario, contenido, fecha_creacion) VALUES (?, ?, ?, ?)",
        (id_posteo, empleado_id, contenido, fecha_creacion)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Comentario agregado correctamente"})

@posteos.route("/empleado/calificacion", methods=["POST"])
def agregar_calificacion():
    if "empleado_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    id_posteo = data.get("id_posteo")
    valor = int(data.get("valor"))
    empleado_id = session["empleado_id"]

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO calificacion (id_posteo, id_usuario, valor) VALUES (?, ?, ?)",
            (id_posteo, empleado_id, valor)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        return jsonify({"error": "Ya calificaste este posteo"}), 400
    finally:
        conn.close()

    return jsonify({"mensaje": "Calificación agregada correctamente"})


@posteos.route("/api/comentarios/<int:id_posteo>", methods=["GET"])
def listar_comentarios(id_posteo):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.contenido, e.usuario
        FROM comentario c
        JOIN empleado e ON c.id_usuario = e.id
        WHERE c.id_posteo = ?
        ORDER BY c.id DESC
    """, (id_posteo,))
    comentarios = cursor.fetchall()
    conn.close()

    return jsonify([{"contenido": c[0], "usuario": c[1]} for c in comentarios])


@posteos.route("/api/calificaciones/<int:id_posteo>", methods=["GET"])
def listar_calificaciones(id_posteo):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cal.valor, e.usuario
        FROM calificacion cal
        JOIN empleado e ON cal.id_usuario = e.id
        WHERE cal.id_posteo = ?
        ORDER BY cal.id DESC
    """, (id_posteo,))
    calificaciones = cursor.fetchall()
    conn.close()

    return jsonify([{"valor": c[0], "usuario": c[1]} for c in calificaciones])