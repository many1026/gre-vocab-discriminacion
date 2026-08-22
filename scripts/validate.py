#!/usr/bin/env python3
"""Gate de build para el dataset de vocabulario.

Sale con código distinto de cero si alguna regla dura se rompe. Las reglas
existen para impedir que entren al estudio entradas que enseñan el grupo en
lugar de la distinción — que es el problema entero que este proyecto ataca.

Uso:
    python3 scripts/validate.py                  # exige cobertura total
    python3 scripts/validate.py --allow-partial  # durante el backfill por lotes
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
GROUPS_DIR = DATA_DIR / "groups"

MIN_GROUP = 5
MAX_GROUP = 9
REQUIRED_FIELDS = ("w", "pos", "def", "disc", "tone", "axisPos", "ej", "twin", "whyNotTwin")
VALID_TONES = {"neg", "neu", "pos"}
BLANK = "___"

#: Por debajo de esta distancia en el eje, dos palabras del mismo tono necesitan
#: un `whyNotTwin` mutuo que las separe. Si no, el eje no las distingue y el
#: ejercicio de ordenar el eje se vuelve irresoluble.
AXIS_COLLISION = 4

#: Umbrales blandos: no rompen el build, salen listados en el reporte.
SOFT_DEF_MAX_WORDS = 12
SHORTEST_DISC_SHOWN = 20

#: `def` es la pista que se muestra en Reconocer y Escribir, así que va en inglés:
#: una pista en español entrenaría traducción español->inglés en vez de la
#: recuperación concepto->palabra que pide el examen. `disc` sí va en español,
#: porque es explicación que solo aparece en el feedback.
SPANISH_CHARS = set("áéíóúüñ¿¡")
SPANISH_STOPWORDS = {
    "que", "de", "la", "el", "los", "las", "con", "sin", "por", "para", "se",
    "un", "una", "es", "su", "lo", "al", "del", "como", "algo", "alguien", "muy",
}


def ej_hash(sentence: str, siblings: list[str]) -> str:
    """Hash que identifica a un ítem cloze (igual que en build_clusters.py).

    Los hermanos entran en el hash porque la unicidad depende de contra qué
    distractores compite la oración, no solo de la oración.
    """
    payload = sentence + " " + " ".join(sorted(siblings))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class Report:
    """Acumula fallos duros y avisos blandos durante la validación."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def fail(self, rule: str, detail: str) -> None:
        self.errors.append(f"[{rule}] {detail}")

    def warn(self, detail: str) -> None:
        self.warnings.append(detail)


def check_group_shape(group: dict[str, Any], report: Report) -> None:
    """Reglas 1 y 9: tamaño del grupo y eje con dos polos nombrados."""
    gid = group.get("id", "<sin id>")
    size = len(group.get("words", []))

    if size < MIN_GROUP or size > MAX_GROUP:
        report.fail(
            "R1 tamaño",
            f"{gid} tiene {size} palabras (permitido {MIN_GROUP}-{MAX_GROUP}). "
            f"El piso es {MIN_GROUP} porque Reconocer necesita 4 distractores del mismo grupo "
            f"y Equivalencia necesita 5 opciones.",
        )

    axis = group.get("axis") or {}
    if not axis.get("lo") or not axis.get("hi"):
        report.fail("R9 eje", f"{gid} no declara axis.lo y axis.hi. Si el eje no se puede nombrar, el grupo está mal formado.")

    if group.get("loose") and not group.get("looseReason"):
        report.fail("R9 eje", f"{gid} está marcado loose pero no explica el corte en looseReason.")


def looks_spanish(text: str) -> str | None:
    """Devuelve el rastro de español encontrado en el texto, o None si parece inglés.

    Parameters
    ----------
    text : str
        Texto a inspeccionar.

    Returns
    -------
    str or None
        Descripción del rastro detectado — un carácter acentuado o una palabra
        funcional castellana — para poder señalarlo en el error.
    """
    accented = SPANISH_CHARS & set(text.lower())
    if accented:
        return f"carácter '{sorted(accented)[0]}'"

    tokens = {t.strip(".,;:()\"'").lower() for t in text.split()}
    hits = tokens & SPANISH_STOPWORDS
    if hits:
        return f"palabra '{sorted(hits)[0]}'"

    return None


