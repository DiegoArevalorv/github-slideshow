# CLAUDE.md — Memoria del proyecto

Contexto permanente para Claude Code en este repositorio. Lee esto antes de tocar
cualquier archivo.

## Qué es este proyecto

`github-slideshow` es una **presentación de diapositivas** publicada con GitHub
Pages. No es una app: es un sitio estático generado por **Jekyll** que renderiza
las diapositivas con **reveal.js 3.9.2**.

- Cada diapositiva es un archivo Markdown en `_posts/`.
- `index.html` recorre `site.posts` en orden inverso y arma la presentación.
- El resultado se publica en GitHub Pages desde la rama por defecto (`master`).

El dueño del repositorio **no es programador**. Prioriza siempre:

1. Que el sitio compile sin errores antes de terminar.
2. Explicaciones en español, cortas y sin jerga.
3. Nunca dejar la rama en un estado roto.

## Idioma

Responde **en español**. Los nombres de archivos, comandos y código quedan en su
idioma original.

## Estructura real del repositorio

```
_posts/            # UNA diapositiva por archivo Markdown  ← aquí va el contenido
_layouts/
  presentation.html  # envoltura de la presentación completa
  slide.html         # una diapositiva servida sola
  print.html         # versión imprimible
_includes/
  head.html          # <head>: CSS de reveal.js y tema (moon)
  slide.html         # plantilla de cada <section class="step">
  script.html        # Reveal.initialize() y plugins
index.html         # arma la presentación iterando los posts
_config.yml         # título, autor, tema, opciones de reveal.js
script/cibuild     # build + validación de enlaces (html-proofer)
script/server      # servidor local de desarrollo
node_modules/reveal.js  # reveal.js commiteado vía package-lock.json
```

## Cómo se escribe una diapositiva

Archivo: `_posts/AAAA-MM-DD-titulo-en-slug.md`

```markdown
---
layout: slide
title: "Título visible de la diapositiva"
---

Contenido en Markdown. Una idea por diapositiva.
```

Reglas que **no** son obvias y hay que respetar:

- **El orden lo define la fecha del nombre del archivo.** `index.html` usa
  `site.posts reversed`, así que la diapositiva con la fecha **más antigua**
  aparece primero. La portada actual es `0000-01-01-intro.md`.
- **`_config.yml` tiene `future: false`.** Una diapositiva con fecha futura
  **no se publica**. Nunca uses fechas posteriores a hoy.
- Para insertar una diapositiva entre dos existentes, usa una fecha intermedia
  (las fechas son solo para ordenar, no se muestran).
- `layout: slide` es obligatorio en el front matter.
- `title: ""` (vacío) oculta el encabezado `<h1>`.

### Front matter opcional que sí soporta `_includes/slide.html`

```yaml
slide-id: mi-ancla        # id HTML de la sección, para enlazar directo
classes: [dark, centrado] # clases CSS extra en la <section>
data:                     # se convierte en atributos data-* de reveal.js
  background: "#1c1c1c"
  transition: fade
```

## Comandos

Ejecuta siempre desde la raíz del repositorio.

| Objetivo | Comando |
|---|---|
| Instalar dependencias Ruby | `.claude/hooks/session-start.sh` |
| Compilar el sitio | `bundle exec jekyll build` |
| Compilar + validar enlaces | `script/cibuild` |
| **Ver las diapositivas (PNG por diapositiva)** | `script/screenshots` |
| Servidor local | `bundle exec jekyll serve --host 0.0.0.0 --port 4000` |
| Verificación completa | `/verificar` (slash command del repo) |

Variables de entorno necesarias (ya fijadas en `.claude/settings.json`):

```sh
export BUNDLE_PATH=vendor/bundle BUNDLER_VERSION=2.5.22 LANG=C.UTF-8 LC_ALL=C.UTF-8
```

### Decisiones de la cadena de build — no las revientes

- **Bundler:** el `Gemfile.lock` histórico fijaba `BUNDLED WITH 1.17.3`, que
  falla en Ruby ≥ 3.2 con `undefined method 'untaint'`. El lock se regeneró con
  Bundler 2.5.22 (`github-pages 232`, `jekyll 3.10.0`, `html-proofer 5.2.2`,
  `nokogiri 1.19.4` con binarios precompilados para Linux y macOS). Si vuelves a
  ver el error de `untaint`, se activó un Bundler 1.x.
- **Locale:** sin `LANG`/`LC_ALL` en UTF-8, html-proofer lanza
  `Encoding::InvalidByteSequenceError` con los acentos del deck y **se salta
  archivos en silencio** en lugar de fallar. Nunca quites esas variables.
- **html-proofer ignora `node_modules/`:** los HTML de ejemplo que trae
  reveal.js tienen enlaces roots propios y rotos. Es código de terceros que no
  vamos a arreglar; validamos nuestras páginas. No amplíes ese `--ignore-files`
  a nuestros archivos.
- **Verificación clave:** el número de archivos en `_posts/` debe coincidir con
  el número de `<section>` en `_site/index.html`. Si no coincide, hay una
  diapositiva que no se publica (casi siempre por fecha futura).

Las gemas se instalan en `vendor/bundle` (ignorado por git).

## Automatismos activos

- **`SessionStart`** → `.claude/hooks/session-start.sh`: prepara Ruby, Bundler y
  las gemas al abrir la sesión. Es idempotente y nunca aborta la sesión.
- **`PostToolUse` (Edit|Write)** → `.claude/hooks/check-slide.py`: cada vez que
  creas o editas un archivo de `_posts/`, valida nombre, fecha (no futura, no
  duplicada) y front matter. Si algo está mal, te lo devuelve para corregirlo en
  el momento.
- **GitHub Actions** (`.github/workflows/ci.yml`): compila, valida enlaces,
  comprueba que todas las diapositivas se publiquen, revisa las fechas y sube
  las imágenes de las diapositivas como artefacto del run.

## Convenciones de trabajo

- **Rama:** desarrolla en la rama que te indique la tarea; nunca hagas push a
  `master` directamente.
- **Commits:** mensajes en español, imperativo, una línea de resumen.
- **Antes de terminar cualquier cambio de contenido o plantilla:** corre
  `bundle exec jekyll build` y confirma que termina sin error.
- **No** edites `node_modules/`, `Gemfile.lock` ni `_site/`.
- **No** reintroduzcas `baseurl` en `_config.yml`: se comentó a propósito
  (commit `f3d6e95`) para que el sitio funcione en la raíz del dominio.
- `_site/` es salida generada y está en `.gitignore`. Nunca la commitees.

## Herramientas propias de este repositorio

Están en `.claude/` y se cargan automáticamente:

- **Comandos** (`.claude/commands/`): `/nueva-presentacion`, `/nueva-slide`,
  `/verificar`, `/vista-previa`, `/publicar`, `/traducir-deck`.
- **Agentes** (`.claude/agents/`): `slide-author`, `deck-reviewer`,
  `build-doctor`, `investigador`.
- **Skill** (`.claude/skills/presentaciones/`): reglas completas de autoría de
  diapositivas en este repositorio.
- **Hook de arranque** (`.claude/hooks/session-start.sh`): deja el entorno listo
  al abrir la sesión.

Usa el agente `build-doctor` cuando el build falle, y `deck-reviewer` antes de
publicar una presentación nueva.
