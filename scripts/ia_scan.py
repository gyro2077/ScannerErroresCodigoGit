#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo Simple de Uso de los Modelos PKL
=========================================
Demuestra cómo usar los modelos para detectar y clasificar vulnerabilidades.

Uso:
    python ejemplo_uso_simple.py
"""

import pickle
from pathlib import Path

def cargar_modelos():
    """Carga todos los modelos necesarios"""
    print("🔄 Cargando modelos...")
    
    models_dir = Path(__file__).parent / "models"
    
    modelos = {
        # Modelo 1: Detector
        'detector': pickle.load(open(models_dir / 'vulnerability_detector.pkl', 'rb')),
        'vectorizer': pickle.load(open(models_dir / 'vectorizer_detector.pkl', 'rb')),
        'lang_encoder': pickle.load(open(models_dir / 'language_encoder.pkl', 'rb')),
        
        # Modelo 2: Clasificador
        'cwe_classifier': pickle.load(open(models_dir / 'cwe_classifier.pkl', 'rb')),
        'vectorizer_cwe': pickle.load(open(models_dir / 'vectorizer_cwe_classifier.pkl', 'rb')),
        'cwe_encoder': pickle.load(open(models_dir / 'cwe_encoder.pkl', 'rb')),
    }
    
    print("✅ Modelos cargados correctamente\n")
    return modelos

def analizar_codigo(codigo, lenguaje, modelos):
    """
    Analiza un código y determina si es vulnerable y de qué tipo.
    
    Args:
        codigo (str): Código fuente a analizar
        lenguaje (str): Lenguaje de programación
        modelos (dict): Diccionario con todos los modelos cargados
    
    Returns:
        dict: Resultados del análisis
    """
    print(f"{'='*70}")
    print(f"📝 Analizando código en {lenguaje}:")
    print(f"{'='*70}")
    print(f"{codigo[:200]}{'...' if len(codigo) > 200 else ''}")
    print(f"{'='*70}\n")
    
    # PASO 1: Detectar si es vulnerable
    features = modelos['vectorizer'].transform([codigo])
    es_vulnerable = modelos['detector'].predict(features)[0]
    probabilidades = modelos['detector'].predict_proba(features)[0]
    
    resultado = {
        'codigo': codigo,
        'lenguaje': lenguaje,
        'vulnerable': bool(es_vulnerable),
        'confianza_deteccion': float(probabilidades[es_vulnerable]),
        'probabilidad_seguro': float(probabilidades[0]),
        'probabilidad_vulnerable': float(probabilidades[1]),
    }
    
    print(f"🔍 DETECCIÓN:")
    print(f"   Estado: {'🔴 VULNERABLE' if es_vulnerable else '🟢 SEGURO'}")
    print(f"   Confianza: {probabilidades[es_vulnerable]:.2%}")
    print(f"   Prob. Seguro: {probabilidades[0]:.2%}")
    print(f"   Prob. Vulnerable: {probabilidades[1]:.2%}")
    
    # PASO 2: Si es vulnerable, clasificar el tipo
    if es_vulnerable:
        features_cwe = modelos['vectorizer_cwe'].transform([codigo])
        tipo_idx = modelos['cwe_classifier'].predict(features_cwe)[0]
        tipo_cwe = modelos['cwe_encoder'].inverse_transform([tipo_idx])[0]
        probabilidades_cwe = modelos['cwe_classifier'].predict_proba(features_cwe)[0]
        
        # Top 3 tipos más probables
        top_3_indices = probabilidades_cwe.argsort()[-3:][::-1]
        top_3_tipos = modelos['cwe_encoder'].inverse_transform(top_3_indices)
        
        resultado['tipo_vulnerabilidad'] = tipo_cwe
        resultado['confianza_clasificacion'] = float(probabilidades_cwe[tipo_idx])
        resultado['top_3_tipos'] = [
            {
                'tipo': tipo,
                'probabilidad': float(probabilidades_cwe[idx])
            }
            for tipo, idx in zip(top_3_tipos, top_3_indices)
        ]
        
        print(f"\n🎯 CLASIFICACIÓN:")
        print(f"   Tipo: {tipo_cwe}")
        print(f"   Confianza: {probabilidades_cwe[tipo_idx]:.2%}")
        print(f"\n   Top 3 tipos más probables:")
        for i, item in enumerate(resultado['top_3_tipos'], 1):
            print(f"      {i}. {item['tipo']}: {item['probabilidad']:.2%}")
    
    print(f"\n{'='*70}\n")
    return resultado

def main():
    """Función principal con ejemplos de uso"""
    print("\n" + "="*70)
    print("  EJEMPLO DE USO DE MODELOS PKL - DETECCIÓN DE VULNERABILIDADES")
    print("="*70 + "\n")
    
    # Cargar modelos
    modelos = cargar_modelos()
    
    # Ejemplos de código a analizar
    ejemplos = [
        {
            'codigo': """
char buffer[10];
strcpy(buffer, user_input);
            """.strip(),
            'lenguaje': 'C++',
            'descripcion': 'Buffer Overflow clásico'
        },
        {
            'codigo': """
query = "SELECT * FROM users WHERE id = " + user_id
cursor.execute(query)
            """.strip(),
            'lenguaje': 'Python',
            'descripcion': 'SQL Injection'
        },
        {
            'codigo': """
eval(user_input)
            """.strip(),
            'lenguaje': 'Python',
            'descripcion': 'Code Injection'
        },
        {
            'codigo': """
def saludar(nombre):
    return f"Hola, {nombre}!"

print(saludar("Mundo"))
            """.strip(),
            'lenguaje': 'Python',
            'descripcion': 'Código seguro'
        },
        {
            'codigo': """
String query = "SELECT * FROM users WHERE username = '" + username + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);
            """.strip(),
            'lenguaje': 'Java',
            'descripcion': 'SQL Injection en Java'
        },
    ]
    
    # Analizar cada ejemplo
    resultados = []
    for i, ejemplo in enumerate(ejemplos, 1):
        print(f"\n📌 EJEMPLO {i}: {ejemplo['descripcion']}")
        resultado = analizar_codigo(
            ejemplo['codigo'],
            ejemplo['lenguaje'],
            modelos
        )
        resultados.append(resultado)
    
    # Resumen final
    print("\n" + "="*70)
    print("  RESUMEN DE ANÁLISIS")
    print("="*70 + "\n")
    
    vulnerables = sum(1 for r in resultados if r['vulnerable'])
    seguros = len(resultados) - vulnerables
    
    print(f"Total de códigos analizados: {len(resultados)}")
    print(f"🔴 Vulnerables: {vulnerables}")
    print(f"🟢 Seguros: {seguros}")
    
    if vulnerables > 0:
        print(f"\nTipos de vulnerabilidades encontradas:")
        tipos = {}
        for r in resultados:
            if r['vulnerable'] and 'tipo_vulnerabilidad' in r:
                tipo = r['tipo_vulnerabilidad']
                tipos[tipo] = tipos.get(tipo, 0) + 1
        
        for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {tipo}: {count}")
    
    print("\n" + "="*70)
    print("✅ Análisis completado")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
