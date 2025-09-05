from flask import Blueprint, request, session, jsonify
from database.bd import get_db

chat = Blueprint("chat", __name__)

# Enviar mensaje (empleado)
@chat.route("/empleado/mensaje", methods=["POST"])
def enviar_mensaje():
    if "usuario_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    id_chat = data.get("id_chat")
    contenido = data.get("contenido")
    id_usuario = session["usuario_id"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mensaje (id_chat, id_usuario, contenido) VALUES (?, ?, ?)",
        (id_chat, id_usuario, contenido)
    )
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Mensaje enviado correctamente"})

# Obtener mensajes de un chat
@chat.route("/empleado/mensajes/<int:id_chat>")
def obtener_mensajes(id_chat):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.contenido, m.fecha_envio, u.nombre, u.apellido
        FROM mensaje m
        JOIN usuario u ON m.id_usuario = u.id
        WHERE m.id_chat=? ORDER BY m.fecha_envio ASC
    """, (id_chat,))
    mensajes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"mensajes": mensajes})

# Editar mensaje propio
@chat.route("/empleado/mensaje/<int:id_mensaje>", methods=["PUT"])
def editar_mensaje(id_mensaje):
    if "usuario_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    nuevo_contenido = data.get("contenido")
    id_usuario = session["usuario_id"]

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE mensaje SET contenido = ? WHERE id = ? AND id_usuario = ?",
        (nuevo_contenido, id_mensaje, id_usuario)
    )
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Mensaje no encontrado o no autorizado"}), 403

    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Mensaje editado correctamente"})

# Eliminar mensaje propio
@chat.route("/empleado/mensaje/<int:id_mensaje>", methods=["DELETE"])
def eliminar_mensaje(id_mensaje):
    if "usuario_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    id_usuario = session["usuario_id"]
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensaje WHERE id = ? AND id_usuario = ?", (id_mensaje, id_usuario))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Mensaje no encontrado o no autorizado"}), 403

    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Mensaje eliminado correctamente"})