def check_blank_spelling(sentence: str, w: str, gid: str, report: Report) -> None:
    """Regla 12: el sufijo pegado al hueco debe producir una palabra bien escrita.

    Las oraciones usan la convención `___d`, `___ed`, `___ing`, `___s`: el hueco
    recibe el lema y el sufijo queda inmediatamente después. Eso funciona para la
    mayoría de los verbos, pero dos reglas ortográficas del inglés lo rompen, y el
    resultado es una palabra que no existe apareciendo en la app.

    Parameters
    ----------
    sentence : str
        El campo `ej`.
    w : str
        El lema que ocupará el hueco.
    gid : str
        Id del grupo, para el mensaje de error.
    report : Report
        Acumulador de fallos.
    """
    suffix = ""
    for char in sentence.split(BLANK, 1)[1]:
        if not char.isalpha():
            break
        suffix += char

    if not suffix:
        return

    # 'dissemble' + 'ing' -> 'dissembleing'. La e muda se cae antes de vocal.
    if w.endswith("e") and suffix[0] in "ei":
        report.fail(
            "R12 sufijo",
            f"{gid}/{w}: '{w}' + '{suffix}' = '{w + suffix}', que no existe. "
            "La e muda se elide: usa '___d' o reescribe la oración.",
        )

    # 'nullify' + 'd' -> 'nullifyd'. La y tras consonante pasa a i.
    if len(w) > 1 and w.endswith("y") and w[-2] not in "aeiou" and suffix in {"d", "ed", "s"}:
        report.fail(
            "R12 sufijo",
            f"{gid}/{w}: '{w}' + '{suffix}' = '{w + suffix}', que no existe. "
            "La y pasa a i ante sufijo: reescribe la oración para usar el lema solo.",
        )


def check_word_fields(word: dict[str, Any], gid: str, report: Report) -> None:
    """Reglas 3, 4 y 10: campos obligatorios, tipos, hueco en el ejemplo e idioma."""
    w = word.get("w", "<sin w>")

    for field in REQUIRED_FIELDS:
        value = word.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            report.fail("R3 campos", f"{gid}/{w}: falta o está vacío '{field}'.")

    if BLANK not in word.get("ej", ""):
        report.fail("R4 hueco", f"{gid}/{w}: el ejemplo no contiene '{BLANK}'.")
    else:
        check_blank_spelling(word.get("ej", ""), w, gid, report)

    tone = word.get("tone")
    if tone not in VALID_TONES:
        report.fail("R3 campos", f"{gid}/{w}: tone '{tone}' fuera de {sorted(VALID_TONES)}.")

    pos = word.get("axisPos")
    if not isinstance(pos, int) or not 0 <= pos <= 100:
        report.fail("R3 campos", f"{gid}/{w}: axisPos '{pos}' debe ser entero de 0 a 100.")

    if word.get("polysemous"):
        sense2 = word.get("sense2") or {}
        if not isinstance(sense2, dict):
            report.fail(
                "R3 campos",
                f"{gid}/{w}: sense2 debe ser un objeto con 'def' y 'ej', no {type(sense2).__name__}.",
            )
        elif not sense2.get("def") or not sense2.get("ej"):
            report.fail("R3 campos", f"{gid}/{w}: marcado polysemous pero sense2 no trae def y ej.")

    definition = word.get("def", "")
    if len(definition.split()) > SOFT_DEF_MAX_WORDS:
        report.warn(f"def larga ({len(definition.split())} palabras): {gid}/{w} — {definition}")

    # Regla 10: la pista va en inglés; la explicación, en español.
    for field in ("def",) + (("sense2.def",) if word.get("sense2") else ()):
        text = word["sense2"]["def"] if field == "sense2.def" else definition
        trace = looks_spanish(text)
        if trace:
            report.fail(
                "R10 idioma",
                f"{gid}/{w}: '{field}' parece español ({trace}) — «{text}». "
                f"La definición es la pista de Reconocer y Escribir y va en inglés.",
            )

    if word.get("disc") and not looks_spanish(word["disc"]):
        report.warn(f"disc podría estar en inglés: {gid}/{w} — {word['disc'][:70]}…")


def check_twins(group: dict[str, Any], report: Report) -> None:
    """Regla 8: el twin debe existir y vivir en el mismo grupo."""
    gid = group["id"]
    members = {w["w"] for w in group["words"]}

    for word in group["words"]:
        twin = word.get("twin")
        if not twin:
            continue
        if twin == word["w"]:
            report.fail("R8 twin", f"{gid}/{word['w']}: se apunta a sí misma como twin.")
        elif twin not in members:
            report.fail(
                "R8 twin",
                f"{gid}/{word['w']}: twin '{twin}' no está en el grupo. "
                f"Los distractores salen del grupo (A1), así que un twin de fuera nunca se puede contrastar.",
            )


