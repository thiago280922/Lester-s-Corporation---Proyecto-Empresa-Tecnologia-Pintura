from flask import Blueprint, request, jsonify, render_template
from database.bd import get_db
from datetime import datetime

# 🔹 Definimos el blueprint con url_prefix
chat_directo_bp = Blueprint("chat_directo", __name__, url_prefix="/chat_directo")


# ==============================
# Renderizar página de chat directo
# ==============================
@chat_directo_bp.route("/<int:remitente_id>/<int:destinatario_id>")
def chat_directo(remitente_id, destinatario_id):
    return render_template(
        "chat_directo.html",
        remitente_id=remitente_id,
        destinatario_id=destinatario_id
    )


# ==============================
# Obtener mensajes entre 2 usuarios
# ==============================
@chat_directo_bp.route("/mensajes/<int:remitente_id>/<int:destinatario_id>", methods=["GET"])
def obtener_mensajes(remitente_id, destinatario_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT cd.id, cd.mensaje, cd.remitente_id, cd.destinatario_id, cd.fecha, e.usuario
        FROM chat_directo cd
        JOIN empleado e ON cd.remitente_id = e.id
        WHERE (cd.remitente_id = ? AND cd.destinatario_id = ?)
           OR (cd.remitente_id = ? AND cd.destinatario_id = ?)
        ORDER BY cd.fecha ASC
    """, (remitente_id, destinatario_id, destinatario_id, remitente_id))

    mensajes = [dict(m) for m in cursor.fetchall()]
    conn.close()

    return jsonify({"mensajes": mensajes})


# ==============================
# Enviar mensaje
# ==============================
@chat_directo_bp.route("/enviar", methods=["POST"])
def enviar_mensaje():
    data = request.get_json()

    remitente_id = data.get("remitente_id")
    destinatario_id = data.get("destinatario_id")
    mensaje = data.get("mensaje")

    if not remitente_id or not destinatario_id or not mensaje:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_directo (remitente_id, destinatario_id, mensaje, fecha)
        VALUES (?, ?, ?, ?)
    """, (remitente_id, destinatario_id, mensaje, datetime.now()))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "mensaje": mensaje})
