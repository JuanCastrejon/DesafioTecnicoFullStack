# Arquitectura Frontend Movil (Propuesta Tecnica)

## Objetivo

Definir una arquitectura de app movil offline-first para consumir la API de eventos y escalar luego a modulos ERP.

## Principios

- Offline-first: la app funciona sin red y sincroniza cuando hay conectividad.
- Separacion por capas: presentacion, aplicacion, dominio e infraestructura.
- Contratos estables: consumo API por clientes tipados y DTOs versionados.
- Observabilidad minima: logs por caso de uso y trazabilidad de errores.

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
      data/
        datasources/
        models/
        repositories/
      domain/
        entities/
        repositories/
        usecases/
      presentation/
        controllers/
        pages/
        widgets/
  shared/
    widgets/
    utils/
```

## Estrategia de estado

- Estado local por feature con controller/reactividad (ej. Riverpod o Bloc).
- Estados base por pantalla:
  - initial
  - loading
  - success
  - empty
  - error
- Cache local para lecturas de listado y detalle.

## Patron de consumo API

- Capa `datasource` maneja HTTP y parseo DTO.
- Capa `repository` orquesta fuente remota + cache local.
- Capa `usecase` expone reglas de negocio al controlador.
- Mapeo DTO -> entidad de dominio sin exponer detalles HTTP a UI.

## Flujo offline-first de eventos

1. UI solicita listado de eventos.
2. Repository retorna cache local inmediata si existe.
3. En paralelo intenta refresco remoto.
4. Si remoto responde, actualiza cache y notifica UI.
5. Si remoto falla, conserva cache y muestra aviso no bloqueante.

## Seguridad y configuracion

- URL base por entorno (`dev`, `staging`, `prod`).
- Timeouts y reintentos acotados.
- Manejo consistente de errores de red/servidor.

## Criterios de calidad

- Pruebas unitarias de usecases y repositories.
- Pruebas de widgets para estados criticos.
- Contratos API versionados y documentados en OpenAPI.

## Estado de implementacion en esta prueba

- Backend de eventos implementado y documentado en Swagger (`/docs`).
- Cliente demo funcional en PHP + jQuery para listado y detalle.
- CI minimo implementado con pruebas unitarias y build Docker en GitHub Actions.
- Esta propuesta mantiene enfoque documental para evolucionar a app movil offline-first en siguientes fases.

## Cobertura explicita del enunciado (Parte 2)

- Propuesta tecnica de arquitectura frontend: seccion "Principios".
- Estructura de carpetas: seccion "Estructura de carpetas sugerida".
- Estrategia de estado: seccion "Estrategia de estado".
- Patron de consumo API: seccion "Patron de consumo API".
- Como se implementaria: secciones "Flujo offline-first", "Seguridad y configuracion" y "Estado de implementacion".
