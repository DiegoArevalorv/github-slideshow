---
name: presentaciones
description: Reglas completas para crear, editar, ordenar y publicar diapositivas en este repositorio (Jekyll + reveal.js). Úsala siempre que la tarea implique tocar archivos de _posts/, cambiar el tema o los estilos de la presentación, ajustar transiciones o fondos de reveal.js, cambiar el orden de las diapositivas, o publicar el deck en GitHub Pages.
---

# Autoría de diapositivas en `github-slideshow`

## Cómo se convierte un archivo en diapositiva

`index.html` recorre `site.posts reversed` e incluye `_includes/slide.html` por
cada post. Es decir: **cada archivo de `_posts/` es exactamente una diapositiva**,
y el orden lo determina la fecha del nombre del archivo, de la más antigua a la
más reciente.

```
_posts/0000-01-01-intro.md   → diapositiva 1
_posts/0001-01-01-que-es.md  → diapositiva 2
_posts/0001-01-02-como.md    → diapositiva 3
```

## Plantilla mínima

```markdown
---
layout: slide
title: "Título visible"
---

Contenido en Markdown.
```

## Las cuatro trampas de este repositorio

1. **Fechas futuras = diapositiva invisible.** `_config.yml` tiene
   `future: false`. Una diapositiva fechada mañana simplemente no se publica, y
   el build **no da error**. Es el fallo más frecuente y el más difícil de
   detectar. Usa siempre la fecha de hoy o anterior.

2. **Fechas duplicadas = orden impredecible.** Dos archivos con el mismo
   `AAAA-MM-DD` quedan en un orden que Jekyll no garantiza. Cada diapositiva
   necesita su propia fecha.

3. **Formato del nombre.** Sin el patrón `AAAA-MM-DD-slug.md`, Jekyll ni
   siquiera considera el archivo un post: desaparece sin avisar.

4. **`baseurl` está comentado a propósito** en `_config.yml` (commit `f3d6e95`).
   Si lo reactivas, los CSS y JS de reveal.js dejan de cargar en GitHub Pages.

## Estrategia de fechas recomendada

Para un deck nuevo, usa una base antigua y días consecutivos. Deja siempre
`0000-01-01` para la portada si quieres que vaya primera:

```
0000-01-01-portada.md
0001-01-01-contexto.md
0001-01-02-problema.md
0001-01-03-solucion.md
0001-01-04-datos.md
0001-01-05-cierre.md
```

Para **insertar** entre `0001-01-02` y `0001-01-03`, no hay hueco de días: usa
horas en el front matter con la clave `date`, que gana a la del nombre:

```yaml
---
layout: slide
title: "Diapositiva intercalada"
date: 0001-01-02 12:00:00
---
```

O bien renumera el deck completo con saltos de 10 días para dejar hueco.

## Front matter soportado

Definido por `_includes/slide.html`:

| Clave | Efecto |
|---|---|
| `layout: slide` | **Obligatorio.** |
| `title: "..."` | Encabezado `<h1>`. Con `""` no se muestra encabezado. |
| `slide-id: mi-ancla` | Pone `id="mi-ancla"` en la `<section>`, para enlazar directo. |
| `classes: [a, b]` | Añade clases CSS a la `<section>`. Sin esta clave se usa `slide`. |
| `data: {clave: valor}` | Se convierte en atributos `data-clave="valor"` de reveal.js. |
| `date: ...` | Sobrescribe la fecha del nombre; sirve para ordenar con precisión. |

Ejemplos útiles de `data` en reveal.js 3.x:

```yaml
data:
  background: "#1a1a1a"          # color de fondo de esa diapositiva
  background-image: "/img/x.png" # imagen de fondo
  transition: fade               # transición solo para esta diapositiva
  background-transition: zoom
```

## Configuración global de la presentación

En `_config.yml`:

- `title`, `author`, `description`: metadatos del deck.
- `solarized.theme`: `dark` o `light` (clase del `<html>`).
- `reveal.*`: opciones de reveal.js (`transition`, `progress`, `center`,
  `width`, `height`, `controls`, `slideNumber`…).
- El **tema visual** de reveal.js está fijado en `_includes/head.html`
  (`css/theme/moon.css`). Los temas disponibles están en
  `node_modules/reveal.js/css/theme/`: `beige`, `black`, `blood`, `league`,
  `moon`, `night`, `serif`, `simple`, `sky`, `solarized`, `white`.

Para cambiar de tema, edita esa línea de `head.html` y verifica el resultado con
`script/screenshots` — no supongas cómo queda, míralo.

## Buenas prácticas de contenido

- Una idea por diapositiva. Si dudas, divide.
- ~40 palabras máximo de cuerpo; 6 viñetas máximo.
- Títulos que afirmen algo, no etiquetas ("Ventas +18% en Q3", no "Ventas").
- Toda imagen con `alt` descriptivo: sin él, `script/cibuild` falla.
- Los enlaces deben decir a dónde llevan; nada de "aquí".
- Bloques de código: solo el fragmento relevante, ~12 líneas máximo.
- Portada al principio, conclusión o llamada a la acción al final.

## Flujo de trabajo completo

```sh
export BUNDLE_PATH=vendor/bundle BUNDLER_VERSION=2.5.22 LANG=C.UTF-8 LC_ALL=C.UTF-8

# 1. Escribir o editar archivos en _posts/
# 2. Compilar y validar
script/cibuild

# 3. Comprobar que TODAS las diapositivas se publicaron
ls _posts/ | wc -l
grep -c '<section' _site/index.html   # debe coincidir

# 4. Ver el resultado
script/screenshots                    # PNG por diapositiva en .preview/
```

Si los dos números del paso 3 no coinciden, hay una diapositiva que no se
publica: revisa fechas futuras y `layout: slide`.

## Publicación

El sitio se publica con GitHub Pages desde `master`. El flujo correcto es:
rama de trabajo → commit → push → Pull Request → fusión a `master`. El comando
`/publicar` hace todo esto con las verificaciones previas.

## Qué no tocar

- `node_modules/` — reveal.js viene commiteado; se actualiza vía npm, no a mano.
- `_site/` — salida generada, está en `.gitignore`.
- `vendor/` y `.preview/` — locales, ignorados por git.
- `Gemfile.lock` — solo si el problema es la resolución de gemas, y explicándolo.
