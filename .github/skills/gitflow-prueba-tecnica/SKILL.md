---
name: gitflow-prueba-tecnica
description: "Define flujo de ramas, política de commits y reglas de PR para mantener entrega profesional y limpia."
---

# Skill: GitFlow para Prueba Técnica

## Objetivo

Mantener orden, trazabilidad y calidad en commits y PRs.

## Reglas

1. Ramas base:
- main = producción
- develop = staging

2. Ramas de trabajo:
- feature/<nombre>
- fix/<nombre>
- docs/<nombre>

3. Flujo:
- Toda rama de trabajo nace desde develop.
- Merge hacia develop solo por PR.
- Merge de develop a main solo por PR.
- No hacer push directo a main.

4. Commits:
- Mensajes en formato Conventional Commits (español).
- Commits atómicos y enfocados en un solo objetivo.
- Prohibido incluir archivos temporales o secretos.

## Checklist previo al commit

- [ ] `git status` revisado
- [ ] `git diff --staged` revisado
- [ ] Sin `.env`, `.vercel`, logs, caches
- [ ] Pruebas mínimas ejecutadas
- [ ] Archivos de uso interno o auditoria excluidos en `.gitignore`
- [ ] Ningun archivo de planeacion privada o evidencia interna quedo en el commit
