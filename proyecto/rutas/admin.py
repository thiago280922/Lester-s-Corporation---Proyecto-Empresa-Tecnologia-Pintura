from flask import Blueprint, request, jsonify
from database.bd import get_db

admin_bp = Blueprint('admin', __name__)

# === Usuarios ===
@admin_bp.route("/admin/usuario", methods=["POST"])
def crear_usuario():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO usuario (dni, nombre, apellido, telefono, contrasenia, email, id_rol)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("dni"), data.get("nombre"), data.get("apellido"), data.get("telefono"),
            data.get("password"), data.get("email"), data.get("id_rol")
        ))
        conn.commit()
        return jsonify({"mensaje": f"Usuario {data.get('nombre')} creado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

@admin_bp.route("/admin/usuario/<int:id_usuario>", methods=["PUT"])
def editar_usuario(id_usuario):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE usuario SET nombre=?, apellido=?, email=?, id_rol=? WHERE id=?
    """, (
        data.get("nombre"), data.get("apellido"), data.get("email"),
        data.get("id_rol"), id_usuario
    ))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Usuario {id_usuario} actualizado correctamente"})

@admin_bp.route("/admin/usuario/<int:id_usuario>", methods=["DELETE"])
def eliminar_usuario(id_usuario):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuario WHERE id=?", (id_usuario,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Usuario {id_usuario} eliminado correctamente"})

# === Roles ===
@admin_bp.route("/admin/rol", methods=["POST"])
def crear_rol():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO rol (nombre_rol) VALUES (?)", (data.get("nombre_rol"),))
        conn.commit()
        return jsonify({"mensaje": f"Rol {data.get('nombre_rol')} creado correctamente"})
    except:
        return jsonify({"error": f"El rol ya existe"}), 400
    finally:
        conn.close()

@admin_bp.route("/admin/rol/<int:id_rol>", methods=["DELETE"])
def eliminar_rol(id_rol):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM usuario WHERE id_rol=?", (id_rol,))
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return jsonify({"error": "No se puede eliminar un rol asignado a usuarios"}), 400
    cursor.execute("DELETE FROM rol WHERE id=?", (id_rol,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Rol {id_rol} eliminado correctamente"})