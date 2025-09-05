from flask import Flask
from rutas.login import login_bp
from rutas.admin import admin_bp
from rutas.posteos import posteos
from rutas.moderador import moderador
from rutas.chat import chat
from database.bd import get_db, init_db
from datetime import datetime
app = Flask(__name__)
app.secret_key = "super_clave_secreta"

# Registrar Blueprints
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(posteos)
app.register_blueprint(moderador)
app.register_blueprint(chat)

if __name__ == "__main__":
    app.run(debug=True)


