"""
Archivo de prueba con código seguro
Este archivo debe pasar el scanner de vulnerabilidades
"""

def calcular_suma(a, b):
    """Función simple y segura para sumar dos números"""
    return a + b

def saludar(nombre):
    """Función segura para saludar"""
    return f"¡Hola, {nombre}!"

if __name__ == "__main__":
    # Código de prueba seguro
    resultado = calcular_suma(5, 3)
    print(f"La suma es: {resultado}")
    
    mensaje = saludar("Mundo")
    print(mensaje)
    
    # Lista de números
    numeros = [1, 2, 3, 4, 5]
    suma_total = sum(numeros)
    print(f"Suma total: {suma_total}")
