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

## Flujo obligatorio por feature

1. Desarrollo local en `feature/*` con commits atómicos.
2. Push de rama a remoto.
3. Verificar runs/checks en GitHub:
- `gh run list --limit 10`
- `gh run view <run_id> --log-failed` (si falla)
4. Abrir PR hacia `develop` solo cuando CI esté en verde.
5. Resolver observaciones de PR y revalidar checks.
6. Merge por PR, nunca por push directo.

## Comandos clave GitHub CLI

- Estado general de PR y ramas:
  - `gh pr status`
- Crear PR:
  - `gh pr create --base develop --head feature/<nombre> --title "feat(...): ..." --body "..."`
- Ver checks de un PR:
  - `gh pr checks <pr_number>`
- Listar runs de Actions:
  - `gh run list --limit 10`
- Inspeccionar fallo:
  - `gh run view <run_id> --log-failed`

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

## Checklist de trazabilidad antes de merge

- [ ] Commits limpios y atómicos.
- [ ] CI en GitHub en verde.
- [ ] Logs de fallos revisados si hubo errores.
- [ ] PR con descripción técnica clara.
- [ ] Evidencia de despliegue preview (si aplica).
- [ ] README/docs actualizados si cambió operación o arquitectura.
