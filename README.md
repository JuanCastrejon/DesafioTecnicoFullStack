# Desafio Tecnico Full Stack

Prueba tecnica full stack con:
- API en FastAPI
- Base de datos PostgreSQL (Supabase en nube)
- Cliente PHP + jQuery
- Deploy serverless en Vercel
- CI con GitHub Actions

## Estructura del proyecto

- backend/: API FastAPI, logica de dominio y pruebas
- php-client/: interfaz de consumo en PHP + jQuery
- api/index.py: entrypoint serverless para Vercel
- .github/workflows/ci.yml: pruebas y build de Docker
- vercel.json: enrutamiento y runtime de Vercel

## Persistencia de eventos

- Fuente principal: PostgreSQL (Supabase o DB local)
- Inicializacion automatica de tabla `events` con seed de 10.000 registros
- Indices para consulta eficiente por fecha y orden compuesto (`event_date`, `event_date + id`)
- Fallback en memoria solo cuando la DB no esta disponible (para no bloquear la demo local)

## Inicio rapido

1. Copiar archivo de variables de entorno:
- backend/.env.example -> backend/.env

2. Configurar DATABASE_URL:
- Supabase (recomendado): usar pooler puerto 6543 con sslmode=require.
- BD local (opcional): mantener valor por defecto en backend/.env.

3. Ejecutar con Docker Compose:
- Supabase-first (sin contenedor db): docker compose up --build
- Con PostgreSQL local: docker compose --profile local-db up --build

4. URLs locales:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Cliente PHP: http://localhost:8080

## Cliente PHP (demo)

- Archivo principal: `php-client/index.php`
- Tecnologias: PHP 8 + jQuery + Bootstrap
- Funcionalidad: listado paginado, filtros por fecha, estados (loading/error/vacio) y modal de detalle

Variable opcional para apuntar a otra API:

- `API_BASE_URL` (por defecto `http://localhost:8000`)

## Modelo de ramas

- main: produccion
- develop: staging
- feature/*: funcionalidades
- fix/*: correcciones
- docs/*: documentacion

## Validaciones minimas

- pytest en backend
- docker build de imagen backend
- commits limpios sin archivos temporales

## CI/CD

- Workflow en GitHub Actions: `.github/workflows/ci.yml`
- En pull requests y push a ramas principales:
	- Ejecuta pruebas backend
- En push a `main`:
	- Ejecuta build de imagen Docker

## Deploy en Vercel + Supabase

Prerrequisitos:

- Vercel CLI autenticado (`vercel whoami`)
- Supabase CLI autenticado (`supabase projects list`)

1. Vincular proyecto local con Supabase (una sola vez):

```bash
supabase link --project-ref <project_ref>
```

2. Configurar variables en Vercel (Preview y Production):

- `DATABASE_URL` (pooler Supabase puerto 6543 con `sslmode=require`)
- `APP_ENV` (ej. `production`)
- `CORS_ORIGINS` (dominio del cliente PHP o frontend)

Ejemplo:

```bash
vercel env add DATABASE_URL production
vercel env add APP_ENV production
vercel env add CORS_ORIGINS production
```

3. Desplegar:

```bash
vercel
vercel --prod
```

4. Verificar endpoints publicos:

- `/health`
- `/events?page=1&size=10`
- `/events/5`
- `/docs`

Puedes usar el script:

```powershell
./scripts/smoke-api.ps1 -BaseUrl "https://tu-api.vercel.app"
```

