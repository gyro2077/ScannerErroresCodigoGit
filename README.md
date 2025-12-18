# 🔐 ScannerErroresCodigoGit

Scanner automático de vulnerabilidades en código con CI/CD integrado y despliegue a Vercel.

## 👥 Integrantes
- Chiliquinga Yeshua
- Ferrin Josue
- Sanmartin Jose

## 📋 Descripción

Sistema de detección automática de vulnerabilidades que implementa un pipeline CI/CD de 3 etapas con despliegue continuo:

```
DEV → TEST → MAIN → 🌐 Vercel
 ↓      ↓      ↓
🔍    🧪    🚀
```

### Flujo de Trabajo Automatizado

1. **DEV (Detección)**: Analiza código con IA para detectar vulnerabilidades
   - ✅ Seguro → Merge automático a TEST
   - ❌ Vulnerable → Bloquea y falla el workflow

2. **TEST (Validación)**: Ejecuta pruebas automáticas
   - ✅ Pasa → Merge automático a MAIN
   - ❌ Falla → Bloquea merge

3. **MAIN (Despliegue)**: Despliega automáticamente a Vercel
   - 🚀 Despliegue automático a producción
   - 🌐 Sitio web público disponible

## 🚀 Inicio Rápido

### Instalación Local

```bash
# Clonar repositorio
git clone <repo-url>
cd ScannerErroresCodigoGit

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest tests/ -v
```

### Configuración GitHub + Vercel

Ver **[SETUP_GUIDE.md](SETUP_GUIDE.md)** para instrucciones completas de configuración.

**Resumen rápido:**
1. Crear repositorio en GitHub
2. Configurar secreto `GH_PAT` (GitHub Personal Access Token)
3. Crear proyecto en Vercel
4. Configurar secretos: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`
5. Push a rama `dev` para activar el pipeline

## 🧪 Pruebas Locales

```bash
# Probar scanner de vulnerabilidades
python scripts/ai_scan.py

# Ejecutar suite de tests
pytest tests/test_basic.py -v

# Ver ejemplo de uso del modelo
python scripts/ia_scan.py
```

## 📚 Documentación

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)**: Guía completa de configuración
- **[implementation_plan.md](implementation_plan.md)**: Plan de implementación técnico

## 🛠️ Tecnologías

- **Backend**: Python 3.9+
- **ML**: scikit-learn (Modelo de detección de vulnerabilidades)
- **Testing**: pytest
- **CI/CD**: GitHub Actions
- **Deployment**: Vercel
- **Frontend**: HTML/CSS (página de estado)

## 📁 Estructura del Proyecto

```
├── .github/workflows/     # Workflows CI/CD
│   ├── dev_scan.yml      # Escaneo en DEV
│   ├── test_validation.yml  # Tests en TEST
│   └── main_deploy.yml   # Deploy en MAIN
├── models/               # Modelos ML entrenados (.pkl)
├── scripts/              # Scripts de automatización
│   ├── ai_scan.py       # Scanner principal
│   └── ia_scan.py       # Ejemplo de uso
├── tests/                # Suite de tests
├── public/               # Archivos estáticos para Vercel
│   └── index.html       # Landing page
├── src/                  # Código fuente (ejemplos)
├── vercel.json          # Configuración Vercel
└── requirements.txt     # Dependencias Python
```

## 🔒 Seguridad

El sistema detecta automáticamente:
- ✅ SQL Injection
- ✅ Command Injection
- ✅ Code Injection (eval, exec)
- ✅ Path Traversal
- ✅ Deserialización insegura
- ✅ Credenciales hardcodeadas
- ✅ Y más patrones de vulnerabilidades...

## 🔄 Workflows de GitHub Actions

### 1. DEV - Vulnerability Scan
**Trigger**: Push a rama `dev`
- Instala dependencias
- Ejecuta scanner de IA
- Si pasa: merge automático a `test`
- Si falla: bloquea y notifica

### 2. TEST - Validation
**Trigger**: Push a rama `test`
- Ejecuta suite de tests con pytest
- Si pasa: merge automático a `main`
- Si falla: bloquea merge

### 3. MAIN - Deploy
**Trigger**: Push a rama `main`
- Despliega automáticamente a Vercel
- Sitio web público disponible

## 📊 Estado del Proyecto

![CI/CD](https://img.shields.io/badge/CI%2FCD-Automated-success)
![Security](https://img.shields.io/badge/Security-AI%20Powered-blue)
![Tests](https://img.shields.io/badge/Tests-Automated-green)
![Deploy](https://img.shields.io/badge/Deploy-Vercel-black)

## 🎯 Uso del Pipeline

### Flujo Normal (Código Seguro)
```bash
# 1. Desarrollar en rama dev
git checkout dev
echo 'print("Hello")' > safe_code.py
git add safe_code.py
git commit -m "Add safe code"
git push origin dev

# 2. El pipeline automáticamente:
#    - Escanea vulnerabilidades ✅
#    - Merge a test ✅
#    - Ejecuta tests ✅
#    - Merge a main ✅
#    - Despliega a Vercel ✅
```

### Flujo con Vulnerabilidad
```bash
# 1. Código vulnerable
git checkout dev
echo 'import os; os.system(input())' > vuln.py
git add vuln.py
git commit -m "Vulnerable code"
git push origin dev

# 2. El pipeline:
#    - Escanea vulnerabilidades ❌
#    - BLOQUEA el merge
#    - Workflow falla
```

## 🌐 Despliegue

El sitio está desplegado automáticamente en Vercel. Cada push a `main` actualiza el deployment.

**URL**: Se genera automáticamente al configurar Vercel

---

**Universidad**: [Tu Universidad]  
**Materia**: Seguridad de Software  
**Fecha**: Diciembre 2024

# Test deployment
