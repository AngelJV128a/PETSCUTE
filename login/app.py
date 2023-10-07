# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = '146.190.218.21'
app.config['MYSQL_USER'] = 'firulais'
app.config['MYSQL_PASSWORD'] = '1D8DE81DJ7nMtgny'
app.config['MYSQL_DB'] = 'petscue_sql'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'correo' in request.form and 'contrasenia' in request.form:
		correo = request.form['correo']
		contrasenia = request.form['contrasenia']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM usuarios WHERE correo = % s AND contrasenia = % s', (correo, contrasenia, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['idUsuario'] = account['id']
			session['nombre'] = account['nombre']
			session['apellido'] = account['apellido']
			session['correo'] = account['correo']
			session['nombreusuario'] = account['nickname']
			msg = 'Inicio de sesion exitoso !'
			return redirect(url_for('menu', msg=msg))
		else:
			msg = 'Correo o contraseña incorrectos !'
	return render_template('login2.html', msg = msg)

@app.route('/menu', methods =['GET', 'POST'])
def menu():
	return render_template('menu2.html')

@app.route('/profile', methods =['GET', 'POST'])
def profile():
	msg = ''
	if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'correo' in request.form and 'nombreusuario' in request.form and 'contrasenia1' in request.form and 'contrasenia2' in request.form:
		nombre = request.form['nombre']
		apellido = request.form['apellido']
		correo = request.form['correo']
		nombreusuario = request.form['nombreusuario']
		contrasenia1 = request.form['contrasenia1']
		contrasenia2 = request.form['contrasenia2']
		idActual = session['idUsuario']
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM usuarios WHERE nickname = % s and id <> % s', (nombreusuario, idActual, ))
		account1 = cursor.fetchone()
		cursor.execute('SELECT * FROM usuarios WHERE nombre = % s and apellido = % s and id <> % s', (nombre, apellido, idActual, ))
		account2 = cursor.fetchone()
		cursor.execute('SELECT * FROM usuarios WHERE correo = % s and id <> % s', (correo, idActual, ))
		account3 = cursor.fetchone()
		if account1:
			msg = 'Este nombre de usuario ya existe !'
		elif account2:
			msg = 'Nombre y Apellidos ya existentes !'
		elif account3:
			msg = 'Correo ya existente !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
			msg = 'Correo invalido !'
		elif not re.match(r'[A-Za-z0-9]+', nombreusuario):
			msg = 'El nombre de usuario solo debe contener letras y numeros !'
		elif not re.match(r'[A-Za-z0-9]+', nombre):
			msg = 'El nombre solo debe contener letras !'
		elif not nombre or not apellido or not nombreusuario or not correo or not contrasenia1 or not contrasenia2:
			msg = 'Por favor llene el formulario !'
		elif contrasenia1 != contrasenia2:
			msg = 'Contraseñas no coinciden !'
		else:
			cursor.execute('UPDATE usuarios SET nombre = % s, apellido = % s, correo = % s, nickname = % s, contrasenia = % s WHERE id = % s', (nombre, apellido, correo, nombreusuario, contrasenia1, idActual, ))
			mysql.connection.commit()
			session['nombre'] = nombre
			session['apellido'] = apellido
			session['correo'] = correo
			session['nombreusuario'] = nombreusuario
	elif request.method == 'POST':
		msg = 'No ha puesto nada para cambiar !'
	return render_template('perfil.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('idUsuario', None)
	session.pop('correo', None)
	session.pop('nombreusuario', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'nombre' in request.form and 'apellido' in request.form and 'nombreusuario' in request.form and 'contrasenia' in request.form and 'correo' in request.form :
		nombre = request.form['nombre']
		apellido = request.form['apellido']
		nombreusuario = request.form['nombreusuario']
		contrasenia = request.form['contrasenia']
		correo = request.form['correo']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM usuarios WHERE nickname = % s', (nombreusuario, ))
		account1 = cursor.fetchone()
		cursor.execute('SELECT * FROM usuarios WHERE nombre = % s and apellido = % s', (nombre, apellido, ))
		account2 = cursor.fetchone()
		cursor.execute('SELECT * FROM usuarios WHERE correo = % s', (correo, ))
		account3 = cursor.fetchone()
		if account1:
			msg = 'Este nombre de usuario ya existe !'
		elif account2:
			msg = 'Nombre y Apellidos ya existentes !'
		elif account3:
			msg = 'Correo ya existente !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', correo):
			msg = 'Correo invalido !'
		elif not re.match(r'[A-Za-z0-9]+', nombreusuario):
			msg = 'El nombre de usuario solo debe contener letras y numeros !'
		elif not re.match(r'[A-Za-z0-9]+', nombre):
			msg = 'El nombre solo debe contener letras !'
		elif not nombre or not apellido or not nombreusuario or not contrasenia or not correo:
			msg = 'Por favor llene el formulario !'
		else:
			cursor.execute('INSERT INTO usuarios (nombre, apellido, nickname, contrasenia, correo) VALUES (% s, % s, % s, % s, % s)', (nombre, apellido, nombreusuario, contrasenia, correo, ))
			mysql.connection.commit()
			msg = 'Registro exitoso !'
	elif request.method == 'POST':
		msg = 'Por favor llene el formulario !'
	return render_template('register2.html', msg = msg)

if __name__ == '__main__':
    app.run(debug=True)
