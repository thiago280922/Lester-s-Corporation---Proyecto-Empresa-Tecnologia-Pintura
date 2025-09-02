import sqlite3

conn = sqlite3.connect("bdSistemaDeStock.db")
cursor = conn.cursor()

# TABLA ROL
cursor.execute("""
    CREATE TABLE IF NOT EXISTS rol (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre_rol TEXT NOT NULL
    );
""")

# TABLA USUARIO
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        dni INTEGER UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        telefono INTEGER NOT NULL,
        contrasenia TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        id_rol INTEGER NOT NULL,
        FOREIGN KEY (id_rol) REFERENCES rol(id)
    );
""")

# TABLA POSTEO
cursor.execute("""
    CREATE TABLE IF NOT EXISTS posteo (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        id_usuario INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    );
""")

# TABLA COMENTARIO
cursor.execute("""
    CREATE TABLE IF NOT EXISTS comentario (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        contenido TEXT NOT NULL,
        fecha_creacion DATE NOT NULL,
        id_usuario INTEGER NOT NULL,
        id_posteo INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id),
        FOREIGN KEY (id_posteo) REFERENCES posteo(id)
    );
""")

# TABLA CALIFICACION
cursor.execute("""
    CREATE TABLE IF NOT EXISTS calificacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        valor INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        id_posteo INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id),
        FOREIGN KEY (id_posteo) REFERENCES posteo(id)
    );
""")

# TABLA CHAT
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre_chat TEXT NOT NULL,
        tipo TEXT NOT NULL,
        fecha_creacion DATE NOT NULL
    );
""")

# TABLA USUARIO_CHAT
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario_chat (
        id_usuario INTEGER NOT NULL,
        id_chat INTEGER NOT NULL,
        PRIMARY KEY (id_usuario, id_chat),
        FOREIGN KEY (id_usuario) REFERENCES usuario(id),
        FOREIGN KEY (id_chat) REFERENCES chat(id)
    );
""")

# TABLA MENSAJE
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mensaje (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        contenido TEXT NOT NULL,
        fecha_envio DATE NOT NULL,
        id_usuario INTEGER NOT NULL,
        id_chat INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id),
        FOREIGN KEY (id_chat) REFERENCES chat(id)
    );
""")

conn.commit()
conn.close()
