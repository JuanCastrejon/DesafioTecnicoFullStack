# Checklist Entrega Final - Prueba Tecnica

## Estado de cumplimiento

- [x] Parte 1 (Backend funcional)
- [x] Parte 2 (Documento de arquitectura)
- [x] Parte 3 (CI/CD con pruebas y build Docker)
- [x] Parte 4 (Cliente PHP + jQuery)
- [x] Bonus de cache dedicado en memoria (TTL + LRU)

## Evidencia tecnica

- [x] Swagger operativo en `/docs`
- [x] Endpoint `GET /events` con paginacion y filtros
- [x] Endpoint `GET /events/{id}` para detalle
- [x] Indices en modelo `events` para consulta por fecha
- [x] Pruebas backend en verde

## Evidencia local validada

- [x] API local en `http://127.0.0.1:8010`
- [x] Demo PHP local en `http://127.0.0.1:8089/index.php`
- [x] Demo HTML local en `http://127.0.0.1:8090/index.html`
- [x] Listado, detalle y paginacion en ambos clientes
- [x] CORS local ajustado para puertos 8080, 8089 y 8090

## Archivos clave de entrega

- `README.md`
- `backend/app/main.py`
- `backend/app/services/events_service.py`
- `backend/app/services/cache.py`
- `backend/tests/test_health.py`
- `backend/tests/test_events_cache.py`
- `php-client/index.php`
- `php-client/index.html`
- `php-client/assets/styles/demo.css`
- `docs/arquitectura-frontend-movil.md`
- `docs/deuda-tecnica.md`
- `docs/CHECKLIST_ENTREGA_FINAL.md`
- `docs/GUIA_VIDEO_2_3_MIN.md`

## Entrega externa (fuera de repo)

- [ ] URL final del repositorio compartida al evaluador
- [ ] Mini video de 2-3 minutos grabado y publicado/enviado
