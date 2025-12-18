# 🚀 Guía de Configuración - GitHub & Vercel

Esta guía te llevará paso a paso para configurar el repositorio en GitHub y desplegarlo en Vercel.

## 📋 Prerequisitos

- Cuenta de GitHub
- Cuenta de Vercel (gratis en [vercel.com](https://vercel.com))
- Git instalado localmente

## 1️⃣ Crear Repositorio en GitHub

### Paso 1: Crear el repositorio
1. Ve a [github.com](https://github.com) e inicia sesión
2. Click en el botón **"New"** (nuevo repositorio)
3. Nombre del repositorio: `ScannerErroresCodigoGit` (o el que prefieras)
4. Selecciona **Público** o **Privado**
5. **NO** inicialices con README, .gitignore ni licencia (ya los tenemos)
6. Click en **"Create repository"**

### Paso 2: Copiar la URL del repositorio
Copia la URL que aparece, será algo como:
```
https://github.com/TU_USUARIO/ScannerErroresCodigoGit.git
```

## 2️⃣ Configurar Git Localmente

Abre una terminal en el directorio del proyecto y ejecuta:

```bash
# Inicializar repositorio
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Initial commit: Scanner de vulnerabilidades con CI/CD"

# Crear las tres ramas principales
git branch -M main
git checkout -b dev
git checkout -b test

# Volver a main
git checkout main

# Conectar con GitHub (reemplaza con TU URL)
git remote add origin https://github.com/TU_USUARIO/ScannerErroresCodigoGit.git

# Subir todas las ramas
git push -u origin main
git push -u origin dev
git push -u origin test
```

## 3️⃣ Crear GitHub Personal Access Token (PAT)

El token es necesario para que los workflows puedan hacer merge automático entre ramas.

### Paso 1: Generar el token
1. En GitHub, ve a **Settings** (tu perfil) → **Developer settings**
2. Click en **Personal access tokens** → **Tokens (classic)**
3. Click en **Generate new token** → **Generate new token (classic)**
4. Nombre: `Scanner CI/CD Token`
5. Selecciona estos permisos:
   - ✅ `repo` (todos los sub-permisos)
   - ✅ `workflow`
6. Click en **Generate token**
7. **¡IMPORTANTE!** Copia el token inmediatamente (solo se muestra una vez)

### Paso 2: Agregar el token como secreto
1. Ve a tu repositorio en GitHub
2. Click en **Settings** → **Secrets and variables** → **Actions**
3. Click en **New repository secret**
4. Name: `GH_PAT`
5. Secret: pega el token que copiaste
6. Click en **Add secret**

## 4️⃣ Configurar Vercel

### Paso 1: Crear cuenta y proyecto en Vercel
1. Ve a [vercel.com](https://vercel.com) y crea una cuenta (puedes usar GitHub)
2. Click en **Add New** → **Project**
3. Importa tu repositorio de GitHub
4. **Framework Preset**: Other
5. **Root Directory**: `./`
6. Click en **Deploy**

### Paso 2: Obtener credenciales de Vercel
1. Ve a [vercel.com/account/tokens](https://vercel.com/account/tokens)
2. Click en **Create Token**
3. Name: `GitHub Actions`
4. Scope: Full Account
5. Click en **Create**
6. **Copia el token** (VERCEL_TOKEN)

### Paso 3: Obtener IDs del proyecto
En tu terminal, instala Vercel CLI:
```bash
npm i -g vercel
```

Luego ejecuta:
```bash
cd /ruta/a/tu/proyecto
vercel login
vercel link
```

Esto creará un archivo `.vercel/project.json`. Ábrelo y copia:
- `orgId` → Este es tu **VERCEL_ORG_ID**
- `projectId` → Este es tu **VERCEL_PROJECT_ID**

### Paso 4: Agregar secretos de Vercel a GitHub
1. Ve a tu repositorio en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Agrega estos tres secretos:

| Name | Value |
|------|-------|
| `VERCEL_TOKEN` | El token que copiaste de Vercel |
| `VERCEL_ORG_ID` | El orgId del archivo .vercel/project.json |
| `VERCEL_PROJECT_ID` | El projectId del archivo .vercel/project.json |

## 5️⃣ Probar el Flujo Completo

### Prueba 1: Código Seguro (debe pasar)

```bash
# Ir a rama dev
git checkout dev

# Crear un archivo de prueba seguro
echo 'print("Hello World")' > test_safe.py

# Commit y push
git add test_safe.py
git commit -m "Test: código seguro"
git push origin dev
```

**Resultado esperado:**
1. ✅ Workflow en DEV ejecuta el scanner
2. ✅ No detecta vulnerabilidades
3. ✅ Hace merge automático a TEST
4. ✅ Tests se ejecutan en TEST
5. ✅ Hace merge automático a MAIN
6. ✅ Se despliega a Vercel

### Prueba 2: Código Vulnerable (debe fallar)

```bash
# Asegúrate de estar en dev
git checkout dev

# Crear un archivo con vulnerabilidad
cat > test_vuln.py << 'EOF'
import os
user_input = input("Enter command: ")
os.system(user_input)  # Command Injection!
EOF

# Commit y push
git add test_vuln.py
git commit -m "Test: código vulnerable"
git push origin dev
```

**Resultado esperado:**
1. ❌ Workflow en DEV ejecuta el scanner
2. ❌ Detecta vulnerabilidad
3. ❌ Workflow falla y NO hace merge a TEST

## 6️⃣ Ver los Resultados

### GitHub Actions
1. Ve a tu repositorio en GitHub
2. Click en la pestaña **Actions**
3. Verás todos los workflows ejecutándose

### Vercel Deployment
1. Ve a [vercel.com](https://vercel.com)
2. Click en tu proyecto
3. Verás el deployment y la URL pública

## 🎉 ¡Listo!

Tu pipeline CI/CD está completamente configurado:

```
DEV (push) → 🔍 Scan → ✅ → TEST → 🧪 Tests → ✅ → MAIN → 🚀 Deploy
```

## 🔧 Solución de Problemas

### Error: "Resource not accessible by integration"
- Verifica que el token `GH_PAT` tenga permisos de `repo` y `workflow`

### Error: "Vercel deployment failed"
- Verifica que los secretos `VERCEL_TOKEN`, `VERCEL_ORG_ID` y `VERCEL_PROJECT_ID` estén correctos

### El scanner no detecta vulnerabilidades
- Asegúrate de que los archivos `.pkl` estén en la carpeta `models/`
- Verifica que `requirements.txt` incluya `scikit-learn` y `joblib`

### Los tests fallan
- Ejecuta localmente: `pytest tests/ -v`
- Verifica que todos los archivos necesarios existan

## 📞 Soporte

Si tienes problemas, revisa los logs en:
- GitHub Actions: pestaña "Actions" en tu repositorio
- Vercel: Dashboard del proyecto en vercel.com
