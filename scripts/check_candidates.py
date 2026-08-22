#!/usr/bin/env python3
"""Comprueba qué palabras candidatas existen en la lista antes de escribir un grupo.

Se ejecuta ANTES de redactar contenido. El gate ya detecta las palabras inventadas
(regla R2), pero para entonces ya se escribió la entrada completa y hay que rehacer
los veredictos de todo el grupo, porque el hash incluye a los hermanos.

Uso:
    python3 scripts/check_candidates.py salubrious salutary benign portentous
    python3 scripts/check_candidates.py --field "solemne" august magisterial turgid
"""

from __future__ import annotations

import argparse
import json
from difflib import get_close_matches
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORDS_PATH = REPO_ROOT / "data" / "words.json"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", nargs="+", help="palabras a comprobar")
    parser.add_argument("--field", default="", help="etiqueta del campo semántico, solo para el título")
    args = parser.parse_args()

    universe = {entry["w"] for entry in json.loads(WORDS_PATH.read_text(encoding="utf-8"))}
    covered = {
        word["w"]
        for path in sorted((REPO_ROOT / "data" / "groups").glob("*.json"))
        for word in json.loads(path.read_text(encoding="utf-8"))["words"]
    }

    available, taken, missing = [], [], []
    for candidate in args.candidates:
        key = candidate.strip().lower()
        if key not in universe:
            missing.append(key)
        elif key in covered:
            taken.append(key)
        else:
            available.append(key)

    if args.field:
        print(f"campo: {args.field}")
    print(f"DISPONIBLES ({len(available)}): {', '.join(available) or '—'}")
    if taken:
        print(f"YA EN UN GRUPO ({len(taken)}): {', '.join(taken)}")
    if missing:
        print(f"NO EXISTEN ({len(missing)}):")
        for word in missing:
            near = get_close_matches(word, universe, n=3, cutoff=0.75)
            hint = f"  ¿quisiste decir {', '.join(near)}?" if near else ""
            print(f"   {word}{hint}")

    # Un grupo necesita al menos 5 miembros disponibles para generar todos los formatos.
    if len(available) < 5:
        print(f"\nAVISO: solo {len(available)} disponibles. El piso por grupo es 5.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
