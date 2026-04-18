---
name: operacion-cli-devops-prueba
description: "Operación profesional con GitHub CLI, Supabase CLI y Vercel CLI para trazabilidad de cambios y control de calidad antes de PRs."
---

# Skill: Operación CLI DevOps para la Prueba

## Objetivo

Asegurar trazabilidad end-to-end de cada feature usando herramientas oficiales:
- GitHub CLI (`gh`) para PRs, checks, runs y releases.
- Supabase CLI (`supabase`) para estado del proyecto, migraciones y enlace.
- Vercel CLI (`vercel`) para despliegues y validación rápida.

## Regla de oro

No se abre ni se mergea PR hacia `develop` o `main` si hay checks fallidos en GitHub.

## Regla obligatoria de encoding en PR

- Nunca enviar descripciones de PR en multilinea usando `--body` inline desde PowerShell.
- Siempre crear un archivo `.md` en UTF-8 y usar `gh pr create --body-file <archivo.md>`.
- Para PRs ya creados con texto corrupto, corregir con `gh pr edit <pr_number> --body-file <archivo.md>`.
- Validar despues de crear/editar:
  - `gh pr view <pr_number> --json body -q ".body"`
  - Confirmar que no existan literales `\\n` ni secuencias corruptas tipo `├` o `�`.

## Flujo obligatorio por feature

1. Desarrollo local en `feature/*` con commits atómicos.
2. Push de rama a remoto.
3. Abrir PR en modo draft para activar CI temprano.
4. Verificar runs/checks en GitHub:
- `gh run list --limit 10`
- `gh run view <run_id> --log-failed` (si falla)
5. Pasar PR a ready for review solo cuando CI esté en verde.
6. Resolver observaciones de PR y revalidar checks.
7. Merge por PR, nunca por push directo.
8. Sincronizar rama local tras merge (`git checkout develop && git pull`).

## Comandos clave GitHub CLI

- Estado general de PR y ramas:
  - `gh pr status`
- Crear PR:
  - `gh pr create --base develop --head feature/<nombre> --title "feat(...): ..." --body-file <pr-body.md> --draft`
- Corregir body de PR existente:
  - `gh pr edit <pr_number> --body-file <pr-body.md>`
- Pasar de draft a ready:
  - `gh pr ready <pr_number>`
- Ver checks de un PR:
  - `gh pr checks <pr_number>`
- Listar runs de Actions:
  - `gh run list --limit 10`
- Inspeccionar fallo:
  - `gh run view <run_id> --log-failed`
- Merge por squash desde CLI:
  - `gh pr merge <pr_number> --squash --delete-branch`

## Comandos clave Supabase CLI

- Confirmar login:
  - `supabase projects list`
- Vincular repo con proyecto:
  - `supabase link --project-ref <ref>`
- Estado local:
  - `supabase status`
- Migraciones:
  - `supabase migration new <nombre>`
  - `supabase db push`

## Comandos clave Vercel CLI

- Confirmar autenticación:
  - `vercel whoami`
- Deploy preview:
  - `vercel`
- Deploy producción:
  - `vercel --prod`
- Variables de entorno:
  - `vercel env ls`

## Política de ramas para esta prueba

- `main`: producción/demo final.
- `develop`: integración continua (actúa como staging).
- `feature/*`: desarrollo.

Nota: No es obligatorio crear una rama adicional `staging` para esta prueba si `develop` ya cumple ese rol. Solo crear `staging` separada si aparece un requisito explícito de entornos múltiples con promoción formal.

## Protección de ramas (recomendación mínima)

- Activar protección en `develop` y `main`.
- Exigir PR para merge (sin push directo).
- Exigir check de CI de backend en verde para permitir merge.
- Verificar estado con API:
  - `gh api repos/<owner>/<repo>/branches/develop/protection`
  - `gh api repos/<owner>/<repo>/branches/main/protection`

## Checklist de trazabilidad antes de merge

- [ ] Commits limpios y atómicos.
- [ ] CI en GitHub en verde.
- [ ] Logs de fallos revisados si hubo errores.
- [ ] PR con descripción técnica clara.
- [ ] Evidencia de despliegue preview (si aplica).
- [ ] README/docs actualizados si cambió operación o arquitectura.
