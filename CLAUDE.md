# CLAUDE.md — Entrenador de discriminación léxica (GRE)

> Este archivo se carga entero en **cada turno**, así que se mantiene corto a propósito.
> Lo que solo hace falta al armar grupos vive en [`docs/trampas.md`](docs/trampas.md).

## Qué es esto

Dataset para una app de estudio de vocabulario GRE. El usuario presenta el **23 de octubre
de 2026** y estudia la lista completa de Vocab Mountain de GregMat (1112 palabras únicas).

El problema que ataca: agrupar sinónimos produce **interferencia asociativa** — sabes a qué
grupo pertenece una palabra sin poder distinguirla de sus vecinas. Eso alcanza para Sentence
Equivalence pero falla en **Text Completion**, que es donde se decide el score de Verbal.
Por eso todos los distractores salen del mismo grupo.

**El criterio que decide cualquier duda de diseño es "¿esto lo prepara mejor para el examen?",
no "¿esto es más elegante o más completo?".**

## Estado actual

Actualiza esta sección al cerrar cada lote.

- **186 grupos, 1037/1112 palabras (93.3%)**, `run_all.py` en verde, 0 errores
- Grupos `loose`: **2** (g183, g184). g185 y g186 **no** son loose: los dos ejes se defienden palabra
  por palabra (escala de daño; apetito de bienes)
- Banco TC/SE auténtico: **109/150 ítems** (TC1=83, TC2=2, SE=24). Los TC de dos huecos
  llevan `optionGroups`: una columna de 3 opciones por hueco, como en el examen. R11 exige
  que `options` sea la concatenación en orden y que cada respuesta caiga en su columna
- **App** en `app/index.html`. Se abre con doble clic, sin servidor. Progreso en
  `localStorage`, feedback sobre el eje. Motor anti-interferencia completo: Leitner
  0·1·3·7·16, matriz de confusión **por par y dirigida**, contrastivo forzado hasta cerrar
  cada par, "dominado" solo si el grupo no tiene pares abiertos (nunca por promedio),
  repaso diario mixto y sesión de sábado. **7 formatos**: Discriminar, Reconocer, Contrastivo,
  Escribir, Equivalencia (SE), Ordenar por intensidad y Leer la oración (TC) — ver `ESTADO.md`
- **Cobertura efectiva 1112/1112 (100%)**: 1037 en grupos + 75 solo en el banco. El informe
  dice 93.3% porque solo cuenta grupos, y está bien que lo haga
- **El banco es la salida de lo que los grupos no pueden contener.** Sinónimos verdaderos →
  un ítem **SE**; huérfana suelta sin campo ni pareja → un ítem **TC1**, que no necesita campo
  semántico ni POS uniforme. **No fuerces un grupo para colocar una palabra**: escribe el ítem.
  El bloque D quedó agotado por esta vía, con los 8 campos posibles documentados en
  `docs/trampas.md`
- Ya es repo git (`main`): cada lote se comitea al cerrar

## Anatomía

```
Greg Mat Vocab List (...).csv   fuente, no se toca
data/words.json                 universo extraído del CSV (1112 palabras)
data/groups/gNNN-slug.json      un archivo por grupo, editable a mano  ← aquí se trabaja
data/field_map.json             plan de campos semánticos con candidatos verificados
data/cloze_verdicts.json        veredictos de unicidad, indexados por hash
data/data.json / data.js        dataset ensamblado que consume la app
data/tc_bank.json               banco TC/SE auténtico (meta 150; hoy 36, sin usar aún en la app)
reports/latest.txt              informe de la última corrida
reports/status.json             estado legible por máquina: qué falta
app/index.html                  la app, un solo archivo, se abre con doble clic
docs/trampas.md                 campos que ya fallaron; se lee al armar grupos, no siempre
```

`data.js` existe además de `data.json` porque `fetch()` sobre `file://` está bloqueado por
CORS: la app tiene que abrir desde el sistema de archivos sin servidor.

## Flujo de un lote

Tamaño razonable: **4–5 grupos (~22–26 palabras)**.

0. **Lee [`docs/trampas.md`](docs/trampas.md) entero antes de proponer ningún campo.** Ahí
   está lo que ya se intentó y falló. Saltarse este paso es cómo se reintenta un campo
   muerto y se descubre a las dos horas de trabajo.
1. Elegir campos. `reports/latest.txt`, sección "campos planificados pendientes", ya solo
   sirve como pista: la mayoría de los campos que quedan ahí se agotan en 3–4 palabras de
   la misma categoría gramatical. **Desde g103 los grupos se arman leyendo la lista de
   palabras libres** y buscando ahí un campo con 5+ de un mismo POS:
   ```
   python3 -c "import json,glob; used={w['w'] for f in glob.glob('data/groups/*.json') for w in json.load(open(f))['words']}; parked={x['w'] for x in json.load(open('data/parked.json'))['parked']}; print([e['w'] for e in json.load(open('data/words.json')) if e['w'] not in used and e['w'] not in parked])"
   ```
