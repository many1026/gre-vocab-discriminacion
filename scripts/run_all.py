#!/usr/bin/env python3
"""Corre el pipeline completo y deja un informe revisable.

Ejecuta, en orden: extract_words -> build_clusters -> validate. Captura la salida
de los tres, la guarda con fecha, y escribe además un `status.json` legible por
máquina para que la siguiente sesión sepa en un vistazo dónde se quedó todo.

Este script NO genera contenido. Los campos `disc`, `ej`, `twin` y `whyNotTwin`
son juicio lingüístico y los escribe el modelo turno a turno; aquí solo se
extrae, se ensambla, se valida y se informa.

Uso:
    python3 scripts/run_all.py              # corre todo y escribe el informe
    python3 scripts/run_all.py --strict     # exige cobertura total (sin --allow-partial)
    python3 scripts/run_all.py --quiet      # solo el resumen final

Códigos de salida:
    0  todo verde
    1  falló la validación (hay errores de contenido que arreglar)
    2  falló una etapa del pipeline (extract o build reventaron)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
DATA = REPO_ROOT / "data"
REPORTS = REPO_ROOT / "reports"

SEPARATOR = "=" * 72


def run_stage(name: str, argv: list[str]) -> tuple[int, str]:
    """Ejecuta una etapa del pipeline y devuelve su código y su salida combinada.

    Parameters
    ----------
    name : str
        Etiqueta de la etapa, para el informe.
    argv : list of str
        Comando completo a ejecutar.

    Returns
    -------
    code : int
        Código de salida del proceso.
    output : str
        stdout y stderr concatenados.
    """
    proc = subprocess.run(argv, capture_output=True, text=True, cwd=REPO_ROOT)
    output = proc.stdout + (("\n[stderr]\n" + proc.stderr) if proc.stderr.strip() else "")
    return proc.returncode, output


def parse_validation(output: str) -> dict[str, Any]:
    """Extrae del reporte de validate.py los datos que interesan a la próxima sesión.

    Parameters
    ----------
    output : str
        Salida completa de validate.py.

    Returns
    -------
    dict
        Errores duros, avisos blandos y las métricas de cabecera.
    """
    errors = [line.strip() for line in output.splitlines() if line.strip().startswith("[")]
    metrics: dict[str, Any] = {}

    for line in output.splitlines():
        stripped = line.strip()
        if stripped.startswith("Cobertura"):
            # "Cobertura        : 233/1112 (21.0%)"
            fraction = stripped.split(":", 1)[1].split("(")[0].strip()
            done, total = fraction.split("/")
            metrics["covered"] = int(done)
            metrics["total"] = int(total)
        elif stripped.startswith("Grupos           :"):
            metrics["groups"] = int(stripped.split(":", 1)[1].strip())
        elif stripped.startswith("Grupos loose"):
            metrics["looseGroups"] = int(stripped.split(":", 1)[1].strip().split()[0])

    return {"errors": errors, "metrics": metrics}


def remaining_words() -> list[str]:
    """Devuelve las palabras del Excel que todavía no están en ningún grupo."""
    universe = [entry["w"] for entry in json.loads((DATA / "words.json").read_text(encoding="utf-8"))]
    covered = {
        word["w"]
        for path in sorted((DATA / "groups").glob("*.json"))
        for word in json.loads(path.read_text(encoding="utf-8"))["words"]
    }
    return [w for w in universe if w not in covered]


def pending_fields() -> list[dict[str, Any]]:
    """Lee el mapa de campos planificados y devuelve los que siguen sin escribirse.

    Returns
    -------
    list of dict
        Cada campo pendiente con sus candidatos que todavía están libres. Lista
        vacía si aún no existe `data/field_map.json`.
    """
    path = DATA / "field_map.json"
    if not path.exists():
        return []

    plan = json.loads(path.read_text(encoding="utf-8")).get("fields", [])
    covered = {
        word["w"]
        for gp in sorted((DATA / "groups").glob("*.json"))
        for word in json.loads(gp.read_text(encoding="utf-8"))["words"]
    }

    pending = []
    for field in plan:
        free = [w for w in field.get("candidates", []) if w not in covered]
        if len(free) >= 5:
            pending.append({"name": field.get("name", "?"), "free": free})
    return pending


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="exige cobertura total")
    parser.add_argument("--quiet", action="store_true", help="solo el resumen")
    args = parser.parse_args()

    started = datetime.now()
    stages = [
        ("extract", [sys.executable, str(SCRIPTS / "extract_words.py")]),
        ("build", [sys.executable, str(SCRIPTS / "build_clusters.py")]),
        (
            "validate",
            [sys.executable, str(SCRIPTS / "validate.py")]
            + ([] if args.strict else ["--allow-partial"]),
        ),
    ]

    log: list[str] = [
        SEPARATOR,
        f"CORRIDA COMPLETA  {started:%Y-%m-%d %H:%M:%S}",
        f"modo: {'strict (exige cobertura total)' if args.strict else 'parcial (backfill en curso)'}",
        SEPARATOR,
    ]
    results: dict[str, int] = {}
    validation_output = ""

    for name, argv in stages:
        code, output = run_stage(name, argv)
        results[name] = code
        log += ["", f"--- etapa: {name}  (exit {code}) ---", output.rstrip()]
        if name == "validate":
            validation_output = output
        if name != "validate" and code != 0:
            log += ["", f"ABORTADO: la etapa '{name}' falló; no se ejecutan las siguientes."]
            break

    parsed = parse_validation(validation_output)
    left = remaining_words()
    fields = pending_fields()

    log += [
        "",
        SEPARATOR,
        "QUÉ QUEDA",
        SEPARATOR,
        f"palabras sin grupo: {len(left)}",
        f"primeras 40       : {', '.join(left[:40])}" if left else "primeras 40       : —",
    ]
    if fields:
        log += ["", f"campos planificados pendientes: {len(fields)}"]
        for field in fields[:15]:
            log.append(f"  - {field['name']}  ({len(field['free'])} libres)")
    else:
        log += ["", "no hay data/field_map.json: los campos se eligen a mano en cada lote."]

    REPORTS.mkdir(exist_ok=True)
    stamp = started.strftime("%Y%m%d_%H%M%S")
    full_log = "\n".join(log) + "\n"
    (REPORTS / f"run_{stamp}.txt").write_text(full_log, encoding="utf-8")
    (REPORTS / "latest.txt").write_text(full_log, encoding="utf-8")

    status = {
        "timestamp": started.isoformat(timespec="seconds"),
        "stages": results,
        "green": all(code == 0 for code in results.values()),
        "metrics": parsed["metrics"],
        "errorCount": len(parsed["errors"]),
        "errors": parsed["errors"],
        "remainingCount": len(left),
        "remaining": left,
        "pendingFields": [f["name"] for f in fields],
    }
    (REPORTS / "status.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    metrics = parsed["metrics"]
    print(SEPARATOR)
    print(f"RESUMEN  {started:%Y-%m-%d %H:%M}")
    print(SEPARATOR)
    for name, code in results.items():
        print(f"  {name:<10} {'ok' if code == 0 else f'FALLO (exit {code})'}")
    if metrics:
        pct = 100 * metrics.get("covered", 0) / max(metrics.get("total", 1), 1)
        print(f"\n  cobertura : {metrics.get('covered')}/{metrics.get('total')} ({pct:.1f}%)")
        print(f"  grupos    : {metrics.get('groups')}  (loose: {metrics.get('looseGroups')})")
    print(f"  sin grupo : {len(left)}")
    print(f"  errores   : {len(parsed['errors'])}")
    for error in parsed["errors"][:10]:
        print(f"     {error}")
    print(f"\n  informe   : reports/latest.txt  (+ reports/run_{stamp}.txt)")
    print(f"  estado    : reports/status.json")

    if any(code != 0 for name, code in results.items() if name != "validate"):
        return 2
    return 1 if results.get("validate", 1) != 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
