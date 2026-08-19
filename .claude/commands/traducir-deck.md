---
description: Traduce todas las diapositivas a otro idioma
argument-hint: <idioma destino, p. ej. inglés>
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

Traduce la presentación completa a: **$ARGUMENTS**

Si no se indicó el idioma, pregúntalo.

1. Lee **todas** las diapositivas de `_posts/` en orden de presentación.
2. Confirma con el usuario si quiere:
   - **(a)** reemplazar el contenido actual por la traducción, o
   - **(b)** conservar el original y añadir la versión traducida al final.

   No asumas: la opción (a) borra contenido. Espera la respuesta.
3. Traduce título y cuerpo de cada diapositiva. Reglas:
   - **No traduzcas** código, nombres de comandos, rutas de archivos, nombres
     propios ni URLs.
   - Adapta el registro y las expresiones idiomáticas; no traduzcas literal.
   - Mantén intacta la estructura Markdown (viñetas, niveles de encabezado,
     bloques de código) y **todo** el front matter salvo `title`.
   - Conserva los `alt` de las imágenes, traducidos.
   - Respeta el límite de ~40 palabras por diapositiva: si la traducción crece
     mucho, acórtala en vez de dejarla ilegible.
4. Compila: `script/cibuild`.
5. Genera la vista previa con `script/screenshots` y muéstrasela al usuario.
6. Resume en español: qué diapositivas se tradujeron y el orden final.
