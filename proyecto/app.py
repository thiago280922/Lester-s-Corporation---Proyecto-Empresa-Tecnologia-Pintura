import re
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,session 
from datetime import datetime
# =========================
# CONFIG
# =========================
app = Flask(__name__)
app.secret_key = "super_clave_secreta"  # cambiar en producción
DB_PATH = "bdSistemaDeStock.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["POST"])
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
        session["rol"] = user["id_rol"]  # guarda el rol como número
        return jsonify({"mensaje": f"Bienvenido {user['nombre']}!"})
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401


# =========================
# ADMINISTRADOR - USUARIOS
# =========================
@app.route("/admin/usuario", methods=["POST"])
def crear_usuario():
    data = request.json
    dni = data.get("dni")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    telefono = data.get("telefono")
    email = data.get("email")
    password = data.get("password")
    rol_id = data.get("id_rol")

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuario (dni, nombre, apellido, telefono, contrasenia, email, id_rol)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (dni, nombre, apellido, telefono, password, email, rol_id))
        conn.commit()
        return jsonify({"mensaje": f"Usuario {nombre} creado correctamente"})
    except sqlite3.IntegrityError as e:
        return jsonify({"error": f"Error al crear usuario: {str(e)}"}), 400
    finally:
        conn.close()


@app.route("/admin/usuario/<int:id_usuario>", methods=["PUT"])
def editar_usuario(id_usuario):
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    rol_id = data.get("id_rol")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuario SET nombre=?, apellido=?, email=?, id_rol=? WHERE id=?
    """, (nombre, apellido, email, rol_id, id_usuario))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Usuario {id_usuario} actualizado correctamente"})


@app.route("/admin/usuario/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuario WHERE id=?", (id_usuario,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Usuario {id_usuario} eliminado correctamente"})


# =========================
# ADMINISTRADOR - ROLES
# =========================
@app.route("/admin/rol", methods=["POST"])
def crear_rol():
    data = request.json
    nombre_rol = data.get("nombre_rol")

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO rol (nombre_rol) VALUES (?)", (nombre_rol,))
        conn.commit()
        return jsonify({"mensaje": f"Rol {nombre_rol} creado correctamente"})
    except sqlite3.IntegrityError:
        return jsonify({"error": f"El rol {nombre_rol} ya existe"}), 400
    finally:
        conn.close()


@app.route("/admin/rol/<int:id_rol>", methods=["DELETE"])
def eliminar_rol(id_rol):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM usuario WHERE id_rol=?", (id_rol,))
    count = cursor.fetchone()["count"]
    if count > 0:
        conn.close()
        return jsonify({"error": "No se puede eliminar un rol asignado a usuarios"}), 400

    cursor.execute("DELETE FROM rol WHERE id=?", (id_rol,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Rol {id_rol} eliminado correctamente"})


# =========================
# CHAT
# =========================
@app.route("/empleado/mensaje", methods=["POST"])
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


@app.route("/empleado/mensajes/<int:id_chat>")
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


# =========================
# POSTEOS
# =========================
@app.route("/empleado/posteo", methods=["POST"])
def crear_posteo():
    if "usuario_id" not in session:
        return jsonify({"error": "No autorizado"}), 403

    data = request.json
    titulo = data.get("titulo")
    descripcion = data.get("descripcion")
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


@app.route("/empleado/posteos")
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


# =========================
# COMENTARIOS
# =========================
@app.route("/empleado/comentario", methods=["POST"])
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


# =========================
# MENSAJES (Editar / Eliminar)
# =========================
@app.route("/empleado/mensaje/<int:id_mensaje>", methods=["PUT"])
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


@app.route("/empleado/mensaje/<int:id_mensaje>", methods=["DELETE"])
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


# =========================
# CALIFICACIÓN
# =========================
@app.route("/empleado/calificacion", methods=["POST"])
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


# =========================
# MODERADOR
# =========================
@app.route("/moderador/mensaje/<int:id_mensaje>", methods=["DELETE"])
def moderador_eliminar_mensaje(id_mensaje):
    if "usuario_id" not in session or session.get("rol") != 2:  # supongamos rol=2 es moderador
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


@app.route("/moderador/posteo/<int:id_posteo>", methods=["DELETE"])
def moderador_eliminar_posteo(id_posteo):
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


@app.route("/moderador/comentario/<int:id_comentario>", methods=["DELETE"])
def moderador_eliminar_comentario(id_comentario):
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


# -------------------------------
# RUTAS CHAT GENERAL
# -------------------------------

@app.route("/chat_general", methods=["GET", "POST"])
def chat_general():
    conn = get_db_connection()

    if request.method == "POST":
        empleado_id = request.form["empleado_id"]
        mensaje = request.form["mensaje"]

        conn.execute(
            "INSERT INTO chat_general (empleado_id, mensaje, fecha) VALUES (?, ?, ?)",
            (empleado_id, mensaje, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        flash("Mensaje enviado al chat general.", "success")

    mensajes = conn.execute("""
        SELECT cg.id, e.nombre || ' ' || e.apellido AS autor, cg.mensaje, cg.fecha
        FROM chat_general cg
        JOIN empleado e ON e.id = cg.empleado_id
        ORDER BY cg.fecha DESC
    """).fetchall()
    conn.close()

    return render_template("chat_general.html", mensajes=mensajes)


# -------------------------------
# RUTAS CHAT DIRECTO
# -------------------------------

@app.route("/chat_directo/<int:remitente_id>/<int:destinatario_id>", methods=["GET", "POST"])
def chat_directo(remitente_id, destinatario_id):
    conn = get_db_connection()

    if request.method == "POST":
        mensaje = request.form["mensaje"]

        conn.execute(
            "INSERT INTO chat_directo (remitente_id, destinatario_id, mensaje, fecha) VALUES (?, ?, ?, ?)",
            (remitente_id, destinatario_id, mensaje, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        flash("Mensaje enviado.", "success")

    mensajes = conn.execute("""
        SELECT cd.id, 
               r.nombre || ' ' || r.apellido AS remitente,
               d.nombre || ' ' || d.apellido AS destinatario,
               cd.mensaje, cd.fecha
        FROM chat_directo cd
        JOIN empleado r ON r.id = cd.remitente_id
        JOIN empleado d ON d.id = cd.destinatario_id
        WHERE (cd.remitente_id = ? AND cd.destinatario_id = ?)
           OR (cd.remitente_id = ? AND cd.destinatario_id = ?)
        ORDER BY cd.fecha DESC
    """, (remitente_id, destinatario_id, destinatario_id, remitente_id)).fetchall()

    conn.close()
    return render_template("chat_directo.html", mensajes=mensajes, remitente_id=remitente_id, destinatario_id=destinatario_id)



# RUTA MODERACIÓN (BORRAR MENSAJES)


@app.route("/borrar_mensaje/<string:tipo>/<int:mensaje_id>", methods=["POST"])
def borrar_mensaje(tipo, mensaje_id):
    conn = get_db_connection()

    if tipo == "general":
        conn.execute("DELETE FROM chat_general WHERE id = ?", (mensaje_id,))
    elif tipo == "directo":
        conn.execute("DELETE FROM chat_directo WHERE id = ?", (mensaje_id,))
    conn.commit()
    conn.close()

    flash("Mensaje eliminado correctamente.", "warning")
    return redirect(request.referrer or url_for("chat_general"))


if __name__ == "__main__":
    app.run(debug=True)
