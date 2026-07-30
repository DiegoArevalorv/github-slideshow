---
description: Verifica, guarda y publica los cambios en GitHub con un Pull Request
argument-hint: [descripción breve del cambio]
allowed-tools: Read, Glob, Grep, Bash, Task
---

Publica los cambios actuales. Descripción dada por el usuario: **$ARGUMENTS**

**No te salgas de este orden. Si un paso falla, para y explícalo en español.**

1. **Verificar primero.** Ejecuta `script/cibuild`. Si falla, lanza el agente
   `build-doctor`, arréglalo y repite. **No publiques nunca con el build en
   rojo.**

2. **Revisar el deck** con el agente `deck-reviewer` si hay cambios en `_posts/`.
   Si encuentra bloqueantes, arréglalos antes de seguir.

3. **Comprobar la rama.** `git branch --show-current`. Si estás en `master`,
   **detente** y pregunta al usuario a qué rama publicar. Nunca hagas commit
   directo a `master`.

4. **Revisar qué se va a guardar.** `git status` y `git diff --stat`. Confirma
   que no se cuelan `_site/`, `vendor/`, `.preview/` ni `node_modules` sin
   querer.

5. **Commit** con mensaje en español, imperativo, una línea de resumen y (si
   aporta) un cuerpo corto explicando el porqué.

6. **Push**: `git push -u origin <rama>`. Si falla por red, reintenta con
   esperas de 2s, 4s, 8s y 16s.

7. **Pull Request**: si no hay ya un PR abierto para esa rama, crea uno **en
   borrador** con título y descripción en español. Después suscríbete a su
   actividad para vigilar CI.

8. **Resumen final en español**: qué se publicó, en qué rama, enlace al PR, y
   qué falta para que aparezca en el sitio público (que el PR se fusione a
   `master`).
