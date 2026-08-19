---
description: Añade una diapositiva a la presentación actual
argument-hint: <título o contenido de la diapositiva> [| después de "otra slide"]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

Añade una diapositiva nueva: **$ARGUMENTS**

Si no se indicó contenido, pregúntalo.

1. Lista `_posts/` para ver las fechas ocupadas y el orden actual.
2. Decide la posición:
   - Por defecto, **al final** del deck: usa la fecha más alta existente + 1 día
     (nunca una fecha futura; si ya llegaste a hoy, avísalo y pregunta).
   - Si el usuario pidió una posición concreta, elige una fecha **intermedia**
     entre las dos diapositivas vecinas.
3. Crea `_posts/AAAA-MM-DD-slug.md` con:
   ```yaml
   ---
   layout: slide
   title: "..."
   ---
   ```
   Contenido en Markdown, máximo ~40 palabras, una sola idea.
4. Compila: `bundle exec jekyll build`.
5. Confirma que la diapositiva salió: busca su título en `_site/index.html`.
6. Genera su imagen con `script/screenshots` y muéstrasela al usuario.
7. Responde en español: en qué posición quedó y el orden completo del deck.
