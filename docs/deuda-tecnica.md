# Deuda Tecnica

## Proposito del documento

Este documento responde directamente al punto del desafio que pide explicar "como manejarias la deuda tecnica si la tuvieras". No describe solo pendientes abstractos: separa lo que ya se corrigio durante la prueba, lo que sigue siendo deuda real y como se priorizaria para una siguiente fase.

## Criterio de trabajo aplicado

Durante la prueba se priorizo este orden:

1. cumplir el alcance funcional del reto;
2. asegurar reproducibilidad y trazabilidad;
3. endurecer arquitectura y operacion;
4. dejar documentada la deuda restante sin ocultarla.

## Deuda que ya fue atendida durante la prueba

Estos puntos aparecian como riesgo tecnico natural del MVP inicial, pero quedaron resueltos o parcialmente resueltos en el estado actual del proyecto:

### 1. Persistencia real y escalabilidad base

Estado actual:

- el backend ya consulta PostgreSQL;
- existe bootstrap controlado por flags;
- se siembran `10.000` eventos cuando el entorno lo requiere;
- el modelo incluye indices para fecha y orden compuesto.

Evidencia:

- `backend/app/models/event.py`
- `backend/app/repositories/events_repository.py`
- `backend/app/db/bootstrap.py`

### 2. Contrato uniforme de errores

Estado actual:

- las respuestas de error siguen el contrato `code`, `message`, `details`, `request_id`;
- existe middleware de `request_id`;
- hay handlers globales para HTTP, validacion y errores no controlados.

Evidencia:

- `backend/app/core/exceptions.py`
- `backend/app/core/logging.py`
- `backend/tests/test_health.py`

### 3. Calidad automatizada minima

Estado actual:

- hay pipeline en GitHub Actions;
- se ejecutan lint, format check, pruebas y coverage minima;
- en `main` se construye la imagen Docker.

Evidencia:

- `.github/workflows/ci.yml`

## Deuda tecnica real al cierre actual

La deuda ya no esta en "hacer que funcione". La deuda real hoy esta en llevar el proyecto desde una muy buena prueba tecnica hacia una base mas cercana a produccion.

### 1. Migraciones formales de base de datos

Situacion:

- el esquema y la semilla se inicializan desde el arranque del backend cuando los flags lo permiten;
- eso funciona bien para demo, CI y entorno controlado, pero no es el mecanismo ideal para evolucion de esquema.

Pendiente:

- introducir Alembic;
- separar creacion de esquema, seed y arranque de app;
- versionar cambios de base de datos formalmente.

Prioridad:

- alta.

### 2. Bootstrap y seed acoplados al ciclo de vida de la app

Situacion:

- `init_events_storage()` se ejecuta en el lifespan de FastAPI;
- para la prueba fue util porque reduce pasos manuales y facilita reproducibilidad;
- para produccion seria mejor usar migraciones o jobs one-shot.

Pendiente:

- mover bootstrap/seed a comandos operativos independientes.

Prioridad:

- alta.

### 3. Cache local al proceso

Situacion:

- el bonus de cache fue resuelto con TTL + LRU en memoria;
- esto mejora lecturas repetidas y simplifica la prueba;
- no escala horizontalmente como una cache distribuida.

Pendiente:

- evaluar Redis o una cache compartida por entorno;
- definir politicas de invalidacion y TTL por caso de uso.

Prioridad:

- media.

### 4. Paginacion de experiencia en la demo PHP

Situacion:

- el backend sí pagina correctamente;
- la demo, en cambio, descarga resultados paginados en bloques de `100` y luego pagina localmente para simplificar UX y mantener el codigo del cliente liviano.

Impacto:

- es aceptable para demo;
- no seria la estrategia deseable para un frontend productivo con alto volumen.

Pendiente:

- hacer paginacion server-driven de extremo a extremo desde el cliente.

Prioridad:

- alta.

### 5. Duplicacion entre `index.php` e `index.html`

Situacion:

- existen dos variantes del cliente para soportar modo PHP local y variante estatica para Vercel;
- esto resolvio una necesidad operativa real, pero duplica HTML/JS.

Pendiente:

- extraer JS compartido;
- minimizar divergencia entre ambas variantes.

Prioridad:

- media.

### 6. Observabilidad y operacion avanzada

Situacion:

- ya existe logging estructurado y `request_id`;
- aun faltan piezas tipicas de una operacion madura.

Pendiente:

- metricas;
- trazas;
- smoke test serverless automatizado;
- alertas basicas por degradacion.

Prioridad:

- media.

### 7. Hardening adicional de seguridad y pipeline

Situacion:

- el pipeline actual cubre calidad base;
- no incluye todavia escaneos de seguridad ni validaciones mas profundas de supply chain.

Pendiente:

- agregar chequeos de seguridad basicos;
- revisar dependencias y politica de actualizacion.

Prioridad:

- baja/media.

## Como la gestionaria

La gestion de deuda seguiria un enfoque pragmatico:

1. no mezclar deuda estructural con mejoras cosmeticas;
2. priorizar primero lo que reduce riesgo operativo;
3. atacar la deuda en cambios pequenos y trazables;
4. dejar evidencia en PR, README y docs cuando una deuda se resuelva.

## Plan sugerido por fases

### Fase 1

- introducir Alembic;
- separar bootstrap/seed del arranque;
- hacer paginacion end-to-end en el cliente.

### Fase 2

- definir estrategia de cache por entorno;
- extraer JS compartido del cliente;
- agregar smoke deploy automatizado.

### Fase 3

- ampliar observabilidad;
- agregar chequeos de seguridad y endurecimiento operativo.

## Conclusion

La deuda tecnica de este proyecto esta controlada y visible. Lo importante es que no quedo escondida bajo el "funciona". El proyecto ya resolvio una parte importante del hardening durante la prueba, y lo pendiente esta identificado con criterio de prioridad y con una ruta clara de evolucion.
