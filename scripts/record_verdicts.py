#!/usr/bin/env python3
"""Registra veredictos de unicidad del cloze sin reescribir el archivo entero.

El JUICIO no lo hace este script. Lo hace el modelo: lee `data/cloze_pending.json`,
que trae la oración y la lista de hermanos, y decide si algún hermano también encaja.
Este script solo hace la contabilidad — buscar el hash, insertar el registro, podar
los veredictos que ya no apunta ninguna oración.

Se identifica por PALABRA, no por hash, porque dentro de un lote cada palabra aparece
una sola vez en la lista de pendientes. Si una palabra apareciera dos veces, aborta.

Uso:
    python3 scripts/record_verdicts.py \
        --unique "congenial:cordial" \
        --unique "convivial:congenial" \
        --ambiguous "urbane:congenial,cordial"

    python3 scripts/record_verdicts.py --prune      # solo poda huérfanos
    python3 scripts/record_verdicts.py --list       # muestra los pendientes

Formato de --unique:     palabra:hermano_mas_cercano[:nota]
Formato de --ambiguous:  palabra:hermano1,hermano2[:nota]   (hace fallar el build)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "data"
PENDING_PATH = DATA / "cloze_pending.json"
VERDICTS_PATH = DATA / "cloze_verdicts.json"


def load_pending() -> dict[str, dict[str, Any]]:
    """Indexa los pendientes por palabra, abortando si hay palabras repetidas."""
    pending = json.loads(PENDING_PATH.read_text(encoding="utf-8"))
    index: dict[str, dict[str, Any]] = {}
    for item in pending:
        word = item["w"]
        if word in index:
            raise SystemExit(
                f"ERROR: '{word}' aparece dos veces en los pendientes; "
                "no se puede identificar por palabra. Resuelve a mano."
            )
        index[word] = item
    return index


def live_hashes() -> set[str]:
    """Todos los hashes que alguna oración vigente usa ahora mismo."""
    data = json.loads((DATA / "data.json").read_text(encoding="utf-8"))
    return {word["ejHash"] for group in data["groups"] for word in group["words"]}


def parse_spec(spec: str, ambiguous: bool) -> tuple[str, list[str], str]:
    """Descompone 'palabra:vecinos[:nota]' en sus tres partes.

    Returns
    -------
    word : str
    neighbours : list of str
    note : str
    """
    parts = spec.split(":", 2)
    word = parts[0].strip()
    raw = parts[1].strip() if len(parts) > 1 else ""
    note = parts[2].strip() if len(parts) > 2 else ""
    neighbours = [n.strip() for n in raw.split(",") if n.strip()]
    if ambiguous and not neighbours:
        raise SystemExit(f"ERROR: '{word}' marcada ambigua sin decir qué hermanos encajan.")
    return word, neighbours, note


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--unique", action="append", default=[], metavar="SPEC")
    parser.add_argument("--ambiguous", action="append", default=[], metavar="SPEC")
    parser.add_argument("--basis", default="semantic", choices=["semantic", "grammatical"])
    parser.add_argument("--prune", action="store_true", help="poda veredictos huérfanos")
    parser.add_argument("--list", action="store_true", help="muestra los pendientes y sale")
    args = parser.parse_args()

    pending = load_pending()

    if args.list:
        for word, item in pending.items():
            print(f"{word:<16} [{item['groupId']}]  hermanos: {', '.join(item['siblings'])}")
            print(f"    {item['ej']}")
        print(f"\n{len(pending)} pendientes")
        return 0

    verdicts = json.loads(VERDICTS_PATH.read_text(encoding="utf-8"))
    written = 0

    for spec in args.unique:
        word, neighbours, note = parse_spec(spec, ambiguous=False)
        if word not in pending:
            raise SystemExit(f"ERROR: '{word}' no está entre los pendientes.")
        item = pending[word]
        for neighbour in neighbours:
            if neighbour not in item["siblings"]:
                raise SystemExit(
                    f"ERROR: '{neighbour}' no es hermano de '{word}' en {item['groupId']}."
                )
        verdicts[item["hash"]] = {
            "w": word,
            "verdict": "unique",
            "alsoFits": [],
            "basis": args.basis,
            "nearMiss": neighbours[0] if neighbours else None,
            "note": note,
        }
        written += 1

    for spec in args.ambiguous:
        word, neighbours, note = parse_spec(spec, ambiguous=True)
        if word not in pending:
            raise SystemExit(f"ERROR: '{word}' no está entre los pendientes.")
        item = pending[word]
        verdicts[item["hash"]] = {
            "w": word,
            "verdict": "ambiguous",
            "alsoFits": neighbours,
            "basis": args.basis,
            "nearMiss": neighbours[0],
            "note": note,
        }
        written += 1

    removed = 0
    if args.prune:
        alive = live_hashes()
        for key in [k for k in verdicts if not k.startswith("_") and k not in alive]:
            del verdicts[key]
            removed += 1

    VERDICTS_PATH.write_text(
        json.dumps(verdicts, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    still = [w for w in pending if pending[w]["hash"] not in verdicts]
    print(f"escritos: {written}   podados: {removed}   sin juzgar: {len(still)}")
    if still:
        print(f"  faltan: {', '.join(still)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
