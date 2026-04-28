# Desafio Tecnico Full Stack

Prueba tecnica full stack para el modulo de eventos con:
- API en FastAPI
- Persistencia en PostgreSQL (Supabase o local)
- Cliente demo en PHP + jQuery
- Deploy serverless en Vercel
- CI con GitHub Actions

## Estado de cumplimiento del desafio

### Parte 1 - Backend (funcional)

Cumplido.

- GET /events con paginacion y filtro por rango de fechas
- GET /events/{id} para detalle
- GET /ready para disponibilidad operativa de la API y verificacion de base de datos
- Escalabilidad base con paginacion y modelo de persistencia en PostgreSQL
- Swagger disponible en /docs
- Bonus implementado: cache dedicado en memoria (TTL + LRU) para respuestas frecuentes de listado y detalle
- Separacion adicional de responsabilidades en use-cases y repositorio, con pruebas de integracion sobre PostgreSQL
- Readiness de base de datos, Docker multi-stage y health checks operativos

### Parte 2 - Arquitectura de apps moviles / enfoque tecnico (documental)

Cumplido.

Documento principal:
- [docs/arquitectura-frontend-movil.md](docs/arquitectura-frontend-movil.md)

Incluye:
- Propuesta de arquitectura frontend
- Estructura de carpetas
- Estrategia de estado
- Patron de consumo de APIs
- Explicacion de implementacion

### Parte 3 - CI/CD sencillo (funcional)

Cumplido.

Workflow:
- [.github/workflows/ci.yml](.github/workflows/ci.yml)

Implementa:
- Pruebas unitarias backend en PR y push a develop/main
- Build de imagen Docker en push a main

### Parte 4 - PHP + jQuery (funcional)

Cumplido.

- [php-client/index.php](php-client/index.php): listado, filtros, modal de detalle y AJAX
- [php-client/index.html](php-client/index.html): variante estatica para Vercel
- Estilos compartidos en [php-client/assets/styles/demo.css](php-client/assets/styles/demo.css)

## Estructura del proyecto

- backend/: API FastAPI, dominio y pruebas
- backend/app/use_cases/: orquestacion de casos de uso de eventos
- backend/app/ports/: contratos internos para cache y repositorio
- backend/app/db/health.py: verificacion de disponibilidad de base de datos
- php-client/: interfaz PHP + jQuery
- api/index.py: entrypoint serverless para Vercel
- .github/workflows/ci.yml: pipeline CI
- docs/: documentacion tecnica y operativa

## Persistencia y escalabilidad

- Fuente principal: PostgreSQL (Supabase o DB local)
- Inicializacion automatica de tabla events con seed de 10.000 registros
- Indices orientados a consulta por fecha y orden compuesto
- Fallback en memoria controlado por flag explicita (`ENABLE_IN_MEMORY_FALLBACK`)

## Modos operativos Docker

| Modo | DB requerida | Fallback | Bootstrap/Seed |
|---|---:|---:|---:|
| Dev Container | Opcional | Opcional por env | Desactivado por defecto |
| Compose base (`docker-compose.yml`) | No | Activado por defecto | Desactivado |
| Compose + local-db (`docker-compose.local-db.yml`) | Si | Desactivado | Activado |
| CI | Si | Desactivado | Desactivado |

### Decisiones de demo vs produccion

- Demo/local:
	- `ENABLE_IN_MEMORY_FALLBACK=true` permite operar sin bloquear demo cuando la DB no esta disponible.
- Produccion/CI:
	- `ENABLE_IN_MEMORY_FALLBACK=false` (valor recomendado) para no ocultar incidentes de infraestructura.
	- Errores SQL se registran con logging estructurado y la API responde error uniforme.

Esta separacion evita el fallback silencioso y deja explicito el trade-off operativo por entorno.

## Levantar localmente (modo validado)

### 1) API local (FastAPI en 8010)

Hay dos formas utiles de levantar la API localmente fuera de Docker:

#### Opcion A: demo local sin depender de PostgreSQL

