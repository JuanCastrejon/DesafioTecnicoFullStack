---
name: documentacion-viva-prueba
description: "Mantener README, docs y evidencias alineadas con el estado real del código de la prueba técnica."
---

# Skill: Documentación Viva de la Prueba

## Cuándo actualizar

- Al cerrar una feature relevante
- Al cambiar arquitectura o despliegue
- Al agregar variables de entorno o dependencias
- Antes de mergear a develop/main

## Archivos que deben mantenerse al día

- README.md
- docs/ACCESOS_Y_CONEXIONES.md
- docs/REPOSITORIO_Y_ARCHIVOS_A_SUBIR.md
- docs/arquitectura-frontend-movil.md (cuando se cree)
- docs/deuda-tecnica.md (cuando se cree)

## Checklist documental

- [ ] Swagger y rutas documentadas
- [ ] Variables de entorno explicadas
- [ ] Instrucciones de ejecución local validadas
- [ ] Evidencia mínima de pruebas/CI

## Regla de higiene documental

- Si un archivo es solo para auditoria interna, plan personal o guion privado, no se commitea al remoto.
- Antes de crear o conservar documentacion sin valor para el repo, agregar su ruta a `.gitignore`.
- Mantener en el repositorio solo documentos que aporten valor a revisores, reclutadores o despliegue.
- Si un documento no forma parte de la entrega publica, debe quedarse fuera del repo y del PR.

## Estándar pendiente: hardening de contrato API

Aplicar cuando se cierre el MVP funcional de endpoints (sin adelantar alcance antes de tiempo):

- Contrato de error uniforme (`code`, `message`, `details`, `request_id`).
- Manejadores globales de excepciones.
- Respuestas OpenAPI documentadas para `200/400/404/422/500`.
- Pruebas automáticas de rutas felices y negativas.
- Logging con `request_id` en todos los errores.
