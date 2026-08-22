#!/usr/bin/env python3
"""Extrae y normaliza la lista de palabras del CSV de Vocab Mountain.

El CSV no es tabular: es una rejilla de hoja de cálculo con 4 bandas
horizontales. Cada banda tiene un encabezado (`Group N`), una fila de
enlaces (`Take Test N`) y luego las palabras, con las columnas de grupo
en los índices pares y columnas vacías en los impares.

La salida, `data/words.json`, es la ÚNICA verdad para el chequeo de
cobertura. `validate.py` compara contra ella, nunca contra el CSV.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = REPO_ROOT / "Greg Mat Vocab List (37 Groups, 1,110 Words) - Word List.csv"
DEFAULT_OUTPUT = REPO_ROOT / "data" / "words.json"

#: Filas donde arranca cada banda de 10 grupos (índice 0 = primera fila del CSV).
BAND_HEADER_ROWS = (1, 34, 67, 100)

#: Las columnas de grupo viven en los índices pares; las impares son separadores vacíos.
GROUP_COL_STRIDE = 2

#: Número esperado de palabras únicas tras normalizar. Falla el build si no cuadra.
EXPECTED_UNIQUE = 1112

#: Correcciones ortográficas de la fuente. Explícitas y registradas a propósito:
#: no queremos arreglos silenciosos sobre el material de estudio.
SPELLING_FIXES = {
    "all-ecompassing": "all-encompassing",
}


def normalize(raw: str) -> str:
    """Normaliza una celda del CSV a la forma canónica de la palabra.

    Parameters
    ----------
    raw : str
        Contenido crudo de la celda, posiblemente con espacios sobrantes.

    Returns
    -------
    str
        Palabra en minúsculas, sin espacios en los bordes y con los espacios
        internos colapsados a uno solo (`ad hoc`, `stem from` los conservan).
    """
    return re.sub(r"\s+", " ", raw.strip().lower())


def parse_grid(source: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Recorre la rejilla del CSV y devuelve las celdas con palabra.

    Parameters
    ----------
    source : Path
        Ruta al CSV original de Vocab Mountain.

    Returns
    -------
    cells : list of dict
        Una entrada por celda con palabra, con claves ``w``, ``gmGroup`` y ``gmRow``.
    stats : dict
        Contadores del recorrido para el reporte: celdas leídas, arreglos aplicados
        y celdas que traían espacios sobrantes.
    """
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))

    cells: list[dict[str, Any]] = []
    stats: dict[str, Any] = {"raw_cells": 0, "whitespace_trimmed": [], "spelling_fixed": []}

    for band_index, header_row in enumerate(BAND_HEADER_ROWS):
        header = rows[header_row]
        is_last_band = band_index + 1 == len(BAND_HEADER_ROWS)
        band_end = len(rows) if is_last_band else BAND_HEADER_ROWS[band_index + 1]
        # +2 salta el encabezado `Group N` y la fila de enlaces `Take Test N`.
        body = rows[header_row + 2 : band_end]

        for col in range(0, len(header), GROUP_COL_STRIDE):
            group_name = header[col].strip()
            if not group_name:
                continue

            for row_index, row in enumerate(body):
                if col >= len(row):
                    continue
                raw = row[col]
                if not raw.strip():
                    continue
                if raw.strip().lower().startswith("take test"):
                    continue

                stats["raw_cells"] += 1
                word = normalize(raw)
                if raw != raw.strip():
                    stats["whitespace_trimmed"].append(word)
                if word in SPELLING_FIXES:
                    stats["spelling_fixed"].append(f"{word} -> {SPELLING_FIXES[word]}")
                    word = SPELLING_FIXES[word]

                cells.append({"w": word, "gmGroup": group_name, "gmRow": row_index})

    return cells, stats


def deduplicate(cells: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Conserva la primera aparición de cada palabra y registra las repetidas.

    Parameters
    ----------
    cells : list of dict
        Celdas en orden de recorrido de la rejilla.

    Returns
    -------
    unique : list of dict
        Una entrada por palabra, en el orden en que apareció por primera vez.
    duplicates : list of dict
        Registro de las apariciones descartadas, con el grupo original y el que la conserva.
    """
    seen: dict[str, dict[str, Any]] = {}
    unique: list[dict[str, Any]] = []
    duplicates: list[dict[str, str]] = []

    for cell in cells:
        word = cell["w"]
        if word in seen:
            duplicates.append(
                {"w": word, "droppedFrom": cell["gmGroup"], "keptIn": seen[word]["gmGroup"]}
            )
            continue
        seen[word] = cell
        unique.append(cell)

    return unique, duplicates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE, help="CSV original")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="destino JSON")
    args = parser.parse_args()

    if not args.source.exists():
        print(f"ERROR: no encuentro la fuente: {args.source}", file=sys.stderr)
        return 1

    cells, stats = parse_grid(args.source)
    words, duplicates = deduplicate(cells)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(words, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    groups = sorted({c["gmGroup"] for c in cells}, key=lambda g: int(g.split()[-1]))
    print(f"fuente        : {args.source.name}")
    print(f"celdas leídas : {stats['raw_cells']}")
    print(f"columnas grupo: {len(groups)} ({groups[0]}..{groups[-1]})")
    print(f"espacios      : {len(stats['whitespace_trimmed'])} celdas recortadas")
    for fix in stats["spelling_fixed"]:
        print(f"fixed         : {fix}")
    for dup in duplicates:
        print(f"dedup         : {dup['w']} (descartada de {dup['droppedFrom']}, se queda en {dup['keptIn']})")
    print(f"escrito       : {args.output.relative_to(REPO_ROOT)}")
    print(f"{len(words)} unique words")

    if len(words) != EXPECTED_UNIQUE:
        print(
            f"ERROR: esperaba {EXPECTED_UNIQUE} palabras únicas, obtuve {len(words)}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
