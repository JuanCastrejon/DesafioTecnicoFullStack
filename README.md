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

