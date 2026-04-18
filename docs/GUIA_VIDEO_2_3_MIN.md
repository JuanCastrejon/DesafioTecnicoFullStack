# Guia de Video (2-3 minutos)

## Objetivo

Mostrar de forma breve que el proyecto cumple el enunciado de la prueba tecnica.

## Guion sugerido

### 0:00 - 0:20 | Introduccion

- Presentar el repositorio y objetivo: modulo de eventos.
- Mencionar stack: FastAPI + PostgreSQL + PHP/jQuery + CI.

### 0:20 - 0:50 | Como levantar el proyecto

- Mostrar `README.md` con comandos locales.
- Levantar API local (8010).
- Levantar demo PHP (8089) o demo HTML (8090).

### 0:50 - 1:30 | Listado de eventos

- Abrir cliente demo.
- Mostrar carga de `GET /events?page=1&size=10`.
- Cambiar pagina para evidenciar paginacion.
- Probar filtro por fechas.

### 1:30 - 2:00 | Detalle de evento

- Abrir modal de detalle desde la tabla.
- Confirmar campos: titulo, descripcion, fecha, ubicacion.
- Mencionar consumo AJAX con jQuery.

### 2:00 - 2:30 | Swagger, CI/CD y cierre

- Mostrar `/docs` en Swagger.
- Resumir CI: pruebas unitarias + build Docker en GitHub Actions.
- Mencionar bonus implementado: cache dedicado en memoria para respuestas frecuentes.

## Checklist antes de grabar

- API responde en local o produccion.
- Demo muestra datos sin errores.
- Tener una pestaña lista con `README.md`.
- Tener abierta la URL de Swagger.
- Confirmar audio claro y zoom legible.
