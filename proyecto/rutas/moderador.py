from flask import Blueprint, request, session, jsonify
from database.bd import get_db

moderador = Blueprint('moderador', __name__)

# Elimina un mensaje (chat general o directo)
@moderador.route("/moderador/mensaje/<int:id_mensaje>", methods=["DELETE"])
def eliminar_mensaje(id_mensaje):
    if "usuario_id" not in session or session.get("rol") != 2:
        return jsonify({"error": "No autorizado"}), 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensaje WHERE id = ?", (id_mensaje,))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Mensaje no encontrado"}), 404
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Mensaje eliminado por moderador"})

# Elimina un posteo
@moderador.route("/moderador/posteo/<int:id_posteo>", methods=["DELETE"])
def eliminar_posteo(id_posteo):
    if "usuario_id" not in session or session.get("rol") != 2:
        return jsonify({"error": "No autorizado"}), 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posteo WHERE id = ?", (id_posteo,))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Posteo no encontrado"}), 404
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Posteo eliminado por moderador"})

# Elimina un comentario
@moderador.route("/moderador/comentario/<int:id_comentario>", methods=["DELETE"])
def eliminar_comentario(id_comentario):
    if "usuario_id" not in session or session.get("rol") != 2:
        return jsonify({"error": "No autorizado"}), 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comentario WHERE id = ?", (id_comentario,))
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Comentario no encontrado"}), 404
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Comentario eliminado por moderador"})
