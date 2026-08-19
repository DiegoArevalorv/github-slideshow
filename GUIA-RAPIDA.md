# Guía rápida — qué escribir para que Claude haga el trabajo

Esta guía es para ti, no para Claude. No necesitas saber programar: basta con
escribir una de estas frases.

---

## Los 6 comandos que resuelven casi todo

Escríbelos tal cual, empezando por la barra `/`.

### `/nueva-presentacion <tema>`
Crea una presentación completa desde cero.

> `/nueva-presentacion los resultados de ventas de Factured en el último trimestre`

Claude investiga si hace falta, escribe las diapositivas, las revisa y te
**muestra imágenes** de cómo quedaron. No publica nada todavía.

### `/nueva-slide <lo que quieres decir>`
Añade una diapositiva a la presentación que ya existe.

> `/nueva-slide una diapositiva de cierre invitando a agendar una reunión`

### `/vista-previa`
Te muestra una imagen de cada diapositiva, tal como se verán proyectadas.
Úsalo siempre antes de publicar.

### `/verificar`
Comprueba que todo está sano: que el sitio se genera, que no hay enlaces
rotos y que **todas** tus diapositivas se están publicando. Te responde con
una lista de ✅ y ❌.

### `/publicar`
Guarda los cambios y los sube a GitHub creando un Pull Request. Antes de
subir nada, verifica que todo funcione. Si algo está roto, se detiene y te
lo explica.

### `/traducir-deck <idioma>`
Traduce toda la presentación.

> `/traducir-deck inglés`

---

## Y si prefieres pedirlo con tus palabras

También funciona. Claude reconoce la intención y usa las herramientas correctas:

- "hazme una presentación de 8 diapositivas sobre X"
- "el sitio no funciona, arréglalo"
- "muéstrame cómo se ven las diapositivas"
- "cambia el tema de la presentación a algo más claro"
- "revisa la presentación antes de que la muestre mañana"
- "mueve la diapositiva de precios al final"

---

## Los especialistas que trabajan por dentro

No tienes que invocarlos: Claude los llama cuando toca. Pero si quieres pedir
uno directamente, nómbralo.

| Especialista | Para qué sirve |
|---|---|
| `slide-author` | Escribe y estructura las diapositivas |
| `deck-reviewer` | Revisa calidad, accesibilidad y ortografía antes de publicar |
| `build-doctor` | Arregla el sitio cuando algo se rompe |
| `investigador` | Busca datos con fuentes verificables para tus diapositivas |

> "usa el deck-reviewer para revisar la presentación"

---

## Las dos reglas que evitan el 90% de los problemas

1. **Nunca pongas una fecha futura en una diapositiva.** El sistema las oculta
   sin avisar. Claude ya lo vigila automáticamente, pero si algo "desaparece",
   esta es la causa.

2. **Ejecuta `/verificar` antes de `/publicar`.** Es la diferencia entre
   descubrir un error tú o descubrirlo tu audiencia.

---

## Qué pasa cuando publicas

`/publicar` **no** cambia el sitio público de inmediato. Crea un Pull Request:
una propuesta de cambio que tú revisas y apruebas. La presentación se actualiza
en la web solo cuando ese Pull Request se fusiona a la rama `master`.

Claude vigila el Pull Request y te avisa si algo falla en las comprobaciones
automáticas.

---

## Si algo se rompe

Escribe simplemente:

> "algo no funciona, revísalo y arréglalo"

Claude reproducirá el error, encontrará la causa y lo corregirá. Los fallos
típicos de este proyecto ya están documentados para él en `CLAUDE.md`, así que
no tiene que adivinar.
