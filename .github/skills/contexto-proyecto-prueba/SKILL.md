---
name: contexto-proyecto-prueba
description: "Contexto operativo de la prueba técnica Full Stack: alcance, arquitectura, despliegue y criterios de entrega."
---

# Skill: Contexto del Proyecto de Prueba

## Alcance funcional obligatorio

1. Backend:
- GET /events con paginación y filtro por fechas
- GET /events/{id}
- Escalabilidad para 10k+ eventos (índices + paginación)

2. Documento técnico (arquitectura móvil/frontend)

3. CI/CD mínimo:
- pruebas unitarias
- build Docker

4. Cliente PHP + jQuery:
- listado de eventos
- detalle en modal por AJAX

## Arquitectura base

- FastAPI + SQLAlchemy + Pydantic
- PostgreSQL en Supabase
- API en Vercel Serverless
- Swagger en `/docs`

## Criterios de éxito

- Cumplimiento exacto del enunciado
- Repositorio limpio sin archivos basura
- Flujo de ramas profesional
- README claro y demo reproducible
