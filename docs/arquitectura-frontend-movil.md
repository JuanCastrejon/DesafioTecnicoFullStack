# Arquitectura Frontend Movil (Propuesta Tecnica)

## Proposito del documento

Este documento responde a la Parte 2 del desafio tecnico, que pide definir para el backend de eventos:

- propuesta tecnica de arquitectura frontend;
- estructura de carpetas;
- estrategia de estado;
- patron de consumo de APIs;
- explicacion de como lo implementaria.

Importante:

- la implementacion funcional exigida en frontend para esta prueba fue la demo en `PHP + jQuery`;
- este documento no reemplaza esa demo;
- documenta como evolucionaria el modulo de eventos hacia una app movil o frontend mas robusto apoyado en el backend ya construido.

## Punto de partida real del proyecto

El backend implementado ya expone lo necesario para construir un cliente moderno:

- `GET /events` con paginacion y filtros por rango de fechas;
- `GET /events/{id}` para detalle;
- Swagger/OpenAPI operativo;
- contrato de errores uniforme;
- semantica de `health` y `ready`.

Eso permite que la propuesta de frontend no sea teorica pura, sino una extension natural del contrato actual del backend.

## Objetivo de la arquitectura propuesta

Construir un frontend movil o multiplataforma que:

1. consuma el backend de eventos de forma tipada y desacoplada;
2. escale a volumen alto sin depender de traer todos los eventos al cliente;
3. soporte estados de carga, vacio, error y exito de forma consistente;
4. permita evolucion posterior a otros modulos de la app social.

## Principios de diseño

### 1. Separacion por capas

Separar presentacion, aplicacion, dominio e infraestructura para evitar que la UI dependa directamente de detalles HTTP o serializacion.

### 2. API-first

El frontend se construye a partir del contrato expuesto por FastAPI/OpenAPI, no de respuestas implícitas ni acoplamientos accidentales.

### 3. Escalabilidad por paginacion real

La app no deberia replicar el atajo de demo de descargar muchos registros y paginar localmente. En una app real, la paginacion debe ser server-driven y conservar el backend como fuente de verdad.

### 4. Evolucion incremental

La arquitectura debe empezar simple, pero permitir agregar autenticacion, cache offline, favoritos, RSVP u otros modulos sin rehacer la base.

## Stack sugerido

Para una app movil o frontend moderno, propondria:

- Flutter o React Native para cliente movil;
- consumo HTTP tipado;
- almacenamiento local ligero para cache;
- manejo de estado por feature;
- configuracion por entornos (`dev`, `staging`, `prod`).

No se implemento esta capa en la prueba porque el entregable funcional del frontend era `PHP + jQuery`; por eso esta parte se mantuvo documental, tal como lo permite el enunciado.

## Arquitectura propuesta

### Capas

1. `presentation`
   - pantallas, widgets, componentes, estado visual.
2. `application`
   - controllers/view models/use cases orientados al flujo.
3. `domain`
   - entidades y contratos del negocio.
4. `infrastructure`
   - clientes HTTP, DTOs, repositorios concretos y persistencia local.

### Beneficio

Esta separacion evita:

- meter parseo HTTP en la UI;
- mezclar estado visual con reglas de negocio;
- acoplar la app a un proveedor de red o storage especifico.

## Estructura de carpetas sugerida

```text
apps/mobile/lib/
  core/
    config/
    errors/
    logger/
    network/
    storage/
  features/
    events/
      presentation/
        pages/
        widgets/
        controllers/
        states/
      application/
        usecases/
        mappers/
      domain/
        entities/
        repositories/
      infrastructure/
        datasources/
        dtos/
        repositories/
  shared/
    widgets/
    utils/
```

## Modelado del modulo de eventos

### Entidades de dominio

Minimo esperado:

- `EventSummary`
- `EventDetail`
- `EventLocation`
- `EventQuery`
- `PaginatedResult<EventSummary>`

### Casos de uso

- `ListEvents`
- `GetEventDetail`

### Contratos

- `EventsRepository`
- `EventsRemoteDataSource`
- `EventsLocalCache` si se requiere offline/cache posterior

## Estrategia de estado

La estrategia recomendada es por feature y por caso de uso, no global para toda la app.

