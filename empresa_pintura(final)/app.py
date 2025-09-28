from flask import Flask, render_template, redirect, url_for, session
from rutas.login import login_bp
from rutas.admin import admin_bp
from rutas.moderador import moderador
from rutas.posteos import posteos
from rutas.chat_general import chat_general_bp
from rutas.chat_directo import chat_directo_bp

app = Flask(__name__)
app.secret_key = "super_clave_secreta"

# Blueprints
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(moderador)
app.register_blueprint(posteos)
app.register_blueprint(chat_general_bp)
app.register_blueprint(chat_directo_bp)

@app.route("/")
def inicio():
    return render_template("registro.html")

@app.route("/interseccion")
def interseccion():
    return render_template("interseccion.html")

if __name__ == "__main__":
    app.run(debug=True)
