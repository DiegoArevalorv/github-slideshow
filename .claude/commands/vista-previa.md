---
description: Muestra cómo se ven las diapositivas (imágenes de cada una)
allowed-tools: Read, Glob, Bash, SendUserFile
---

Genera y muestra la vista previa visual de la presentación.

1. Ejecuta `script/screenshots`. Genera un PNG por diapositiva en `.preview/`.
2. Si el build falla, lanza el agente `build-doctor`, arregla el problema y
   vuelve a intentarlo.
3. Muestra **todas** las imágenes al usuario con `SendUserFile`
   (`display: "render"`), en orden de presentación.
4. Acompáñalas de la lista numerada de títulos en español.
5. Señala cualquier problema visual que veas en las capturas: texto que se sale
   de la pantalla, título cortado, contraste insuficiente, diapositiva vacía o
   demasiado cargada.

Si el usuario quiere el servidor interactivo en vez de imágenes, indícale:

```sh
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

y avísale de que en este entorno remoto el puerto puede no ser accesible desde
su navegador; las imágenes son la vía fiable.
