# CLAUDE.md — Entrenador de discriminación léxica (GRE)

> Nota: el `CLAUDE.md` de la carpeta padre (`~/Downloads/CLAUDE.md`) es de otro proyecto
> — KN Hack, finanzas cuantitativas — y **no aplica aquí**. Ignóralo.

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

- **131 grupos, 754/1112 palabras (67.8%)**, `run_all.py` en verde, 0 errores
- Banco TC/SE auténtico: **24/150 ítems**
- La app todavía **no existe**; `data/data.js` ya está listo para que la consuma
- Ya es repo git (`main`): cada lote se comitea al cerrar

## Anatomía

```
Greg Mat Vocab List (...).csv   fuente, no se toca
data/words.json                 universo extraído del CSV (1112 palabras)
data/groups/gNNN-slug.json      un archivo por grupo, editable a mano  ← aquí se trabaja
data/field_map.json             plan de campos semánticos con candidatos verificados
data/cloze_verdicts.json        veredictos de unicidad, indexados por hash
data/data.json / data.js        dataset ensamblado que consume la app
tc_bank.json                    banco TC/SE auténtico (meta 150)
reports/latest.txt              informe de la última corrida
reports/status.json             estado legible por máquina: qué falta
```

`data.js` existe además de `data.json` porque `fetch()` sobre `file://` está bloqueado por
CORS: la app tiene que abrir desde el sistema de archivos sin servidor.

## Flujo de un lote

Tamaño razonable: **4–5 grupos (~22–26 palabras)**.

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

- **El hash del cloze incluye a los hermanos.** Si cambia la composición del grupo, los
  veredictos caducan y hay que volver a juzgar. Es a propósito: la unicidad depende de contra
  qué distractores compite la oración.
- **Sinónimos verdaderos no pueden ser hermanos.** `hamper`/`hinder`/`impede` no tienen firma
  colocacional que los separe: como hermanos no producen cloze únicos. Necesitan un grupo
  diseñado por dominios (`occlude`→conducto, `inhibit`→proceso, `circumscribe`→alcance).
- **Campo "presagiar" bloqueado**: solo quedan 4 verbos libres (`presage`, `portend`,
  `forebode`, `prefigure`) y `harbinger` es sustantivo.
- **`placate`/`mollify`/`appease` son tres sinónimos verdaderos.** Ninguna oración separa a
  dos de ellos: lo que calma un enojo sirve para los tres. Están en `data/parked.json`; el
  campo "calmar" se cerró con los cinco que sí tienen dominio propio (`lull` → falsa
  seguridad, `propitiate` → dios, `pacify` → provincia, `mediate` → entre partes,
  `reconcile` → versiones que no cuadran).
- **Campos bloqueados por falta de quinta palabra**: "pena y remordimiento" (solo
  `chagrin`, `vexation`, `grievance`, `dirge`) y "el que actúa por otro" (solo `proxy`,
  `surrogate`, `intermediary`, `latitude`). No existen en la lista *remorse*, *contrition*,
  *emissary*, *envoy* ni *deputy*.
- **Campo "cansancio y desgana" bloqueado**: no queda ningún adjetivo libre (`lethargic`,
  `languid`, `phlegmatic`, `sluggish`, `weary`, `soporific` ya están colocados) y los
  sustantivos son solo 4: `lassitude`, `torpor`, `ennui`, `apathy`. `languish` es verbo.
- **`penchant`/`predilection` no pueden ser hermanas.** En el sentido de "afición" son
  intercambiables: penchant pide objeto de gusto, predilection pide preferencia previa,
  pero ninguna oración excluye a la otra sin sonar forzada. Y el campo "inclinación (n)"
  solo tiene esas dos más `proclivity`, `propensity` y `affinity` — es decir, no llega a 5
  sin meterlas juntas. Ese grupo queda bloqueado hasta que aparezca un sustantivo más.
