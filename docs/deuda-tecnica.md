# Deuda Tecnica

## Estado actual

El MVP cumple endpoints de eventos, cliente demo PHP y flujo CI/PR con proteccion de ramas.

## Deuda tecnica priorizada

1. Persistencia real en PostgreSQL/Supabase
- Migrar de dataset semilla en memoria a tablas `events`.
- Agregar migraciones Alembic y seed reproducible.

2. Contrato de errores robusto
- Estandarizar errores (`code`, `message`, `details`, `request_id`).
- Manejadores globales de excepciones en FastAPI.

3. Performance para volumen real
- Implementar indices en DB para fechas y orden compuesto.
- Medir latencia de consultas con dataset >= 10k.

4. Pruebas adicionales
- Integracion contra DB real para filtros y paginacion.
- Pruebas negativas adicionales (422/500 controlado).

5. Observabilidad
- Completar trazabilidad de request_id en toda la capa API.
- Definir formato de logs consistente para debug operativo.

## Criterio de priorizacion

- Primero: riesgos que afectan exactitud funcional (datos reales y contrato de errores).
- Segundo: riesgos de operacion (performance y observabilidad).
- Tercero: mejoras de cobertura y ergonomia.
