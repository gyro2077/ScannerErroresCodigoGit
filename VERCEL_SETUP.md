# 🌐 Configuración de Vercel - Guía Paso a Paso

## ✅ Estado Actual
- ✅ Código subido a GitHub
- ✅ Workflows de DEV y TEST funcionando
- ❌ Deployment a Vercel pendiente (falta configurar secretos)

## 📋 Pasos para Configurar Vercel

### 1. Crear Cuenta en Vercel

1. Ve a https://vercel.com
2. Click en **Sign Up**
3. Selecciona **Continue with GitHub** (recomendado)
4. Autoriza a Vercel para acceder a tu cuenta de GitHub

### 2. Importar el Proyecto

1. En el dashboard de Vercel, click en **Add New** → **Project**
2. Busca tu repositorio `ScannerErroresCodigoGit`
3. Click en **Import**
4. Configuración:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: (dejar vacío)
   - **Output Directory**: `public`
5. Click en **Deploy**

### 3. Obtener el Token de Vercel

1. Ve a https://vercel.com/account/tokens
2. Click en **Create Token**
3. Configuración:
   - **Token Name**: `GitHub Actions`
   - **Scope**: Full Account
   - **Expiration**: No Expiration (o el tiempo que prefieras)
4. Click en **Create**
5. **¡COPIA EL TOKEN!** (solo se muestra una vez)

### 4. Obtener IDs del Proyecto

**Opción A: Desde la Terminal (Recomendado)**

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Vincular proyecto
cd /home/gyro/Documents/OCT25-MAR26/SOFT_SEGURO/PARCIAL_DOS/ScannerErroresCodigoGit
vercel link

# Ver los IDs
cat .vercel/project.json
```

Esto te mostrará algo como:
```json
{
  "orgId": "team_xxxxxxxxxxxxx",
  "projectId": "prj_xxxxxxxxxxxxx"
}
```

**Opción B: Desde el Dashboard de Vercel**

1. Ve a tu proyecto en Vercel
2. Click en **Settings**
3. En la sección **General**:
   - **Project ID**: copia este valor
4. Para el **Org ID**:
   - Ve a https://vercel.com/account
   - En la URL verás algo como: `vercel.com/teams/TEAM_ID` o `vercel.com/ORG_ID`

### 5. Agregar Secretos en GitHub

1. Ve a tu repositorio en GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Click en **New repository secret**

Agrega estos **3 secretos**:

| Secret Name | Value | Descripción |
|-------------|-------|-------------|
| `VERCEL_TOKEN` | El token que copiaste | Token de autenticación |
| `VERCEL_ORG_ID` | `team_xxxxx` o `user_xxxxx` | ID de organización |
| `VERCEL_PROJECT_ID` | `prj_xxxxx` | ID del proyecto |

### 6. Probar el Deployment

Una vez configurados los secretos:

```bash
# Hacer un cambio en main para disparar el deployment
git checkout main
echo "# Test deployment" >> README.md
git add README.md
git commit -m "Test: trigger Vercel deployment"
git push origin main
```

### 7. Verificar el Deployment

1. Ve a **Actions** en GitHub
2. Verás el workflow "MAIN - Deploy to Vercel" ejecutándose
3. Debería completarse exitosamente ✅
4. Ve a tu proyecto en Vercel para ver la URL pública

---

## 🚀 Opción Alternativa: Desactivar Deployment (Más Simple)

Si **NO quieres** configurar Vercel ahora, puedes desactivar temporalmente el workflow de deployment:

```bash
# Renombrar el workflow para desactivarlo
cd .github/workflows
mv main_deploy.yml main_deploy.yml.disabled

git add .
git commit -m "Disable Vercel deployment temporarily"
git push origin main
```

Esto hará que solo funcionen los workflows de DEV y TEST, que ya están operativos.

---

## 📊 Resumen de Secretos Necesarios

Para que TODO funcione, necesitas estos secretos en GitHub:

| Secret | Propósito | Estado |
|--------|-----------|--------|
| `GH_PAT` | Auto-merge entre ramas | ✅ Configurado |
| `VERCEL_TOKEN` | Autenticación con Vercel | ❌ Pendiente |
| `VERCEL_ORG_ID` | ID de organización | ❌ Pendiente |
| `VERCEL_PROJECT_ID` | ID del proyecto | ❌ Pendiente |

---

## 🎯 ¿Qué Opción Elegir?

**Opción 1: Configurar Vercel Completo**
- ✅ Tendrás el pipeline completo (DEV → TEST → MAIN → Vercel)
- ✅ Sitio web público disponible
- ⏱️ Toma ~10 minutos configurar

**Opción 2: Desactivar Deployment**
- ✅ Más rápido (1 minuto)
- ✅ Los workflows de seguridad y tests siguen funcionando
- ❌ No tendrás sitio web público

---

## 💡 Recomendación

Si solo quieres **probar el flujo de seguridad** (DEV → TEST → MAIN), usa la **Opción 2**.

Si quieres el **pipeline completo con deployment**, usa la **Opción 1**.
