import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Bienvenido a la App Vulnerable (No usar en producción)"

# CASO 1: SQL INJECTION (El clásico)
# El modelo debería detectar palabras clave como 'execute', 'SELECT' concatenado con inputs.
@app.route('/buscar_usuario')
def buscar_usuario():
    username = request.args.get('username')
    
    # ❌ PELIGRO: Concatenación directa de strings en una consulta SQL
    # Un atacante podría poner: admin' --
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        c.execute(query) # <--- Aquí está la vulnerabilidad que busca la IA
        result = c.fetchall()
        return str(result)
    except Exception as e:
        return str(e)
    finally:
        conn.close()

# CASO 2: OS COMMAND INJECTION (El más peligroso)
# El modelo debería alarmarse al ver 'os.system' o 'eval' con datos de entrada.
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    
    # ❌ PELIGRO: El usuario puede ejecutar comandos del sistema
    # Un atacante podría poner: 127.0.0.1; rm -rf /
    os.system("ping -c 1 " + ip) 
    
    return "Ping ejecutado (revisar consola del servidor)"

if __name__ == '__main__':
    # debug=True en producción también es una mala práctica
    app.run(host='0.0.0.0', port=5000, debug=True)