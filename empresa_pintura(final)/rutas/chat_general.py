from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from database.bd import get_db

chat_general_bp = Blueprint("chat_general", __name__, template_folder="templates")

# ================================
# CHAT GENERAL
# ================================
@chat_general_bp.route("/chat")
def chat():
    if "empleado_id" not in session:
        return redirect(url_for("login.login"))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.mensaje, c.fecha, e.usuario
        FROM chat_general c
        JOIN empleado e ON c.empleado_id = e.id
        ORDER BY c.fecha ASC
    """)
    mensajes = cursor.fetchall()
    conn.close()

 
    return render_template("chat.html", mensajes=mensajes, empleado_id=session["empleado_id"])



@chat_general_bp.route("/chat/enviar", methods=["POST"])
def enviar():
    if "empleado_id" not in session:
        return jsonify({"error": "No logueado"}), 403

    data = request.json
    texto = data.get("mensaje", "").strip()

    if not texto:
        return jsonify({"error": "Mensaje vacío"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_general (empleado_id, mensaje, fecha) VALUES (?, ?, datetime('now'))",
        (session["empleado_id"], texto)
    )
    conn.commit()
    conn.close()

    return jsonify({"ok": True})


@chat_general_bp.route("/chat/mensajes", methods=["GET"])
def obtener_mensajes_general():
    if "empleado_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.mensaje, c.fecha, e.usuario
        FROM chat_general c
        JOIN empleado e ON c.empleado_id = e.id
        ORDER BY c.fecha ASC
    """)
    mensajes = cursor.fetchall()
    conn.close()

    mensajes_json = [
        {
            "mensaje": m["mensaje"],
            "fecha": m["fecha"],
            "usuario": m["usuario"]
        } for m in mensajes
    ]

    return jsonify(mensajes_json)


# ================================
# CONTACTOS
# ================================


@chat_general_bp.route("/buscar_empleado")
def buscar_empleado():
    if "empleado_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    query = request.args.get("id", "").strip()
    if not query:
        return jsonify({"error": "Falta parámetro de búsqueda"}), 400

    conn = get_db()
    cursor = conn.cursor()

    # 🔹 Buscar por usuario o por email (sin el @tecnologia.com)
    cursor.execute("""
        SELECT id, usuario, email
        FROM empleado
        WHERE usuario LIKE ?
           OR email LIKE ? 
    """, (f"%{query}%", f"%{query}@tecnologia.com"))
    
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Empleado no encontrado"})

    return jsonify({
        "id": row["id"],
        "usuario": row["usuario"],
        "email": row["email"]
    })


@chat_general_bp.route("/contactos/agregar", methods=["POST"])
def agregar_contacto():
    if "empleado_id" not in session:
        return jsonify({"error": "No logueado"}), 403

    data = request.json
    contacto_id = data.get("contacto_id")

    if not contacto_id:
        return jsonify({"error": "Falta contacto_id"}), 400

    db = get_db()
    cursor = db.cursor()

    # Verificar que exista
    cursor.execute("SELECT id FROM empleado WHERE id = ?", (contacto_id,))
    if not cursor.fetchone():
        return jsonify({"error": "Empleado no existe"}), 404

    # Verificar duplicado
    cursor.execute("""
        SELECT 1 FROM contactos 
        WHERE empleado_id = ? AND contacto_id = ?
    """, (session["empleado_id"], contacto_id))
    if cursor.fetchone():
        return jsonify({"error": "Ya lo tienes agregado"}), 400

    # Insertar
    cursor.execute("""
        INSERT INTO contactos (empleado_id, contacto_id) VALUES (?, ?)
    """, (session["empleado_id"], contacto_id))
    db.commit()

    return jsonify({"ok": True, "mensaje": "Contacto agregado"})


@chat_general_bp.route("/contactos", methods=["GET"])
def listar_contactos():
    if "empleado_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    db = get_db()
    cursor = db.cursor()

    # Listar SOLO los contactos agregados por el usuario
    cursor.execute("""
        SELECT e.id, e.usuario
        FROM contactos c
        JOIN empleado e ON e.id = c.contacto_id
        WHERE c.empleado_id = ?
    """, (session["empleado_id"],))

    contactos = [
        {"id": row["id"], "usuario": row["usuario"]}
        for row in cursor.fetchall()
    ]

    return jsonify(contactos)