def check_axis_collisions(group: dict[str, Any], report: Report) -> None:
    """Regla 6: dos palabras muy juntas en el eje y del mismo tono deben ser twins mutuas."""
    gid = group["id"]

    for a, b in combinations(group["words"], 2):
        pos_a, pos_b = a.get("axisPos"), b.get("axisPos")
        if not isinstance(pos_a, int) or not isinstance(pos_b, int):
            continue
        if abs(pos_a - pos_b) >= AXIS_COLLISION or a.get("tone") != b.get("tone"):
            continue

        linked = (a.get("twin") == b["w"] and a.get("whyNotTwin")) or (
            b.get("twin") == a["w"] and b.get("whyNotTwin")
        )
        if not linked:
            report.fail(
                "R6 eje",
                f"{gid}: '{a['w']}' ({pos_a}) y '{b['w']}' ({pos_b}) están a menos de {AXIS_COLLISION} "
                f"puntos con el mismo tone '{a.get('tone')}' y ninguna explica a la otra en whyNotTwin. "
                f"Tal como están, el ejercicio de ordenar el eje no tiene solución única.",
            )


def check_cloze(group: dict[str, Any], verdicts: dict[str, Any], report: Report) -> list[str]:
    """Regla 5: cada ejemplo necesita un veredicto de unicidad vigente.

    Returns
    -------
    list of str
        Etiquetas de las oraciones que se resuelven solo por gramática (aviso blando).
    """
    gid = group["id"]
    grammatical: list[str] = []
    members = [w["w"] for w in group["words"]]

    for word in group["words"]:
        others = [m for m in members if m != word["w"]]
        digest = ej_hash(word.get("ej", ""), others)
        verdict = verdicts.get(digest)

        if verdict is None:
            report.fail(
                "R5 cloze",
                f"{gid}/{word['w']}: sin veredicto de unicidad vigente (hash {digest}). "
                f"Si editaste la oración o cambió la composición del grupo, hay que volver a juzgarla.",
            )
            continue

        if verdict.get("verdict") != "unique":
            also = ", ".join(verdict.get("alsoFits", [])) or "?"
            report.fail(
                "R5 cloze",
                f"{gid}/{word['w']}: el ejemplo no es discriminante — también encajan: {also}. "
                f"Reescribir la oración.",
            )
        elif verdict.get("alsoFits"):
            report.fail(
                "R5 cloze",
                f"{gid}/{word['w']}: veredicto 'unique' pero alsoFits no está vacío. Contradicción en el registro.",
            )

        if verdict.get("basis") == "grammatical":
            grammatical.append(f"{gid}/{word['w']}")

    return grammatical


