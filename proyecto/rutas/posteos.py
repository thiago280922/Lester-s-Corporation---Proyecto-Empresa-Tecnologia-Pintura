from flask import Blueprint, request, jsonify, session
from database.bd import get_db

posteos = Blueprint('posteos', __name__)

@posteos.route("/empleado/posteo", methods=["POST"])
def crear_posteo():
    if "usuario_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")  # esto sería el link de GitHub
    id_usuario = session["usuario_id"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posteo (titulo, descripcion, id_usuario) VALUES (?, ?, ?)",
        (titulo, descripcion, id_usuario)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Posteo creado correctamente"})

@posteos.route("/empleado/posteos")
def listar_posteos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.titulo, p.descripcion, p.fecha_creacion, u.nombre, u.apellido
        FROM posteo p
        JOIN usuario u ON p.id_usuario = u.id
        ORDER BY p.fecha_creacion DESC
    """)
    posteos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"posteos": posteos})

@posteos.route("/empleado/comentario", methods=["POST"])
def agregar_comentario():
    if "usuario_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    id_posteo = data.get("id_posteo")
    contenido = data.get("contenido")
    id_usuario = session["usuario_id"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comentario (id_posteo, id_usuario, contenido) VALUES (?, ?, ?)",
        (id_posteo, id_usuario, contenido)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Comentario agregado correctamente"})

@posteos.route("/empleado/calificacion", methods=["POST"])
def agregar_calificacion():
    if "usuario_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    id_posteo = data.get("id_posteo")
    valor = int(data.get("valor"))
    id_usuario = session["usuario_id"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO calificacion (id_posteo, id_usuario, valor) VALUES (?, ?, ?)",
        (id_posteo, id_usuario, valor)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Calificación agregada correctamente"})
