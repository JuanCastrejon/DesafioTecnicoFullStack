# Instrucciones del Proyecto — Prueba Técnica Full Stack

## Idioma

- Documentación, comentarios, PRs y commits: en español.
- Identificadores de código (variables, funciones, clases): en inglés.

## Stack objetivo

- Backend: FastAPI + SQLAlchemy + PostgreSQL (Supabase).
- Front demo: PHP + jQuery.
- Deploy: Vercel Serverless + Supabase.
- CI: GitHub Actions.

## Convenciones

- Mantener alcance acotado al enunciado de la prueba.
- Evitar sobreingeniería y dependencias innecesarias.
- Logging mínimo-profesional (INFO/ERROR + request_id).
- Swagger/OpenAPI debe estar operativo en `/docs`.

## Flujo Git

- main: producción.
- develop: staging.
- feature/*, fix/*, docs/* para trabajo diario.
- Commits con Conventional Commits en español.

## Higiene del repositorio

- Nunca commitear secretos (`.env`, tokens, claves).
- Excluir salidas locales (`.vercel`, caches, logs, vendor, node_modules).
- Antes de push: revisar `git status` y `git diff --staged`.