2. **Verificar candidatos ANTES de redactar**:
   `python3 scripts/check_candidates.py --field "sumiso adj" obsequious subservient ...`
   El gate detecta palabras inventadas, pero para entonces ya escribiste el grupo entero y
   hay que rehacer todos los veredictos, porque el hash incluye a los hermanos.
3. Escribir `data/groups/gNNN-slug.json`.
4. `python3 scripts/build_clusters.py`
5. Juzgar cada cloze: `python3 scripts/record_verdicts.py --list`, y luego
   `--unique "palabra:hermano_más_cercano:por qué los demás no encajan"`.
   **El juicio lo haces tú, no el script.** Si un hermano también encaja, la oración se
   reescribe — no se marca `unique`.
6. `python3 scripts/run_all.py` — tiene que salir **VERDE** antes de dar el lote por cerrado.

## Reglas de contenido (ya decididas, no re-litigar)

1. **Idioma por campo.** `def` en **inglés** (es la pista de Reconocer y Escribir; en español
   entrenaría traducción en vez de recuperación concepto→palabra). `disc`, `whyNotTwin`,
   nombres de grupo y polos del eje en **español**: solo aparecen en el feedback.
2. **Agrupar por campo semántico Y categoría gramatical a la vez.** Un grupo con POS mezclado
   produce ítems que se resuelven por gramática ("The ___ heir" solo admite un adjetivo).
   `loose` es último recurso, no primera salida.
3. **Cláusula de rechazo** ("Nobody flattered anyone: the board had simply become ___") solo
   para **pares de inclusión**, donde una palabra contiene a la otra: `obsequious`⊃`subservient`,
   `specious`⊃`fallacious`, `prolix`⊃`verbose`. Es la única construcción que los separa.
4. **Dos bancos de oraciones distintos.** El `ej` discriminante puede ser artificioso — su
   trabajo es enseñar la distinción. El banco TC/SE (`tc_bank.json`) va en registro auténtico,
   con palabras señal, y alimenta el modo "Leer la oración" y el Simulacro.
5. **La unicidad se mide distinto en cada banco.** En un `ej` de grupo la oración compite
   contra **todos** los hermanos, y por eso hay que blindarla tanto. En el banco TC/SE compite
   solo contra **las cinco o seis opciones impresas**: basta con que ninguna otra de esas
   funcione. Eso permite huecos que un sinónimo ausente también llenaría — y cuando ese
   sinónimo es de los que el alumno debe tener presentes, se nombra en el `trapNote`
   («fíjate en que poise y aplomb no están entre las opciones»), que es exactamente la
   disciplina que pide el examen real.

## Reglas duras (las verifica `scripts/validate.py`)

| | |
|---|---|
| R1 | tamaño de grupo 5–9 |
| R2 | cobertura contra `words.json`; nada inventado |
| R3 | campos obligatorios, `tone` ∈ {neg,neu,pos}, `axisPos` 0–100 |
| R4 | el `ej` contiene `___` |
| R5 | cada `ej` necesita veredicto de unicidad **vigente** |
| R6 | dos palabras a <4 puntos del eje con el mismo `tone` exigen `whyNotTwin` mutuo |
| R7 | una palabra vive en un solo grupo |
| R8 | el `twin` existe y está en el mismo grupo |
| R9 | el eje declara `lo` y `hi`; `loose` exige `looseReason` |
| R10 | `def` en inglés, `disc` en español |
| R11 | integridad del banco TC/SE |
| R12 | el sufijo pegado al hueco produce una palabra que existe (`dissemble`+`ing` ✗) |

## Trampas conocidas

**Están en [`docs/trampas.md`](docs/trampas.md)** — el registro de campos que ya se
intentaron y fallaron, y de pares de palabras que no pueden ser hermanas.

Se sacó de aquí porque `CLAUDE.md` se carga entero en cada turno y el registro pesaba el
84% del archivo, mientras que solo hace falta al armar un grupo. **Léelo completo en el
paso 1 del flujo de un lote**, antes de proponer ningún campo, y **añade ahí** lo que
descubras — no aquí.

## Qué NO hacer

- **Nunca** marcar `unique` un cloze que otro hermano puede llenar. Es la regla que sostiene
  el proyecto entero: un cloze ambiguo enseña el grupo, que es justo el problema a resolver.
- **Nunca** mezclar POS para llegar al piso de 5 palabras.
- **Nunca** editar `data/data.json` o `data.js` a mano: se regeneran desde `data/groups/`.
- **Nunca** cerrar un lote sin que `run_all.py` salga en verde.