### Estados base

Cada pantalla debe contemplar como minimo:

- `initial`
- `loading`
- `success`
- `empty`
- `error`

### Estado del listado

Debe modelar:

- filtros activos;
- pagina actual;
- tamaño de pagina;
- total;
- items cargados;
- indicador de carga inicial;
- indicador de carga incremental;
- error recuperable.

### Estado del detalle

Debe modelar:

- id seleccionado;
- carga de detalle;
- detalle listo;
- error de consulta.

### Recomendacion de gestion

Se puede usar `Riverpod`, `Bloc` o una estrategia equivalente. Lo importante no es la libreria sino mantener:

- estado local por feature;
- efectos de red encapsulados;
- transiciones predecibles y testeables.

## Patron de consumo de APIs

### Flujo recomendado

1. la UI dispara una accion;
2. el controller/view model invoca un use case;
3. el use case usa un repositorio de dominio;
4. el repositorio delega al datasource remoto;
5. el datasource consume HTTP y transforma DTOs;
6. el resultado vuelve como entidades al dominio y a la presentacion.

### Mapeo

Se recomienda este flujo:

- DTO HTTP -> modelo de infraestructura -> entidad de dominio -> estado de UI

Esto evita exponer estructuras de red directamente en componentes visuales.

### Manejo de errores

El frontend deberia mapear el contrato del backend:

- `validation_error`
- `bad_request`
- `not_found`
- `service_unavailable`
- `internal_server_error`

De esa forma la UI puede responder distinto a:

- filtro invalido;
- evento inexistente;
- indisponibilidad temporal del servicio.

## Estrategia de paginacion y volumen

Como el reto pide pensar en `10.000+` eventos, la estrategia correcta en frontend seria:

1. pedir pagina inicial con `page` y `size`;
2. refrescar lista solo con los filtros visibles;
3. soportar "load more" o paginacion numerada sin cargar todo el dataset;
4. cachear solo lo necesario para UX, no el universo completo de eventos.

### Decision importante

La demo PHP actual simplifica esto y pagina en cliente despues de traer bloques del backend. Esa decision fue valida para el entregable funcional de la prueba, pero en una app movil real propondria paginacion remota directa.

## Estrategia offline / cache local

Si el producto evolucionara de verdad a app social movil, propondria una estrategia offline-first moderada:

1. mostrar ultimo listado cacheado si existe;
2. refrescar en segundo plano cuando haya conectividad;
3. persistir detalle de eventos consultados recientemente;
4. invalidar cache por TTL o por rango de fechas.

Para esta prueba no se implemento esta capa porque el enunciado la pide como enfoque tecnico, no como desarrollo funcional.

## Seguridad y configuracion

### Configuracion por entorno

Definir:

- `baseUrl` por ambiente;
- timeouts;
- flags de logging;
- politicas de reintento.

### Politica de red

- timeout corto;
- retry acotado solo en errores transitorios;
- no repetir solicitudes invalidas de negocio.

## Como lo implementaria por fases

### Fase 1

- cliente de eventos;
- listado paginado;
- filtros por fecha;
- pantalla de detalle;
- manejo de errores y vacio.

### Fase 2

- cache local;
- refresco incremental;
- mejoras de observabilidad del cliente.

### Fase 3

- capacidades offline;
- sincronizacion mas avanzada;
- nuevos modulos relacionados a eventos.

## Relacion con la implementacion real de esta prueba

La relacion entre este documento y el codigo actual es:

- el backend ya materializa el contrato que esta propuesta consumiria;
- la demo `PHP + jQuery` valida funcionalmente lista, filtros, detalle y consumo AJAX;
- este documento cubre la parte documental pedida por la prueba para una arquitectura frontend futura.

En otras palabras:

- `php-client/` demuestra funcionalidad inmediata;
- este documento demuestra criterio de arquitectura para una evolucion posterior.

## Cierre

Este documento fue diseñado precisamente por lo que pide el enunciado en la Parte 2. No pretende competir con la demo funcional ni inventar alcance extra. Su objetivo es mostrar como estructuraria un frontend mas serio sobre el backend de eventos ya construido, manteniendo desacoplamiento, paginacion real, estados claros y una ruta limpia de evolucion.
