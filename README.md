# Desafio Tecnico Full Stack

Prueba tecnica full stack para el modulo de eventos con:
- API en FastAPI
- Persistencia en PostgreSQL (Supabase o local)
- Cliente demo en PHP + jQuery
- Deploy serverless en Vercel
- CI con GitHub Actions

## Estado de cumplimiento del desafio

### Parte 1 - Backend (funcional)

Cumplido.

- GET /events con paginacion y filtro por rango de fechas
- GET /events/{id} para detalle
- GET /ready para disponibilidad operativa de la API y verificacion de base de datos
- Escalabilidad base con paginacion y modelo de persistencia en PostgreSQL
- Swagger disponible en /docs
- Bonus implementado: cache dedicado en memoria (TTL + LRU) para respuestas frecuentes de listado y detalle
- Fase 2 completada: separacion adicional de responsabilidades en use-cases y repositorio, con pruebas de integracion sobre PostgreSQL
- Fase 3 aplicada: readiness de base de datos, Docker multi-stage y health checks operativos

### Parte 2 - Arquitectura de apps moviles / enfoque tecnico (documental)

Cumplido.

Documento principal:
- [docs/arquitectura-frontend-movil.md](docs/arquitectura-frontend-movil.md)

Incluye:
- Propuesta de arquitectura frontend
- Estructura de carpetas
- Estrategia de estado
- Patron de consumo de APIs
- Explicacion de implementacion

### Parte 3 - CI/CD sencillo (funcional)

Cumplido.

Workflow:
- [.github/workflows/ci.yml](.github/workflows/ci.yml)

Implementa:
- Pruebas unitarias backend en PR y push a develop/main
- Build de imagen Docker en push a main

### Parte 4 - PHP + jQuery (funcional)

Cumplido.

- [php-client/index.php](php-client/index.php): listado, filtros, modal de detalle y AJAX
- [php-client/index.html](php-client/index.html): variante estatica para Vercel
- Estilos compartidos en [php-client/assets/styles/demo.css](php-client/assets/styles/demo.css)

## Estructura del proyecto

- backend/: API FastAPI, dominio y pruebas
- backend/app/use_cases/: orquestacion de casos de uso de eventos
- backend/app/ports/: contratos internos para cache y repositorio
- backend/app/db/health.py: verificacion de disponibilidad de base de datos
- php-client/: interfaz PHP + jQuery
- api/index.py: entrypoint serverless para Vercel
- .github/workflows/ci.yml: pipeline CI
- docs/: documentacion tecnica y operativa

## Persistencia y escalabilidad

- Fuente principal: PostgreSQL (Supabase o DB local)
- Inicializacion automatica de tabla events con seed de 10.000 registros
- Indices orientados a consulta por fecha y orden compuesto
- Fallback en memoria controlado por flag explicita (`ENABLE_IN_MEMORY_FALLBACK`)

### Decisiones de demo vs produccion

- Demo/local:
	- `ENABLE_IN_MEMORY_FALLBACK=true` permite operar sin bloquear demo cuando la DB no esta disponible.
- Produccion/CI:
	- `ENABLE_IN_MEMORY_FALLBACK=false` (valor recomendado) para no ocultar incidentes de infraestructura.
	- Errores SQL se registran con logging estructurado y la API responde error uniforme.

Esta separacion evita el fallback silencioso y deja explicito el trade-off operativo por entorno.

## Levantar localmente (modo validado)

### 1) API local (FastAPI en 8010)

Desde PowerShell:

```powershell
Set-Location "desafio-tecnico-full-stack/backend"
$env:CORS_ORIGINS="http://localhost:8080,http://127.0.0.1:8080,http://localhost:8089,http://127.0.0.1:8089,http://localhost:8090,http://127.0.0.1:8090"
c:/Users/juand/source/repos/DesafioTecnicoFullStack/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8010
```

### 2) Demo PHP local (index.php en 8089)

Si `php` ya esta en PATH:

