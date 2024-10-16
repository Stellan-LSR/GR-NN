from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'samuel444'
app.config['MYSQL_DB'] = 'vitivinicultura'

mysql = MySQL(app)

@app.route('/')
def inicio():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Usuarios WHERE email = %s AND contraseña = %s", (email, contraseña))
        usuario = cur.fetchone()
        cur.close()
        if usuario:
            return redirect(url_for('index', nombre=usuario[1]))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contraseña = request.form['contraseña']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Usuarios (nombre, email, contraseña) VALUES (%s, %s, %s)", (nombre, email, contraseña))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/index/<nombre>')
def index(nombre):
    return render_template('index.html', nombre=nombre)

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