Usa fallback en memoria. Es la forma mas simple si solo quieres probar la API y la demo sin configurar base de datos.

```powershell
Set-Location "desafio-tecnico-full-stack/backend"
$env:CORS_ORIGINS="http://localhost:8080,http://127.0.0.1:8080,http://localhost:8089,http://127.0.0.1:8089,http://localhost:8090,http://127.0.0.1:8090"
$env:ENABLE_IN_MEMORY_FALLBACK="true"
$env:RUN_DB_BOOTSTRAP="false"
$env:SEED_EVENTS="false"
c:/Users/juand/source/repos/DesafioTecnicoFullStack/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

#### Opcion B: API local conectada a PostgreSQL o Supabase

Si quieres validar persistencia real fuera de Docker, entonces si debes definir `DATABASE_URL`.

Puedes hacerlo con variables de entorno en PowerShell o creando `backend/.env` a partir de `backend/.env.example`.

Ejemplo con variables en PowerShell:

```powershell
Set-Location "desafio-tecnico-full-stack/backend"
$env:CORS_ORIGINS="http://localhost:8080,http://127.0.0.1:8080,http://localhost:8089,http://127.0.0.1:8089,http://localhost:8090,http://127.0.0.1:8090"
$env:DATABASE_URL="postgresql+psycopg://postgres.<project-id>:<password>@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
$env:ENABLE_IN_MEMORY_FALLBACK="false"
c:/Users/juand/source/repos/DesafioTecnicoFullStack/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

Nota:

- si no defines `DATABASE_URL`, la app intentara usar `postgresql+psycopg://postgres:postgres@localhost:5432/events_db`;
- si tampoco tienes esa DB local disponible y `ENABLE_IN_MEMORY_FALLBACK=false`, `GET /events` y `GET /ready` fallaran.

### 2) Demo PHP local (index.php en 8089)

Si `php` ya esta en PATH:

```powershell
Set-Location "desafio-tecnico-full-stack/php-client"
php -S 127.0.0.1:8089
```

Si el terminal aun no toma PATH (caso Windows tras instalacion con winget), usar ruta absoluta:

```powershell
Set-Location "desafio-tecnico-full-stack/php-client"
& "C:/Users/juand/AppData/Local/Microsoft/WinGet/Packages/PHP.PHP.8.3_Microsoft.Winget.Source_8wekyb3d8bbwe/php.exe" -S 127.0.0.1:8089
```

### 3) Demo HTML local (index.html en 8090)

```powershell
Set-Location "desafio-tecnico-full-stack/php-client"
c:/Users/juand/source/repos/DesafioTecnicoFullStack/.venv/Scripts/python.exe -m http.server 8090
```

### 4) URLs locales

- API: http://127.0.0.1:8010
- Swagger: http://127.0.0.1:8010/docs
- Demo PHP: http://127.0.0.1:8089/index.php
- Demo HTML: http://127.0.0.1:8090/index.html

## Dev Container (opcional recomendado)

Para facilitar la evaluacion tecnica en entorno reproducible, el repositorio incluye configuracion Dev Container en:
- [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json)

Pasos:
1. Abrir el repositorio en VS Code.
2. Ejecutar el comando: Dev Containers: Reopen in Container.
3. Esperar la provision inicial (instala PHP CLI y dependencias Python del backend).
4. Ejecutar los mismos comandos de la seccion Levantar localmente.

Notas:
- Esta opcion no reemplaza Docker Compose ni modo local tradicional; es una alternativa para estandarizar el entorno del evaluador.
- Los puertos 8010, 8089, 8090 y 8000 quedan expuestos para API y demos.

## Levantar con Docker Compose

### Aclaracion sobre variables de entorno

En el estado actual del proyecto, `backend/.env` no es obligatorio para usar Docker Compose.

Modos disponibles:

- Modo base:
  - no requiere `backend/.env`
  - usa `ENABLE_IN_MEMORY_FALLBACK=true`
  - permite levantar API + demo aun sin PostgreSQL disponible
