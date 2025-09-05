from flask import Blueprint, request, session, jsonify
import re
from database.bd import get_db

login_bp = Blueprint('login', __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email", "")
    password = data.get("password", "")

    if not re.match(r"^[\w\.-]+@tecnologia\.com$", email):
        return jsonify({"error": "El correo debe ser corporativo (@tecnologia.com)"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE email=? AND contrasenia=?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session["usuario_id"] = user["id"]
        session["rol"] = user["id_rol"]
        return jsonify({"mensaje": f"Bienvenido {user['nombre']}!"})
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401