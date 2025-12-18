import os
import sys
import joblib

# --- CONFIGURACIÓN CON TUS NOMBRES EXACTOS ---
# Usamos los archivos que terminan en 'detector'
MODELO_PATH = 'models/vulnerability_detector.pkl'
VECTORIZADOR_PATH = 'models/vectorizer_detector.pkl'

def cargar_modelo():
    try:
        print(f"⏳ Cargando modelo desde {MODELO_PATH}...")
        modelo = joblib.load(MODELO_PATH)
        vectorizador = joblib.load(VECTORIZADOR_PATH)
        print("✅ Modelo y vectorizador cargados.")
        return modelo, vectorizador
    except Exception as e:
        print(f"❌ Error cargando archivos .pkl: {e}")
        print("Asegúrate de haber subido 'vulnerability_detector.pkl' y 'vectorizer_detector.pkl' a la carpeta models/")
        sys.exit(1)

def analizar_codigo():
    modelo, vectorizador = cargar_modelo()
    es_vulnerable = False
    archivos_afectados = []
    
    print("🔍 Iniciando escaneo con IA...")

    for root, dirs, files in os.walk("."):
        # Skip common directories that shouldn't be scanned
        skip_dirs = [".git", "models", "scripts", ".venv", "venv", "node_modules", 
                     "__pycache__", ".pytest_cache", "env", ".env"]
        if any(skip_dir in root for skip_dir in skip_dirs):
            continue

        for file in files:
            if file.endswith((".py", ".js", ".java", ".php", ".cpp")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", errors="ignore") as f:
                        contenido = f.read()
                    
                    # 1. Vectorizar
                    features = vectorizador.transform([contenido])
                    
                    # 2. Predecir
                    # IMPORTANTE: Asumimos que 1 = Vulnerable. 
                    # Si el modelo funciona al revés, cambia esto a 'prediction == 0'
                    prediction = modelo.predict(features)[0]
                    
                    if prediction == 1: 
                        print(f"⚠️ AMENAZA DETECTADA en: {file}")
                        es_vulnerable = True
                        archivos_afectados.append(file)
                        
                except Exception as e:
                    print(f"Error leyendo {file}: {e}")

    if es_vulnerable:
        print(f"\n⛔ RECHAZADO: Se detectaron vulnerabilidades en: {archivos_afectados}")
        sys.exit(1) # Falla el pipeline
    else:
        print("\n✅ APROBADO: El código parece seguro.")
        sys.exit(0) # Pasa el pipeline

if __name__ == "__main__":
    analizar_codigo()