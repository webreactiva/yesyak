#!/usr/bin/env bash
# Enlaza las skills de YesYak en otro proyecto (un symlink por skill).
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"

usage() {
  cat <<EOF
Uso: $(basename "$0") [opciones] [skill...]

Crea un enlace simbólico por cada skill de YesYak dentro del directorio de
skills de un proyecto. Sin nombres de skill, instala todas.

Opciones:
  -t, --target DIR   Proyecto destino (por defecto: directorio actual)
  -c, --claude       Instalar en DIR/.claude/skills (por defecto)
  -a, --agents       Instalar en DIR/.agents/skills
  -b, --both         Instalar en ambos
  -u, --uninstall    Quitar los enlaces (solo los que apuntan a este repo)
  -l, --list         Listar las skills disponibles y salir
  -h, --help         Mostrar esta ayuda

Notas:
  - Un enlace simbólico existente con el mismo nombre se reemplaza.
  - Si ya existe una carpeta o archivo real con ese nombre, se omite con aviso.
  - Las skills guardan ficheros de trabajo en .scratchpad/: añádelo a .gitignore.

Ejemplos:
  $(basename "$0") -t ~/code/mi-app                 # todas en .claude/skills
  $(basename "$0") -t ~/code/mi-app -a ask-yak bug-intake
  $(basename "$0") -t ~/code/mi-app -b -u           # desinstalar de ambos
EOF
}

target="$PWD"; dirs=(); uninstall=0; skills=()
while [ $# -gt 0 ]; do
  case "$1" in
    -t|--target) target="${2:?falta DIR para $1}"; shift ;;
    -c|--claude) dirs+=(.claude/skills) ;;
    -a|--agents) dirs+=(.agents/skills) ;;
    -b|--both) dirs+=(.claude/skills .agents/skills) ;;
    -u|--uninstall) uninstall=1 ;;
    -l|--list) ls "$SRC"; exit 0 ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Opción desconocida: $1" >&2; usage >&2; exit 1 ;;
    *) skills+=("$1") ;;
  esac
  shift
done

[ -d "$target" ] || { echo "No existe el destino: $target" >&2; exit 1; }
target="$(cd "$target" && pwd)"
[ ${#dirs[@]} -gt 0 ] || dirs=(.claude/skills)
[ ${#skills[@]} -gt 0 ] || skills=($(ls "$SRC"))

for s in "${skills[@]}"; do
  [ -f "$SRC/$s/SKILL.md" ] || { echo "Skill desconocida: $s (usa --list)" >&2; exit 1; }
done

for d in "${dirs[@]}"; do
  dest="$target/$d"
  [ $uninstall -eq 1 ] || mkdir -p "$dest"
  for s in "${skills[@]}"; do
    link="$dest/$s"
    if [ $uninstall -eq 1 ]; then
      if [ -L "$link" ] && [ "$(readlink "$link")" = "$SRC/$s" ]; then
        rm "$link" && echo "quitado  $d/$s"
      fi
    elif [ -e "$link" ] && [ ! -L "$link" ]; then
      echo "omitido  $d/$s (ya existe y no es un enlace)" >&2
    else
      ln -sfn "$SRC/$s" "$link" && echo "enlazado $d/$s"
    fi
  done
done
