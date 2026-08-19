#!/usr/bin/env python3
"""Valida una diapositiva justo después de que Claude la crea o edita.

Hook PostToolUse (Edit|Write). Solo revisa archivos dentro de `_posts/`.
Si encuentra un problema, sale con código 2 para que Claude lo corrija
inmediatamente en lugar de descubrirlo en el build.

Comprueba:
  1. Nombre de archivo con el formato AAAA-MM-DD-slug.md que Jekyll exige.
  2. Fecha no futura (`future: false` en _config.yml haría desaparecer la slide).
  3. Front matter presente y con `layout: slide`.
  4. Que exista un `title` (aunque sea vacío a propósito).
  5. Que no haya fechas duplicadas que hagan el orden impredecible.
"""

import datetime
import json
import os
import re
import sys

NAME_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-[^/]+\.(md|markdown|html)$")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or ""
    if not path:
        return 0

    project = payload.get("cwd") or os.getcwd()
    posts_dir = os.path.join(project, "_posts")
    if os.path.dirname(os.path.abspath(path)) != os.path.abspath(posts_dir):
        return 0
    if not os.path.exists(path):
        return 0

    name = os.path.basename(path)
    problems = []

    match = NAME_RE.match(name)
    if not match:
        problems.append(
            f"El nombre '{name}' no sirve: Jekyll exige AAAA-MM-DD-slug.md "
            "(por ejemplo 2026-07-30-mi-diapositiva.md). Sin ese formato la "
            "diapositiva no se publica."
        )
    else:
        year, month, day = (int(g) for g in match.groups()[:3])
        # Jekyll acepta años como 0000 (la portada usa 0000-01-01), que
        # datetime.date no admite. Validamos el calendario solo cuando el año
        # está en el rango que datetime soporta.
        valid_date = True
        if year >= datetime.MINYEAR:
            try:
                datetime.date(year, month, day)
            except ValueError:
                valid_date = False
        else:
            valid_date = 1 <= month <= 12 and 1 <= day <= 31

        if not valid_date:
            problems.append(
                f"La fecha del nombre '{name}' no existe en el calendario."
            )
        else:
            today = datetime.date.today()
            if (year, month, day) > (today.year, today.month, today.day):
                problems.append(
                    f"La fecha {year:04d}-{month:02d}-{day:02d} está en el "
                    "futuro y _config.yml tiene `future: false`, así que esta "
                    "diapositiva NO aparecerá en la presentación. Usa la fecha "
                    "de hoy o anterior."
                )

    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        content = handle.read()

    if not content.startswith("---"):
        problems.append(
            "Falta el front matter. El archivo debe empezar con una línea '---', "
            "luego 'layout: slide' y 'title: \"...\"', y cerrar con otra '---'."
        )
    else:
        parts = content.split("---", 2)
        front = parts[1] if len(parts) > 2 else ""
        if not re.search(r"^\s*layout:\s*slide\s*$", front, re.MULTILINE):
            problems.append(
                "El front matter no declara 'layout: slide'. Sin ese layout la "
                "diapositiva se renderiza mal."
            )
        if not re.search(r"^\s*title:", front, re.MULTILINE):
            problems.append(
                "El front matter no tiene 'title:'. Usa title: \"\" si quieres "
                "una diapositiva sin encabezado."
            )

    # Fechas duplicadas: el orden de site.posts se vuelve arbitrario.
    if match:
        prefix = name[:10]
        siblings = [
            other
            for other in os.listdir(posts_dir)
            if other != name and other.startswith(prefix)
        ]
        if siblings:
            problems.append(
                f"Ya existe otra diapositiva con la fecha {prefix} "
                f"({', '.join(siblings)}). Dos diapositivas con la misma fecha "
                "tienen un orden impredecible: cámbiale la fecha a una libre."
            )

    if problems:
        print(f"Problemas en {name}:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print(
            "Corrígelos ahora. Detalles en .claude/skills/presentaciones/SKILL.md",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
