import sqlite3

DB_PATH = "bdSistema.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn



def crear_tablas():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rol (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nombre_rol TEXT UNIQUE NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empleado (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            usuario TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contrasenia TEXT NOT NULL,
            id_rol INTEGER NOT NULL,
            FOREIGN KEY (id_rol) REFERENCES rol(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_general (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            empleado_id INTEGER NOT NULL,
            mensaje TEXT NOT NULL,
            fecha DATE NOT NULL,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_directo (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            remitente_id INTEGER NOT NULL,
            destinatario_id INTEGER NOT NULL,
            mensaje TEXT NOT NULL,
            fecha DATE NOT NULL,
            FOREIGN KEY (remitente_id) REFERENCES empleado(id),
            FOREIGN KEY (destinatario_id) REFERENCES empleado(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nombre TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensaje (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            contenido TEXT NOT NULL,
            fecha_envio DATE NOT NULL,
            id_usuario INTEGER NOT NULL,
            id_chat INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES empleado(id),
            FOREIGN KEY (id_chat) REFERENCES chat(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posteo (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_creacion DATE NOT NULL,
            empleado_id INTEGER NOT NULL,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentario (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            contenido TEXT NOT NULL,
            fecha_creacion DATE NOT NULL,
            id_usuario INTEGER NOT NULL,
            id_posteo INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES empleado(id),
            FOREIGN KEY (id_posteo) REFERENCES posteo(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calificacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            valor INTEGER NOT NULL CHECK(valor BETWEEN 1 AND 5),
            id_usuario INTEGER NOT NULL,
            id_posteo INTEGER NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES empleado(id),
            FOREIGN KEY (id_posteo) REFERENCES posteo(id)
            UNIQUE(id_usuario, id_posteo)
        );
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            empleado_id INTEGER NOT NULL,
            contacto_id INTEGER NOT NULL,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id),
            FOREIGN KEY (contacto_id) REFERENCES empleado(id),
            UNIQUE(empleado_id, contacto_id) -- evita duplicados
        );
    ''')

    conn.commit()
    conn.close()
    print("✅ Tablas creadas con éxito.")




def crear_roles():
    conn = get_db()
    cursor = conn.cursor()
    roles = ["Administrador", "Empleado", "Moderador"]
    for r in roles:
        try:
            cursor.execute("INSERT INTO rol (nombre_rol) VALUES (?)", (r,))
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()
    print("✅ Roles creados.")


def insertar_admin():
    conn = get_db()
    cursor = conn.cursor()
    usuario = "admin1"
    email = "admin@tecnologia.com"
    contrasenia = "admin12345"

    cursor.execute("SELECT id FROM rol WHERE nombre_rol = ?", ("Administrador",))
    rol_id = cursor.fetchone()
    if rol_id is None:
        print("❌ Error: ejecutá primero crear_roles()")
        conn.close()
        return

    try:
        cursor.execute("""
            INSERT INTO empleado (usuario, email, contrasenia, id_rol)
            VALUES (?, ?, ?, ?)
        """, (usuario, email, contrasenia, rol_id[0]))
        conn.commit()
        print("✅ Admin creado.")
    except sqlite3.IntegrityError:
        print("⚠️ El admin ya existe.")
    finally:
        conn.close()


if __name__ == "__main__":
    crear_tablas()
    crear_roles()
    insertar_admin()



#usuario = "admin1"
#   email = "admin@tecnologia.com"
#    contrasenia = "admin12345"


#usuario = "usuario1"
#   email = "usuario@tecnologia.com"
#    contrasenia = "usuario12345"


#usuario = "usuario2"
#   email = "usuario2@tecnologia.com"
#    contrasenia = "usuario12345"