- Modo con DB local:
  - no requiere `backend/.env`
  - usa `docker-compose.local-db.yml` para provisionar PostgreSQL en contenedor
- Modo apuntando a Supabase u otra DB externa:
  - requiere definir `DATABASE_URL`
  - lo mas claro es exportarla en tu shell o definirla en un `.env` en la raiz del repositorio antes de ejecutar `docker compose`

`backend/.env.example` queda como referencia util para ejecucion local fuera de Docker o para documentar el formato esperado de variables, pero no es un prerrequisito para levantar Compose en los modos validados del repositorio.

### 1) Modo base (sin DB local, fallback en memoria)

```bash
docker compose up --build
```

Comportamiento esperado:

- API en `http://localhost:8000`
- Demo PHP en `http://localhost:8080`
- `GET /health` responde OK
- `GET /events` responde usando fallback en memoria si no hay DB

### 2) Modo con PostgreSQL local en contenedor

```bash
docker compose -f docker-compose.yml -f docker-compose.local-db.yml up --build
```

Comportamiento esperado:

- PostgreSQL se levanta en el servicio `db`
- la API usa `DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/events_db`
- `RUN_DB_BOOTSTRAP=true`
- `SEED_EVENTS=true`
- `ENABLE_IN_MEMORY_FALLBACK=false`

### 3) Opcional: usar una base externa como Supabase desde Docker Compose

Si quieres levantar el contenedor `api` apuntando a Supabase en lugar de `db`, define antes `DATABASE_URL` en tu entorno.

Ejemplo en PowerShell:

```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres.<project-id>:<password>@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
docker compose up --build
```

Si usas una DB externa, conviene revisar tambien estas variables segun el caso:

```powershell
$env:ENABLE_IN_MEMORY_FALLBACK="false"
$env:RUN_DB_BOOTSTRAP="false"
$env:SEED_EVENTS="false"
```

### 4) Smoke test automatizado de Docker Compose:

```powershell
./scripts/smoke-docker-compose.ps1
```

Opciones:

```powershell
./scripts/smoke-docker-compose.ps1 -OnlyBase
./scripts/smoke-docker-compose.ps1 -OnlyLocalDb
```

Puertos en modo Docker Compose:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Readiness operativa: http://localhost:8000/ready
- Demo PHP: http://localhost:8080

## CI/CD

- Pipeline en [.github/workflows/ci.yml](.github/workflows/ci.yml)
- test-backend:
	- Levanta PostgreSQL de pruebas en servicio
	- Instala dependencias
	- Ejecuta lint con `ruff check`
	- Ejecuta validacion de formato con `ruff format --check`
	- Ejecuta pytest con coverage minimo (70%)
- docker-build:
	- Se ejecuta en push a main
	- Construye imagen Docker multi-stage del backend con healthcheck

## Pruebas locales reproducibles

Sin depender de variables implicitas como `PYTHONPATH`:

```powershell
Set-Location "desafio-tecnico-full-stack"
c:/Users/juand/source/repos/DesafioTecnicoFullStack/.venv/Scripts/python.exe -m pytest backend/tests -q
```

Este comando replica el mismo esquema de imports esperado en CI y en contenedor.

## Deploy en Vercel + Supabase

Prerrequisitos:
- Vercel CLI autenticado
- Supabase CLI autenticado

1. Vincular con Supabase (una sola vez):

```bash
supabase link --project-ref <project_ref>
```

2. Variables en Vercel (preview y production):
- DATABASE_URL (pooler Supabase puerto 6543 con sslmode=require)
- APP_ENV=production
- CORS_ORIGINS=<dominios frontend permitidos>

3. Desplegar:

```bash
vercel
vercel --prod
```

4. Smoke test:

```powershell
./scripts/smoke-api.ps1 -BaseUrl "https://tu-api.vercel.app"
```

## Deuda tecnica

Plan y priorizacion:
- [docs/deuda-tecnica.md](docs/deuda-tecnica.md)

## Demo publica

- API: https://desafio-tecnico-full-stack.vercel.app/docs
- Cliente: https://php-client-chi.vercel.app

