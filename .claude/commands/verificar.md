---
description: Comprueba que todo está bien antes de publicar (build, enlaces, orden)
allowed-tools: Read, Glob, Grep, Bash, Task
---

Verifica el estado completo del repositorio y responde en español, sin jerga.

Ejecuta, en este orden:

1. **Entorno**
   ```sh
   ruby -v && bundle -v && bundle exec jekyll -v
   ```

2. **Build y validación de enlaces**
   ```sh
   script/cibuild
   ```

3. **Inventario de diapositivas**
   ```sh
   ls _posts/
   grep -c '<section' _site/index.html
   ```
   Comprueba que el número de `<section>` publicadas coincide con el número de
   archivos en `_posts/`. Si no coincide, alguna diapositiva no se está
   publicando: casi siempre es una **fecha futura** (`future: false`) o falta
   `layout: slide`.

4. **Fechas**: ninguna futura, ninguna duplicada.

5. **Git**: `git status` y `git log --oneline -3`. Di si hay cambios sin
   guardar y en qué rama estás.

Si algo falla, lanza el agente `build-doctor` para que lo arregle y vuelve a
verificar.

## Formato de la respuesta

```
✅ / ❌  Entorno
✅ / ❌  El sitio compila
✅ / ❌  Enlaces e imágenes correctos
✅ / ❌  Todas las diapositivas se publican (N de N)
✅ / ❌  Fechas correctas

Diapositivas, en orden:
1. ...

Estado de git: rama X, N cambios sin guardar
```

Si algo está en ❌, explica en una frase qué pasa y qué hay que hacer.
