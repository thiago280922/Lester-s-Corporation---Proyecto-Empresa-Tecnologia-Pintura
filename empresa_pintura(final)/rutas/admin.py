from flask import Blueprint, request, jsonify, session
from functools import wraps
from database.bd import get_db

admin_bp = Blueprint('admin', __name__)

# ✅ Decorador para validar si es administrador
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("id_rol") != 1:  # Rol 1 = administrador
            return jsonify({"error": "No autorizado"}), 403
        return f(*args, **kwargs)
    return wrapper

# === EMPLEADOS ===
@admin_bp.route("/admin/usuario", methods=["POST"])
@admin_required
def crear_empleado():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO empleado (usuario, email, contrasenia, id_rol)
            VALUES (?, ?, ?, ?)
        """, (
            data.get("usuario"),
            data.get("email"),
            data.get("contrasenia"),
            data.get("id_rol")
        ))
        conn.commit()
        return jsonify({"mensaje": f"Empleado {data.get('usuario')} creado correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@admin_bp.route("/admin/usuario/<int:id_empleado>", methods=["PUT"])
@admin_required
def editar_empleado(id_empleado):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE empleado SET usuario=?, email=?, contrasenia=?, id_rol=? WHERE id=?
    """, (
        data.get("usuario"),
        data.get("email"),
        data.get("contrasenia"),
        data.get("id_rol"),
        id_empleado
    ))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Empleado {id_empleado} actualizado correctamente"})


@admin_bp.route("/admin/usuario/<int:id_empleado>", methods=["DELETE"])
@admin_required
def eliminar_empleado(id_empleado):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleado WHERE id=?", (id_empleado,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Empleado {id_empleado} eliminado correctamente"})


# === ROLES ===
@admin_bp.route("/admin/rol", methods=["POST"])
@admin_required
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
@admin_required
def eliminar_rol(id_rol):
    conn = get_db()
    cursor = conn.cursor()
    # Verificar si hay empleados con ese rol
    cursor.execute("SELECT COUNT(*) as cantidad FROM empleado WHERE id_rol=?", (id_rol,))
    if cursor.fetchone()["cantidad"] > 0:
        conn.close()
        return jsonify({"error": "No se puede eliminar un rol asignado a empleados"}), 400

    cursor.execute("DELETE FROM rol WHERE id=?", (id_rol,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": f"Rol {id_rol} eliminado correctamente"})
