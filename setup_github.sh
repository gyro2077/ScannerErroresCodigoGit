#!/bin/bash

# Script de ayuda para subir el proyecto a GitHub
# Este script te guiará paso a paso

echo "🚀 Script de Configuración GitHub + Vercel"
echo "=========================================="
echo ""

# Verificar que estamos en un repositorio git
if [ ! -d ".git" ]; then
    echo "❌ Error: No estás en un repositorio git"
    echo "   Ejecuta primero: git init"
    exit 1
fi

echo "📝 Paso 1: Configurar repositorio remoto"
echo "----------------------------------------"
echo "Por favor, ingresa la URL de tu repositorio de GitHub:"
echo "Ejemplo: https://github.com/TU_USUARIO/ScannerErroresCodigoGit.git"
read -p "URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Error: URL vacía"
    exit 1
fi

# Verificar si ya existe un remote
if git remote | grep -q "origin"; then
    echo "⚠️  Ya existe un remote 'origin'. ¿Quieres reemplazarlo? (s/n)"
    read -p "Respuesta: " REPLACE
    if [ "$REPLACE" = "s" ] || [ "$REPLACE" = "S" ]; then
        git remote remove origin
        git remote add origin "$REPO_URL"
        echo "✅ Remote actualizado"
    fi
else
    git remote add origin "$REPO_URL"
    echo "✅ Remote agregado"
fi

echo ""
echo "📤 Paso 2: Subir código a GitHub"
echo "--------------------------------"
echo "Subiendo las 3 ramas (main, dev, test)..."

# Asegurarse de estar en main
git checkout main

# Push de todas las ramas
git push -u origin main
git push -u origin dev
git push -u origin test

echo ""
echo "✅ Código subido exitosamente a GitHub!"
echo ""
echo "📋 Paso 3: Configurar GitHub Secrets"
echo "------------------------------------"
echo "Ahora necesitas configurar los secretos en GitHub:"
echo ""
echo "1. Ve a: https://github.com/TU_USUARIO/TU_REPO/settings/secrets/actions"
echo ""
echo "2. Agrega estos secretos:"
echo "   - GH_PAT: Tu GitHub Personal Access Token"
echo "     (Créalo en: https://github.com/settings/tokens)"
echo "     Permisos necesarios: repo, workflow"
echo ""
echo "   - VERCEL_TOKEN: Tu token de Vercel"
echo "     (Obténlo en: https://vercel.com/account/tokens)"
echo ""
echo "   - VERCEL_ORG_ID: ID de tu organización en Vercel"
echo "   - VERCEL_PROJECT_ID: ID de tu proyecto en Vercel"
echo "     (Estos dos los obtienes ejecutando: vercel link)"
echo ""
echo "📖 Para más detalles, consulta: SETUP_GUIDE.md"
echo ""
echo "🎉 ¡Listo! Una vez configurados los secretos, el pipeline estará activo."
