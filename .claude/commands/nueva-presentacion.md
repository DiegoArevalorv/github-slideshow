---
description: Crea una presentación completa desde cero sobre un tema
argument-hint: <tema de la presentación> [| en N diapositivas]
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

Crea una presentación completa sobre: **$ARGUMENTS**

Si no se indicó un tema, pregúntalo antes de hacer nada más.

Sigue este orden:

1. **Decide si hace falta investigar.** Si el tema requiere datos, cifras o
   hechos externos, lanza el agente `investigador` para obtener material con
   fuentes. Si el tema es interno o el usuario ya te dio el contenido, sáltate
   este paso.

2. **Revisa qué hay.** Lista `_posts/` para ver las diapositivas existentes y
   las fechas ya ocupadas. Pregunta al usuario si esta presentación
   **sustituye** el contenido actual o **se añade** al final. No borres nada sin
   confirmación explícita.

3. **Escribe las diapositivas** con el agente `slide-author`. Salvo que el
   usuario pida otra cosa: entre 6 y 9 diapositivas, una idea por diapositiva,
   en español, con portada y cierre.

4. **Revisa la calidad** con el agente `deck-reviewer`.

5. **Genera la vista previa visual**: `script/screenshots`. Muestra al usuario
   las imágenes de las diapositivas con SendUserFile.

6. **Resume en español** (sin jerga): cuántas diapositivas hay, el título de
   cada una en orden, y confirma que `script/cibuild` pasó.

No hagas commit ni push en este comando. Al final dile al usuario que puede
publicar con `/publicar`.