def check_tc_bank(universe: set[str], report: Report) -> dict[str, int]:
    """Valida el banco de ítems TC/SE auténticos que alimenta 'Leer la oración' y el Simulacro.

    Parameters
    ----------
    universe : set of str
        Todas las palabras del Excel, para comprobar que los `targets` existen.
    report : Report
        Acumulador de fallos.

    Returns
    -------
    dict
        Conteo de ítems por tipo, para el reporte.
    """
    path = DATA_DIR / "tc_bank.json"
    if not path.exists():
        return {}

    bank = load_json(path).get("items", [])
    counts: dict[str, int] = {}
    expected_answers = {"TC1": 1, "TC2": 2, "TC3": 3, "SE": 2}

    for item in bank:
        iid = item.get("id", "<sin id>")
        kind = item.get("type", "")
        counts[kind] = counts.get(kind, 0) + 1

        text = item.get("text", "")
        if text.count(BLANK) != max(expected_answers.get(kind, 1), 1) and kind != "SE":
            report.fail("R11 banco", f"{iid}: {kind} debería tener {expected_answers.get(kind)} hueco(s) '{BLANK}'.")
        elif kind == "SE" and BLANK not in text:
            report.fail("R11 banco", f"{iid}: el ítem SE no tiene hueco '{BLANK}'.")

        # La pista se resalta en el paso 2, así que tiene que existir literal en el texto.
        clue = item.get("clue", "")
        if not clue:
            report.fail("R11 banco", f"{iid}: falta 'clue'; sin ella el paso 2 del modo no se puede construir.")
        elif clue not in text:
            report.fail("R11 banco", f"{iid}: 'clue' no aparece literal en 'text', así que no se puede resaltar.")

        options = item.get("options", [])
        answers = item.get("answer", [])
        if len(answers) != expected_answers.get(kind, 1):
            report.fail("R11 banco", f"{iid}: {kind} necesita {expected_answers.get(kind)} respuesta(s), tiene {len(answers)}.")
        for answer in answers:
            if answer not in options:
                report.fail("R11 banco", f"{iid}: la respuesta '{answer}' no está entre las opciones.")
        if len(set(options)) != len(options):
            report.fail("R11 banco", f"{iid}: hay opciones repetidas.")
        if kind == "SE" and len(options) != 6:
            report.fail("R11 banco", f"{iid}: SE lleva 6 opciones, tiene {len(options)}.")

        if not item.get("signal", {}).get("relation"):
            report.fail("R11 banco", f"{iid}: falta signal.relation; es la respuesta del paso 1.")
        if item.get("blankTone") not in VALID_TONES:
            report.fail("R11 banco", f"{iid}: blankTone '{item.get('blankTone')}' fuera de {sorted(VALID_TONES)}.")

        for target in item.get("targets", []):
            if target not in universe:
                report.fail("R11 banco", f"{iid}: target '{target}' no existe en words.json.")

    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="reporta huérfanos sin fallar (durante el backfill por lotes)",
    )
    args = parser.parse_args()

    report = Report()
    words = load_json(DATA_DIR / "words.json")
    universe = [entry["w"] for entry in words]

    verdicts_path = DATA_DIR / "cloze_verdicts.json"
    raw_verdicts = load_json(verdicts_path) if verdicts_path.exists() else {}
    verdicts = {k: v for k, v in raw_verdicts.items() if not k.startswith("_")}

    groups = [load_json(p) for p in sorted(GROUPS_DIR.glob("*.json"))]

    seen: dict[str, str] = {}
    grammatical: list[str] = []
    tones: dict[str, int] = {}
    tiers: dict[int, int] = {}
    all_words: list[tuple[str, str, str]] = []

    for group in groups:
        gid = group.get("id", "<sin id>")
        check_group_shape(group, report)
        check_twins(group, report)
        check_axis_collisions(group, report)
        grammatical.extend(check_cloze(group, verdicts, report))

        for word in group.get("words", []):
            check_word_fields(word, gid, report)
            w = word.get("w", "")

            # Regla 7: una palabra no puede vivir en dos grupos.
            if w in seen:
                report.fail("R7 duplicado", f"'{w}' aparece en {seen[w]} y en {gid}.")
            else:
                seen[w] = gid

            tones[word.get("tone", "?")] = tones.get(word.get("tone", "?"), 0) + 1
            tiers[word.get("tier", 0)] = tiers.get(word.get("tier", 0), 0) + 1
            all_words.append((w, gid, word.get("disc", "")))

    tc_counts = check_tc_bank(set(universe), report)

    # Regla 2: cobertura contra words.json.
    orphans = [w for w in universe if w not in seen]
    stray = [w for w in seen if w not in set(universe)]

    for w in stray:
        report.fail("R2 cobertura", f"'{w}' está en {seen[w]} pero no existe en words.json.")

    if orphans and not args.allow_partial:
        preview = ", ".join(orphans[:12])
        report.fail(
            "R2 cobertura",
            f"{len(orphans)} palabras sin grupo. orphans: [{preview}"
            f"{', …' if len(orphans) > 12 else ''}]",
        )

    # ---------------- Reporte ----------------
    print("=" * 62)
    print("REPORTE DE VALIDACIÓN")
    print("=" * 62)

    covered = len(seen)
    print(f"\nCobertura        : {covered}/{len(universe)} ({100 * covered / len(universe):.1f}%)")
    print(f"Grupos           : {len(groups)}")
    loose = [g["id"] for g in groups if g.get("loose")]
    print(f"Grupos loose     : {len(loose)}{' — ' + ', '.join(loose) if loose else ''}")

    print("\nTamaño por grupo:")
    for group in groups:
        mark = " (loose)" if group.get("loose") else ""
        print(f"  {group.get('id'):<6} n={len(group.get('words', [])):<2} {group.get('name', '')}{mark}")

    print("\nDistribución de tone:")
    for tone in ("neg", "neu", "pos"):
        n = tones.get(tone, 0)
        bar = "█" * round(30 * n / max(covered, 1))
        print(f"  {tone}  {n:>4}  {bar}")

    print("\nDistribución de tier:")
    for tier in sorted(tiers):
        print(f"  tier {tier}: {tiers[tier]}")

    if tc_counts:
        total_tc = sum(tc_counts.values())
        by_kind = ", ".join(f"{k}={v}" for k, v in sorted(tc_counts.items()))
        print(f"\nBanco TC/SE auténtico: {total_tc} ítems ({by_kind}) — meta 150")

    if grammatical:
        print(f"\nCloze que se resuelven solo por gramática ({len(grammatical)}):")
        for label in grammatical:
            print(f"  {label}")

    print(f"\nLas {SHORTEST_DISC_SHOWN} entradas con 'disc' más corta (candidatas a estar mal escritas):")
    for w, gid, disc in sorted(all_words, key=lambda t: len(t[2]))[:SHORTEST_DISC_SHOWN]:
        print(f"  {len(disc):>4} car  {gid}/{w}")

    if orphans:
        label = "AVISO" if args.allow_partial else "ERROR"
        print(f"\n{label}: {len(orphans)} palabras todavía sin grupo.")

    if report.warnings:
        print(f"\nAvisos blandos ({len(report.warnings)}):")
        for warning in report.warnings:
            print(f"  {warning}")

    print("\n" + "-" * 62)
    if report.errors:
        print(f"FALLA: {len(report.errors)} error(es)\n")
        for error in report.errors:
            print(f"  {error}")
        return 1

    print("VERDE: todas las reglas duras pasan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
