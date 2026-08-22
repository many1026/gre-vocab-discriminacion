#!/usr/bin/env python3
"""Ensambla los grupos semánticos sueltos en el dataset que consume la app.

Lee `data/groups/*.json` (un archivo por grupo, editable a mano), los une con
`data/words.json` para inyectar la procedencia `gmGroup`, y emite:

- `data/data.json` : dataset canónico, editable a mano
- `data/data.js`   : el mismo JSON asignado a `window.VOCAB`

Existen los dos porque `fetch()` sobre `file://` está bloqueado por CORS en
Chrome y Safari: un `index.html` que hiciera fetch no abriría desde el sistema
de archivos, que es un requisito del proyecto. Un `<script>` sí carga, así que
la app consume `data.js`. Todo lo que va después del `=` es JSON puro, de modo
que sigue siendo editable sin tocar código.

También emite `data/cloze_pending.json` con las oraciones que aún no tienen
veredicto de unicidad, para que sirvan de lista de trabajo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
GROUPS_DIR = DATA_DIR / "groups"

JS_PREFIX = "window.VOCAB = "
JS_SUFFIX = ";\n"


def ej_hash(sentence: str, siblings: list[str]) -> str:
    """Devuelve el sha256 truncado que identifica a un ítem cloze.

    Parameters
    ----------
    sentence : str
        Texto del campo ``ej``.
    siblings : list of str
        Las demás palabras del grupo, que son los distractores del ítem.

    Returns
    -------
    str
        Primeros 16 hex del sha256 de la oración *y* del conjunto de hermanos.

    Notes
    -----
    Los hermanos entran en el hash a propósito. La unicidad de un cloze no
    depende solo de la oración: depende de contra qué distractores compite. Si
    una palabra cambia de grupo, la misma oración puede dejar de ser
    discriminante, así que el veredicto tiene que caducar. Hashear solo la
    oración dejaba pasar exactamente ese caso.
    """
    payload = sentence + " " + " ".join(sorted(siblings))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Une grupos, procedencia y trampas ortográficas en un solo dataset.

    Returns
    -------
    dataset : dict
        Estructura final con ``groups``, ``formConfusions`` y ``meta``.
    pending : list of dict
        Oraciones cloze sin veredicto de unicidad registrado.
    """
    words = load_json(DATA_DIR / "words.json")
    provenance = {entry["w"]: entry["gmGroup"] for entry in words}

    confusions_path = DATA_DIR / "form_confusions.json"
    confusions = load_json(confusions_path) if confusions_path.exists() else []

    verdicts_path = DATA_DIR / "cloze_verdicts.json"
    verdicts = load_json(verdicts_path) if verdicts_path.exists() else {}

    groups: list[dict[str, Any]] = []
    pending: list[dict[str, Any]] = []

    for path in sorted(GROUPS_DIR.glob("*.json")):
        group = load_json(path)
        siblings = [w["w"] for w in group["words"]]

        for word in group["words"]:
            word["gmGroup"] = provenance.get(word["w"])
            word["groupId"] = group["id"]

            others = [s for s in siblings if s != word["w"]]
            digest = ej_hash(word["ej"], others)
            word["ejHash"] = digest
            if digest not in verdicts:
                pending.append(
                    {
                        "hash": digest,
                        "w": word["w"],
                        "groupId": group["id"],
                        "ej": word["ej"],
                        "siblings": others,
                    }
                )

        groups.append(group)

    covered = {w["w"] for g in groups for w in g["words"]}
    dataset = {
        "meta": {
            "totalWords": len(words),
            "coveredWords": len(covered),
            "groupCount": len(groups),
        },
        "groups": groups,
        "formConfusions": confusions,
    }
    return dataset, pending


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="suprime el resumen")
    args = parser.parse_args()

    if not GROUPS_DIR.exists():
        print(f"ERROR: no existe {GROUPS_DIR}", file=sys.stderr)
        return 1

    dataset, pending = build()
    payload = json.dumps(dataset, ensure_ascii=False, indent=1)

    (DATA_DIR / "data.json").write_text(payload + "\n", encoding="utf-8")
    (DATA_DIR / "data.js").write_text(JS_PREFIX + payload + JS_SUFFIX, encoding="utf-8")
    (DATA_DIR / "cloze_pending.json").write_text(
        json.dumps(pending, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    if not args.quiet:
        meta = dataset["meta"]
        pct = 100 * meta["coveredWords"] / meta["totalWords"]
        print(f"grupos          : {meta['groupCount']}")
        print(f"cobertura       : {meta['coveredWords']}/{meta['totalWords']} ({pct:.1f}%)")
        print(f"trampas de forma: {len(dataset['formConfusions'])}")
        print(f"cloze pendientes: {len(pending)}")
        print("escrito         : data/data.json, data/data.js, data/cloze_pending.json")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
