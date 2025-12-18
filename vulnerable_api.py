"""
API de usuarios con vulnerabilidad de SQL Injection
Este código DEBE ser detectado por el modelo de IA
"""
from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # VULNERABILIDAD: SQL Injection
    # El modelo debe detectar la concatenación directa en la query SQL
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)  # ← Vulnerable!
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"status": "success", "message": "Login exitoso"}
    else:
        return {"status": "error", "message": "Credenciales inválidas"}

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('q')
    
    # VULNERABILIDAD: SQL Injection en búsqueda
    query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%'"
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(query)  # ← Vulnerable!
    results = cursor.fetchall()
    conn.close()
    
    return {"results": results}

if __name__ == '__main__':
    app.run(debug=True)
