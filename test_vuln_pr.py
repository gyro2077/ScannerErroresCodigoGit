# Código vulnerable de prueba
import os

print("PELIGRO")

# SQL Injection
user_id = input("ID: ")
query = "SELECT * FROM users WHERE id = " + user_id

# Command Injection
filename = input("File: ")
os.system("cat " + filename)

# eval() peligroso
calc = input("Calc: ")
result = eval(calc)
