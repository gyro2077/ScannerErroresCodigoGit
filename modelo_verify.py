#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Verificación de Modelos PKL
======================================
Verifica que todos los archivos .pkl estén correctos y funcionales.

Uso:
    python verificar_modelos.py
"""

import pickle
import os
import sys
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Imprime un encabezado formateado"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")

def print_success(text):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    """Imprime mensaje informativo"""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def verificar_archivo_existe(ruta):
    """Verifica que un archivo existe"""
    if not os.path.exists(ruta):
        print_error(f"Archivo no encontrado: {ruta}")
        return False
    
    tamaño_mb = os.path.getsize(ruta) / (1024 * 1024)
    print_success(f"Archivo encontrado: {os.path.basename(ruta)}")
    print_info(f"   Tamaño: {tamaño_mb:.2f} MB")
    return True

def cargar_modelo(ruta):
    """Intenta cargar un modelo pickle"""
    try:
        with open(ruta, 'rb') as f:
            modelo = pickle.load(f)
        print_success(f"Modelo cargado correctamente")
        return modelo
    except Exception as e:
        print_error(f"Error al cargar modelo: {e}")
        return None

def verificar_modelo_detector(modelo):
    """Verifica atributos del modelo detector/clasificador"""
    try:
        print_info(f"   Tipo: {type(modelo).__name__}")
        
        if hasattr(modelo, 'n_estimators'):
            print_info(f"   Número de árboles: {modelo.n_estimators}")
        
        if hasattr(modelo, 'n_features_in_'):
            print_info(f"   Features de entrada: {modelo.n_features_in_}")
        
        if hasattr(modelo, 'classes_'):
            print_info(f"   Clases: {len(modelo.classes_)} → {modelo.classes_}")
        
        return True
    except Exception as e:
        print_error(f"Error al verificar modelo: {e}")
        return False

def verificar_vectorizer(vectorizer):
    """Verifica atributos del vectorizador TF-IDF"""
    try:
        print_info(f"   Tipo: {type(vectorizer).__name__}")
        
        if hasattr(vectorizer, 'vocabulary_'):
            print_info(f"   Vocabulario: {len(vectorizer.vocabulary_)} palabras")
        
        if hasattr(vectorizer, 'max_features'):
            print_info(f"   Max features: {vectorizer.max_features}")
        
        if hasattr(vectorizer, 'ngram_range'):
            print_info(f"   N-gramas: {vectorizer.ngram_range}")
        
        return True
    except Exception as e:
        print_error(f"Error al verificar vectorizador: {e}")
        return False

def verificar_encoder(encoder):
    """Verifica atributos del encoder"""
    try:
        print_info(f"   Tipo: {type(encoder).__name__}")
        
        if hasattr(encoder, 'classes_'):
            print_info(f"   Clases codificadas: {len(encoder.classes_)}")
            print_info(f"   Valores: {list(encoder.classes_)[:5]}...")  # Primeros 5
        
        return True
    except Exception as e:
        print_error(f"Error al verificar encoder: {e}")
        return False

def probar_prediccion_detector(detector, vectorizer):
    """Prueba una predicción con el detector"""
    try:
        # Código de prueba vulnerable
        codigo_vulnerable = "char buffer[10]; strcpy(buffer, user_input);"
        
        # Vectorizar
        features = vectorizer.transform([codigo_vulnerable])
        
        # Predecir
        prediccion = detector.predict(features)[0]
        probabilidades = detector.predict_proba(features)[0]
        
        print_success("Predicción de prueba exitosa")
        print_info(f"   Código: {codigo_vulnerable}")
        print_info(f"   Predicción: {'Vulnerable' if prediccion == 1 else 'Seguro'}")
        print_info(f"   Confianza: {probabilidades[prediccion]:.2%}")
        print_info(f"   Prob. Seguro: {probabilidades[0]:.2%} | Prob. Vulnerable: {probabilidades[1]:.2%}")
        
        return True
    except Exception as e:
        print_error(f"Error en predicción de prueba: {e}")
        return False

def probar_prediccion_clasificador(classifier, vectorizer, encoder):
    """Prueba una predicción con el clasificador CWE"""
    try:
        # Código de prueba SQL Injection
        codigo_sql = "SELECT * FROM users WHERE id = " + "user_input"
        
        # Vectorizar
        features = vectorizer.transform([codigo_sql])
        
        # Predecir
        prediccion_idx = classifier.predict(features)[0]
        tipo_cwe = encoder.inverse_transform([prediccion_idx])[0]
        probabilidades = classifier.predict_proba(features)[0]
        
        # Top 3
        top_3_indices = probabilidades.argsort()[-3:][::-1]
        top_3_tipos = encoder.inverse_transform(top_3_indices)
        
        print_success("Predicción de prueba exitosa")
        print_info(f"   Código: {codigo_sql}")
        print_info(f"   Tipo CWE: {tipo_cwe}")
        print_info(f"   Confianza: {probabilidades[prediccion_idx]:.2%}")
        print_info(f"   Top 3:")
        for i, (tipo, idx) in enumerate(zip(top_3_tipos, top_3_indices), 1):
            print_info(f"      {i}. {tipo}: {probabilidades[idx]:.2%}")
        
        return True
    except Exception as e:
        print_error(f"Error en predicción de prueba: {e}")
        return False

def main():
    """Función principal"""
    print_header("VERIFICACIÓN DE MODELOS PKL")
    
    # Definir rutas
    base_dir = Path(__file__).parent
    models_dir = base_dir / "models"
    
    archivos = {
        'detector': models_dir / 'vulnerability_detector.pkl',
        'vectorizer_detector': models_dir / 'vectorizer_detector.pkl',
        'language_encoder': models_dir / 'language_encoder.pkl',
        'cwe_classifier': models_dir / 'cwe_classifier.pkl',
        'vectorizer_cwe': models_dir / 'vectorizer_cwe_classifier.pkl',
        'cwe_encoder': models_dir / 'cwe_encoder.pkl',
    }
    
    resultados = {
        'total': len(archivos),
        'exitosos': 0,
        'fallidos': 0
    }
    
    modelos_cargados = {}
    
    # ========== VERIFICACIÓN 1: MODELO DETECTOR ==========
    print_header("1. MODELO DETECTOR (Detección Binaria)")
    
    print(f"{Colors.BOLD}Verificando vulnerability_detector.pkl...{Colors.END}")
    if verificar_archivo_existe(archivos['detector']):
        modelo = cargar_modelo(archivos['detector'])
        if modelo and verificar_modelo_detector(modelo):
            modelos_cargados['detector'] = modelo
            resultados['exitosos'] += 1
        else:
            resultados['fallidos'] += 1
    else:
        resultados['fallidos'] += 1
    
    print(f"\n{Colors.BOLD}Verificando vectorizer_detector.pkl...{Colors.END}")
    if verificar_archivo_existe(archivos['vectorizer_detector']):
        vectorizer = cargar_modelo(archivos['vectorizer_detector'])
        if vectorizer and verificar_vectorizer(vectorizer):
            modelos_cargados['vectorizer_detector'] = vectorizer
            resultados['exitosos'] += 1
        else:
            resultados['fallidos'] += 1
    else:
        resultados['fallidos'] += 1
    
    print(f"\n{Colors.BOLD}Verificando language_encoder.pkl...{Colors.END}")
    if verificar_archivo_existe(archivos['language_encoder']):
        encoder = cargar_modelo(archivos['language_encoder'])
        if encoder and verificar_encoder(encoder):
            modelos_cargados['language_encoder'] = encoder
            resultados['exitosos'] += 1
        else:
            resultados['fallidos'] += 1
    else:
        resultados['fallidos'] += 1
    
    # ========== VERIFICACIÓN 2: MODELO CLASIFICADOR ==========
    print_header("2. MODELO CLASIFICADOR (Clasificación CWE)")
    
    print(f"{Colors.BOLD}Verificando cwe_classifier.pkl...{Colors.END}")
    if verificar_archivo_existe(archivos['cwe_classifier']):
        modelo = cargar_modelo(archivos['cwe_classifier'])
        if modelo and verificar_modelo_detector(modelo):
            modelos_cargados['cwe_classifier'] = modelo
            resultados['exitosos'] += 1
        else:
            resultados['fallidos'] += 1
    else:
        resultados['fallidos'] += 1
    
    print(f"\n{Colors.BOLD}Verificando vectorizer_cwe_classifier.pkl...{Colors.END}")
    if verificar_archivo_existe(archivos['vectorizer_cwe']):
        vectorizer = cargar_modelo(archivos['vectorizer_cwe'])
        if vectorizer and verificar_vectorizer(vectorizer):
            modelos_cargados['vectorizer_cwe'] = vectorizer
            resultados['exitosos'] += 1
        else:
            resultados['fallidos'] += 1
    else:
        resultados['fallidos'] += 1
    
    print(f"\n{Colors.BOLD}Verificando cwe_encoder.pkl...{Colors.END}")
    if verificar_archivo_existe(archivos['cwe_encoder']):
        encoder = cargar_modelo(archivos['cwe_encoder'])
        if encoder and verificar_encoder(encoder):
            modelos_cargados['cwe_encoder'] = encoder
            resultados['exitosos'] += 1
        else:
            resultados['fallidos'] += 1
    else:
        resultados['fallidos'] += 1
    
    # ========== VERIFICACIÓN 3: PRUEBAS FUNCIONALES ==========
    print_header("3. PRUEBAS FUNCIONALES")
    
    if 'detector' in modelos_cargados and 'vectorizer_detector' in modelos_cargados:
        print(f"{Colors.BOLD}Probando Detector Binario...{Colors.END}")
        probar_prediccion_detector(
            modelos_cargados['detector'],
            modelos_cargados['vectorizer_detector']
        )
    else:
        print_warning("No se puede probar el detector (modelos no cargados)")
    
    print()
    
    if all(k in modelos_cargados for k in ['cwe_classifier', 'vectorizer_cwe', 'cwe_encoder']):
        print(f"{Colors.BOLD}Probando Clasificador CWE...{Colors.END}")
        probar_prediccion_clasificador(
            modelos_cargados['cwe_classifier'],
            modelos_cargados['vectorizer_cwe'],
            modelos_cargados['cwe_encoder']
        )
    else:
        print_warning("No se puede probar el clasificador (modelos no cargados)")
    
    # ========== RESUMEN FINAL ==========
    print_header("RESUMEN FINAL")
    
    porcentaje = (resultados['exitosos'] / resultados['total']) * 100
    
    print(f"Total de archivos verificados: {resultados['total']}")
    print_success(f"Exitosos: {resultados['exitosos']}")
    
    if resultados['fallidos'] > 0:
        print_error(f"Fallidos: {resultados['fallidos']}")
    
    print(f"\n{Colors.BOLD}Porcentaje de éxito: {porcentaje:.1f}%{Colors.END}\n")
    
    if porcentaje == 100:
        print_success("¡Todos los modelos están correctos y funcionales! 🎉")
        return 0
    elif porcentaje >= 80:
        print_warning("La mayoría de los modelos funcionan, pero hay algunos problemas.")
        return 1
    else:
        print_error("Hay problemas significativos con los modelos.")
        print_info("Considera volver a entrenar los modelos:")
        print_info("  cd modelo_1_detector && python vulnerability_detector.py")
        print_info("  cd modelo_2_clasificador && python cwe_classifier.py")
        return 2

if __name__ == "__main__":
    sys.exit(main())