```powershell
Set-Location "desafio-tecnico-full-stack/php-client"
php -S 127.0.0.1:8089
```

Si el terminal aun no toma PATH (caso Windows tras instalacion con winget), usar ruta absoluta:

```powershell
Set-Location "desafio-tecnico-full-stack/php-client"
& "C:/Users/juand/AppData/Local/Microsoft/WinGet/Packages/PHP.PHP.8.3_Microsoft.Winget.Source_8wekyb3d8bbwe/php.exe" -S 127.0.0.1:8089
```

### 3) Demo HTML local (index.html en 8090)

```powershell
Set-Location "desafio-tecnico-full-stack/php-client"
c:/Users/juand/source/repos/DesafioTecnicoFullStack/.venv/Scripts/python.exe -m http.server 8090
```

### 4) URLs locales

- API: http://127.0.0.1:8010
- Swagger: http://127.0.0.1:8010/docs
- Demo PHP: http://127.0.0.1:8089/index.php
- Demo HTML: http://127.0.0.1:8090/index.html

## Dev Container (opcional recomendado)

Para facilitar la evaluacion tecnica en entorno reproducible, el repositorio incluye configuracion Dev Container en:
- [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json)

Pasos:
1. Abrir el repositorio en VS Code.
2. Ejecutar el comando: Dev Containers: Reopen in Container.
3. Esperar la provision inicial (instala PHP CLI y dependencias Python del backend).
4. Ejecutar los mismos comandos de la seccion Levantar localmente.

Notas:
- Esta opcion no reemplaza Docker Compose ni modo local tradicional; es una alternativa para estandarizar el entorno del evaluador.
- Los puertos 8010, 8089, 8090 y 8000 quedan expuestos para API y demos.

## Levantar con Docker Compose

1. Copiar variables de entorno:
- backend/.env.example -> backend/.env

2. Levantar stack:

```bash
docker compose up --build
```

Opcional con PostgreSQL local en contenedor:

```bash
docker compose --profile local-db up --build
```

Puertos en modo Docker Compose:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Readiness operativa: http://localhost:8000/ready
- Demo PHP: http://localhost:8080

## CI/CD

- Pipeline en [.github/workflows/ci.yml](.github/workflows/ci.yml)
- test-backend:
	- Levanta PostgreSQL de pruebas en servicio
	- Instala dependencias
	- Ejecuta lint con `ruff check`
	- Ejecuta validacion de formato con `ruff format --check`
	- Ejecuta pytest con coverage minimo (70%)
- docker-build:
	- Se ejecuta en push a main
	- Construye imagen Docker multi-stage del backend con healthcheck

## Pruebas locales reproducibles

Sin depender de variables implicitas como `PYTHONPATH`:

```powershell
Set-Location "desafio-tecnico-full-stack"
c:/Users/juand/source/repos/DesafioTecnicoFullStack/.venv/Scripts/python.exe -m pytest backend/tests -q
```

Este comando replica el mismo esquema de imports esperado en CI y en contenedor.

## Deploy en Vercel + Supabase

Prerrequisitos:
- Vercel CLI autenticado
- Supabase CLI autenticado

1. Vincular con Supabase (una sola vez):

```bash
supabase link --project-ref <project_ref>
```

2. Variables en Vercel (preview y production):
- DATABASE_URL (pooler Supabase puerto 6543 con sslmode=require)
- APP_ENV=production
- CORS_ORIGINS=<dominios frontend permitidos>

3. Desplegar:

```bash
vercel
vercel --prod
```

4. Smoke test:

```powershell
./scripts/smoke-api.ps1 -BaseUrl "https://tu-api.vercel.app"
```

## Deuda tecnica

Plan y priorizacion:
- [docs/deuda-tecnica.md](docs/deuda-tecnica.md)

## Demo publica

- API: https://desafio-tecnico-full-stack.vercel.app/docs
- Cliente: https://php-client-chi.vercel.app

