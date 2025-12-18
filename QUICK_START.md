# 🚀 Guía Rápida: Subir a GitHub

## Paso 1: Crear Repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre: `ScannerErroresCodigoGit` (o el que prefieras)
3. **NO marques** ninguna opción (README, .gitignore, licencia)
4. Click en "Create repository"
5. Copia la URL que aparece (ejemplo: `https://github.com/usuario/ScannerErroresCodigoGit.git`)

## Paso 2: Subir el Código

Ejecuta estos comandos en la terminal (reemplaza `TU_USUARIO` y `TU_REPO` con tus valores):

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git

# Subir todas las ramas
git push -u origin main
git push -u origin dev
git push -u origin test
```

## Paso 3: Crear GitHub Personal Access Token (PAT)

1. Ve a https://github.com/settings/tokens
2. Click en "Generate new token" → "Generate new token (classic)"
3. Nombre: `Scanner CI/CD`
4. Selecciona estos permisos:
   - ✅ `repo` (todos los sub-permisos)
   - ✅ `workflow`
5. Click en "Generate token"
6. **¡COPIA EL TOKEN!** (solo se muestra una vez)
## Paso 4: Agregar Secretos en GitHub

1. Ve a tu repositorio: `https://github.com/TU_USUARIO/ScannerErroresCodigoGit`
2. Click en **Settings** → **Secrets and variables** → **Actions**
3. Click en **New repository secret**

Agrega este secreto:

| Name | Value |
|------|-------|
| `GH_PAT` | El token que acabas de copiar |

## Paso 5: Probar el Flujo

```bash
# Ir a rama dev
git checkout dev

# Crear archivo de prueba seguro
echo 'print("Hello World")' > test_hello.py
git add test_hello.py
git commit -m "Test: código seguro"
git push origin dev
```

## Paso 6: Ver el Workflow en Acción

1. Ve a tu repositorio en GitHub
2. Click en la pestaña **Actions**
3. Verás el workflow ejecutándose
4. Debería:
   - ✅ Escanear vulnerabilidades
   - ✅ Aprobar el código
   - ✅ Hacer merge automático a `test`
   - ✅ Ejecutar tests
   - ✅ Hacer merge automático a `main`

---

## 🎯 Probar con Código Vulnerable

```bash
git checkout dev

# Crear código vulnerable
cat > test_vuln.py << 'EOF'
import os
user_input = input("Enter: ")
os.system(user_input)  # Command Injection!
EOF

git add test_vuln.py
git commit -m "Test: código vulnerable"
git push origin dev
```

**Resultado esperado**: El workflow debe **FALLAR** y bloquear el merge ❌

---

## 📝 Notas

- Por ahora **NO** configuraremos Vercel (solo GitHub workflows)
- El workflow de deployment a Vercel fallará (es normal, lo configuraremos después)
- Lo importante es que funcionen los workflows de DEV y TEST