- **El artículo delante del hueco delata la respuesta.** En grupos de sustantivos, `an ___`
  descarta de un vistazo a los cuatro hermanos que empiezan por consonante: el ítem se
  resuelve por gramática y no enseña nada (le pasó a `ideologue` en g120). La salida es
  poner el hueco tras `the` o tras un plural — `the reflex of the ___` — que sirve para
  los cinco.
- **`robust` se cuela en casi cualquier hueco de firmeza.** En g126 hubo que reescribir dos
  cloze por su culpa: *her most ___ defender* admite `robust` («a robust defender» es
  inglés corriente) y *her alibi was ___* también («a robust alibi»). La salida fue sacar a
  `steadfast` del terreno del apoyo — una **mirada** que no se aparta — y a `ironclad` al de
  la **garantía sin resquicio** («no exclusions, no small print»). Regla práctica: si el
  hueco admite «fuerte» a secas, `robust` lo llena.
- **`banal` no se gasta, nace vacía.** Es lo que la separa de `hackneyed`, y el cloze de
  `hackneyed` tiene que decirlo: si la frase sigue diciendo lo justo y lo que la inutiliza
  es la repetición, `banal` queda fuera. Un cloze de `hackneyed` que solo diga «trillado»
  lo llenan las dos.
- **`wander off into ___` no separa `digression` de `soliloquy`.** «Launch into a soliloquy»
  es igual de idiomático. Hace falta **un interlocutor que pregunte y un regreso al tema**:
  el soliloquy exige estar solo y no vuelve de ninguna parte.
- **`facetious` solo se separa de `droll` por la colocación fija.** Cualquier cloze del tipo
  «su ___ respuesta — algo sobre la máquina de café — no satisfizo a nadie» lo llena `droll`
  igual de bien: una respuesta de humor seco también deja a todos insatisfechos si la
  pregunta era grave. La salida en g129 fue el reproche hecho: **«Don't be ___»** más una
  pregunta seria contestada con un chiste. «Don't be droll» no es inglés.
- **`slovenly` se cuela en cualquier hueco de institución dejada.** El primer cloze de
  `decadent` en g130 («no army worth the name, nobody left who remembered why the rules
  existed») lo llenaba `slovenly`: eso es desidia administrativa, no decadencia. `decadent`
  necesita **lujo que se está comiendo un patrimonio previo** — banquetes de nueve horas que
  se comen la renta de una provincia —, porque lo suyo es la caída desde una altura, no el
  desorden.
- **`extemporize` y `expatiate` comparten la preposición `on`.** «Expatiate on drainage for
  an hour» y «extemporize on drainage for an hour» son las dos inglés corriente, así que la
  longitud y el tema no separan nada. Lo que sí separa es **el soporte**: `expatiate` vale
  para lo escrito (cuarenta páginas), y `extemporize` no puede serlo — sin guion previo no
  hay páginas. `improvise` queda libre pero es sinónimo verdadero de `extemporize` en el
  sentido de hablar sin preparación: no pueden ser hermanas.
- **Los sustantivos de persona sí discriminan bien.** Al revés que los adjetivos de calma
  o los verbos de estorbar, cada tipo humano trae su escena propia (el martinet y la
  hebilla, el recluse y el correo sin recoger), y esa escena excluye sola a los hermanos.
  Quedan libres para un grupo futuro `miscreant`, `reprobate` y `libertine`, pero son solo
  tres: hacen falta dos personajes reprobables más.

## Qué NO hacer

- **Nunca** marcar `unique` un cloze que otro hermano puede llenar. Es la regla que sostiene
  el proyecto entero: un cloze ambiguo enseña el grupo, que es justo el problema a resolver.
- **Nunca** mezclar POS para llegar al piso de 5 palabras.
- **Nunca** editar `data/data.json` o `data.js` a mano: se regeneran desde `data/groups/`.
- **Nunca** cerrar un lote sin que `run_all.py` salga en verde.
