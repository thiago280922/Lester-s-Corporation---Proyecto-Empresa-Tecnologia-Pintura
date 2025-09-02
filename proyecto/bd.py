import sqlite3

conn = sqlite3.connect('bdSistema.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS rol (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre_rol TEXT NOT NULL
    );
''')
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        dni INTEGER UNIQUE NOT NULL,
        telefono INTEGER NOT NULL,
        email TEXT NOT NULL,
        contrasenia TEXT NOT NULL,
        id_rol INTEGER NOT NULL,
        FOREIGN KEY (id_rol) REFERENCES rol(id)
    );
''')
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        nombre_chat TEXT NOT NULL,
        fecha_creacion DATE NOT NULL
    );
''')
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS mensaje (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        contenido TEXT NOT NULL,
        fecha_envio DATE NOT NULL,
        id_usuario INTEGER NOT NULL,
        id_chat INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id),
        FOREIGN KEY (id_chat) REFERENCES chat(id)
    );
''')
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS posteo (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        fecha_creacion DATE NOT NULL,
        id_usuario INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    );
''')
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS comentario (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        contenido TEXT NOT NULL,
        fecha_creacion DATE NOT NULL,
        id_usuario INTEGER NOT NULL,
        id_posteo INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id),
        FOREIGN KEY (id_posteo) REFERENCES posteo(id)
    );
''')
conn.commit()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS calificacion (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        valor INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        id_posteo INTEGER NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id),
        FOREIGN KEY (id_posteo) REFERENCES posteo(id)
    );
''')
conn.commit()

print("Base de datos creada con éxito")
conn.close()
