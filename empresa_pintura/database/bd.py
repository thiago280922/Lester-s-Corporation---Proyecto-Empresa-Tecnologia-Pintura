import sqlite3

conn = sqlite3.connect("bdSistema.db")
cursor = conn.cursor()

# Tabla de roles
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rol (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre_rol TEXT UNIQUE NOT NULL
    );
''')
conn.commit()

# Tabla de empleados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS empleado (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        dni TEXT UNIQUE NOT NULL,
        telefono TEXT,
        email TEXT UNIQUE NOT NULL,
        contrasenia TEXT NOT NULL,
        id_rol INTEGER NOT NULL,
        FOREIGN KEY (id_rol) REFERENCES rol(id)
    );
''')
conn.commit()

# Chat general
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat_general (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        empleado_id INTEGER NOT NULL,
        mensaje TEXT NOT NULL,
        fecha DATE NOT NULL,
        FOREIGN KEY (empleado_id) REFERENCES empleado(id)
    );
''')
conn.commit()

# Chat directo
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
conn.commit()

# Chats grupales o privados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre TEXT
    );
''')
conn.commit()

# Mensajes dentro de un chat
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
conn.commit()

# Posteos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posteo (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        fecha_creacion DATE NOT NULL,
        id_usuario INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES empleado(id)
    );
''')
conn.commit()

# Comentarios en posteos
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
conn.commit()

# Calificaciones en posteos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS calificacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        valor INTEGER NOT NULL CHECK(valor BETWEEN 1 AND 5),
        id_usuario INTEGER NOT NULL,
        id_posteo INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES empleado(id),
        FOREIGN KEY (id_posteo) REFERENCES posteo(id)
    );
''')
conn.commit()

print("✅ Tablas creadas con éxito")
conn.close()
