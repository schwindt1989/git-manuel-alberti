from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("M.Alberti.html")

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