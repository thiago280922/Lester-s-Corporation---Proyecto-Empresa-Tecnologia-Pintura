from flask import Blueprint, request, session, jsonify, render_template, redirect, url_for, flash
import re
from database.bd import get_db

login_bp = Blueprint('login', __name__)

# -------- LOGIN --------
@login_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("login.html")


@login_bp.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not re.match(r"^[\w\.-]+@tecnologia\.com$", email):
        flash("El correo debe ser corporativo (@tecnologia.com)", "error")
        return redirect(url_for('login.login_form'))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT e.id, e.usuario, e.email, e.contrasenia, e.id_rol, r.nombre_rol 
        FROM empleado e
        JOIN rol r ON e.id_rol = r.id
        WHERE e.email=? AND e.contrasenia=?
    """, (email, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        session["empleado_id"] = user["id"]
        session["email"] = user["email"]
        session["rol"] = user["nombre_rol"]
        session["id_rol"] = user["id_rol"]

        if user["id_rol"] == 1:
            return render_template("admin.html", email=user["email"])
        elif user["id_rol"] == 2:
            return render_template("interseccion.html", email=user["email"])
        elif user["id_rol"] == 3:
            return render_template("interseccion.html", email=user["email"])
        else:
            flash("Rol desconocido.", "error")
            return redirect(url_for('login.login_form'))

    flash("Usuario o contraseña incorrectos", "error")
    return redirect(url_for('login.login_form'))



# -------- REGISTRO --------
@login_bp.route("/registro", methods=["GET"])
def registro_form():
    return render_template("registro.html")

@login_bp.route("/registro", methods=["POST"])
def registro():
    usuario = request.form.get("usuario", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not usuario or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if not re.match(r"^[\w\.-]+@tecnologia\.com$", email):
        return jsonify({"error": "El correo debe ser corporativo (@tecnologia.com)"}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Verificar que no exista
    cursor.execute("SELECT id FROM empleado WHERE email=?", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "El email ya está registrado"}), 400

    # Insertar con rol empleado (id_rol = 3)
    cursor.execute("""
        INSERT INTO empleado (usuario, email, contrasenia, id_rol)
        VALUES (?, ?, ?, ?)
    """, (usuario, email, password, 3))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 200