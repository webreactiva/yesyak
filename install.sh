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
  - También escribe un bloque mínimo de YesYak en AGENTS.md, @AGENTS.md en CLAUDE.md
    (con -c o -b) y .scratchpad/ en .gitignore, si faltan. -u quita el bloque mínimo.

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

# Without the YesYak block in AGENTS.md, a strong model ignores the skills for small changes. Install writes a
# minimal block; customize-yak replaces it with the full one. Its lines must match the template of customize-yak
# (check_yesyak.py --dev compares them).
read -r -d '' MIN_BLOCK <<'EOF' || true
<!-- yesyak:start -->
## YesYak

- At the start of a session and after a compaction, run `python3` with the `scripts/check_yesyak.py` of the `ask-yak` skill, from the project root. If it exits with 0, apply each `active:` line it prints when you use that skill: `add` adds the instruction, `replace` uses the instruction in place of the named section, `off` skips the skill unless the user asks for it by name. If it fails or cannot run, tell the user and use the skills as written. When you brief a subagent, include the `active:` lines of the skills it uses.
- A feature request or a bug report starts `yak-pilot`, whatever the size. It plans the skills and the stops; ask the user before you leave out a step of its plan.
- YesYak is installed but not set up: before the first task, offer `customize-yak` to detect the checks and conventions of this project.
<!-- yesyak:end -->
EOF
NOT_SET_UP='YesYak is installed but not set up'

if [ $uninstall -eq 1 ]; then
  # Remove the block only while it is still the minimal one; a block that customize-yak wrote stays.
  if grep -qs "$NOT_SET_UP" "$target/AGENTS.md"; then
    awk '/<!-- yesyak:start -->/{skip=1} !skip{print} /<!-- yesyak:end -->/{skip=0}' "$target/AGENTS.md" > "$target/AGENTS.md.tmp"
    mv "$target/AGENTS.md.tmp" "$target/AGENTS.md"
    echo "quitado  bloque mínimo de YesYak en AGENTS.md"
  fi
  exit 0
fi

if ! grep -qs 'yesyak:start' "$target/AGENTS.md"; then
  { [ -s "$target/AGENTS.md" ] && echo; printf '%s\n' "$MIN_BLOCK"; } >> "$target/AGENTS.md"
  echo "escrito  bloque mínimo de YesYak en AGENTS.md (el agente ofrecerá customize-yak antes de la primera tarea)"
fi
# Claude Code reads CLAUDE.md, not AGENTS.md.
if [[ " ${dirs[*]} " == *" .claude/skills "* ]] && ! grep -qs '^@AGENTS.md' "$target/CLAUDE.md"; then
  { [ -s "$target/CLAUDE.md" ] && echo; echo "@AGENTS.md"; } >> "$target/CLAUDE.md"
  echo "escrito  @AGENTS.md en CLAUDE.md"
fi
if ! grep -qsE '^/?\.scratchpad/?$' "$target/.gitignore"; then
  { [ -s "$target/.gitignore" ] && [ -n "$(tail -c1 "$target/.gitignore")" ] && echo; echo ".scratchpad/"; } >> "$target/.gitignore"
  echo "escrito  .scratchpad/ en .gitignore"
fi
