#!/usr/bin/env bash
# Prepara el entorno de este repositorio al iniciar una sesión de Claude Code.
#
# Qué hace:
#   1. Fija una versión de Bundler compatible con Ruby 3.x.
#   2. Instala las gemas en vendor/bundle si faltan.
#   3. Verifica que reveal.js esté presente.
#
# Es idempotente: si todo está listo, termina en menos de un segundo.
# Nunca falla la sesión: si algo no se puede instalar, avisa y sigue.

set -uo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/../.." || exit 0

# Bundler 1.17.3 (el que fija Gemfile.lock antiguo) rompe en Ruby >= 3.2 con
# "undefined method 'untaint'". Elegimos la versión instalada más adecuada.
pick_bundler() {
  local v
  for v in 2.5.22 2.6.9 2.5.23; do
    if gem list -i -v "$v" bundler >/dev/null 2>&1; then
      echo "$v"
      return 0
    fi
  done
  # Última opción: la más nueva que no sea la serie 1.x.
  gem list bundler 2>/dev/null \
    | sed -n 's/^bundler (\(.*\))$/\1/p' \
    | tr ',' '\n' \
    | sed 's/default: //' \
    | tr -d ' ' \
    | grep -v '^1\.' \
    | sort -V \
    | tail -1
}

BUNDLER_VERSION="$(pick_bundler)"
export BUNDLER_VERSION
export BUNDLE_PATH="vendor/bundle"

echo "== Preparando github-slideshow =="
echo "Ruby:    $(ruby -v 2>/dev/null | cut -d' ' -f2 || echo 'no encontrado')"
echo "Bundler: ${BUNDLER_VERSION:-no encontrado}"

if [ -z "${BUNDLER_VERSION}" ]; then
  echo "AVISO: no hay un Bundler compatible instalado. Ejecuta: gem install bundler -v 2.5.22"
  exit 0
fi

if bundle exec jekyll -v >/dev/null 2>&1; then
  echo "Gemas:   ya instaladas ($(bundle exec jekyll -v 2>/dev/null))"
else
  echo "Gemas:   instalando en vendor/bundle (puede tardar unos minutos)..."
  if bundle install --quiet >/tmp/bundle-install.log 2>&1; then
    echo "Gemas:   listas ($(bundle exec jekyll -v 2>/dev/null))"
  else
    echo "AVISO: 'bundle install' falló. Últimas líneas:"
    tail -15 /tmp/bundle-install.log 2>/dev/null | sed 's/^/  /'
    echo "AVISO: usa el agente 'build-doctor' para diagnosticarlo."
    exit 0
  fi
fi

if [ -d node_modules/reveal.js ]; then
  echo "reveal.js: presente"
else
  echo "AVISO: falta node_modules/reveal.js. Ejecuta: npm install"
fi

echo "== Listo. Compila con: bundle exec jekyll build =="
exit 0
