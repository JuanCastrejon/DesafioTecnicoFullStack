# Instrucciones FastAPI Backend

Aplicable a: backend/**/*.py

- Mantener endpoints simples y claros.
- Validar query params con Pydantic/FastAPI.
- Evitar lógica de negocio en rutas; mover a servicios cuando crezca la complejidad.
- Mantener respuestas consistentes y tipadas.
- Logging estructurado mínimo con request_id.
- Priorizar legibilidad y pruebas unitarias.
