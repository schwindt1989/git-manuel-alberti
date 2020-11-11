from flask import Flask, render_template, request, session, escape
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, pre_load, validate
from utils import req
from werkzeug.security import generate_password_hash, check_password_hash


import os

dbdir ="sqlite:///" + os.path.abspath(os.getcwd())+ "/database.db"


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] =False

ma = Marshmallow(app)
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique = True, nullable=False)
    username = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(80),nullable=False)
    domicilio  = db.Column(db.String(80),nullable=False)
    telefono = db.Column(db.Integer)

    def __init__(self, email, username, password, domicilio, telefono):
        self.email = email
        self.username = username
        self.password = password
        self.domicilio = domicilio
        self.telefono = telefono

class UsuarioSchema(ma.ModelSchema):
    id = fields.Integer(dump_only=True)
    email = fields.String(required=True)
    username = fields.String()
    password = fields.String()
    domicilio = fields.String()
    telefono = fields.Integer()

usuarios_schema = UsuarioSchema(many=True)
usuario_schema = UsuarioSchema()

@app.route("/")
def home():
    return render_template("M.Alberti.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Usuario.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["username"] = user.username
            return "as logeado bien"
        return "vuelve a intentarlo."

    return render_template("login.html")

@app.route("/usuarios")
def usuarios():
    usuarios = Usuario.query.all()
    result = usuarios_schema.dump(usuarios)
    return {"status": "success", "data": result}, 201

@app.route('/usuarios/<int:id>')
def getProduct(id):
    usuario = Usuario.query.filter_by(id=int(id)).first()
    db.session.commit()
    result = usuario_schema.dump(usuario)

    return {"status":"success", "data":result}, 200

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        passwordsifrado =  generate_password_hash(request.form["password"], method="sha256")
        usuario = Usuario(email = request.form["email"],
        username = request.form["username"],
        password = passwordsifrado, 
        domicilio = request.form["domicilio"],
        telefono = request.form["telefono"])
        if usuario.email == None and usuario.password == None:
            return {
                'status': 'error',
                'message': 'Ooops!!! Te faltan completar uno o mas datos obligatorios'
            }
        db.session.add(usuario)
        db.session.commit()
        result = usuario_schema.dump(usuario)

    
        return render_template("login.html")
    return render_template("signup.html")


@app.route("/editar/<int:id>",  methods=["PUT"])
def editar(id):
    usuario = Usuario.query.filter_by(id= int(id)).first()
    if usuario is None:
        return{
            'status':'error',
            'mensage': 'no se ha encontrado'
        }
    username = req.getJsonField("username")
    telefono = req.getJsonField("telefono")
    domicilio = req.getJsonField("domicilio")

    if username is not None:
        usuario.username = username

    if telefono is not None:
        usuario.telefono = telefono

    if domicilio is not None:
        usuario.domicilio = domicilio
    db.session.add(usuario)
    db.session.commit()
    result = usuario_schema.dump(usuario)
    return {"status":"success", "data":result}, 200

@app.route ('/products/<int:id>', methods=['DELETE'])
def delete(id):
    product = Products.query.filter_by(id=int(id)).delete()
    db.session.commit()
    usuarios = Products.query.all()
    result = products_schema.dump(usuarios)

    return {"status":"success", "data":result}, 200

app.secret_key = "12345"
   
@app.route("/locales")
def locales():
    return render_template("locales.html")

@app.route("/servicio")
def servicio():
    return render_template("servicio.html")

@app.route("/preguntas")
def preguntas():
    return render_template("preguntas.html")

@app.route("/verduleria")
def verduleria():
    return render_template("verduleria.html")

@app.route("/peluqueria")
def peluqueria():
    return render_template("peluqueria.html")

@app.route("/celulares")
def celulares():
    return render_template("celulares.html")

@app.route("/perfumeria")
def perfumeria():
    return render_template("perfumeria.html")

if __name__ == "__main__":
    app.run (debug=True,port=4000)