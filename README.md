# Entrenador de discriminación léxica — GRE

Una app de estudio para la lista completa de **Vocab Mountain** de GregMat
(1112 palabras), construida sobre una idea concreta:

> Agrupar sinónimos mejora la memorización, pero produce **interferencia
> asociativa**: acabas sabiendo a qué grupo pertenece una palabra sin poder
> distinguirla de sus vecinas. Eso basta para Sentence Equivalence y falla en
> Text Completion, que es donde se decide el score de Verbal.

Por eso **todos los distractores salen del mismo grupo**, y el sistema no da una
palabra por sabida hasta que la separas de la que se le parece.

## Abrir la app

**En el móvil o en cualquier navegador:**

### 🔗 https://many1026.github.io/gre-vocab-discriminacion/

Añádela a la pantalla de inicio y funciona como una app (Safari: Compartir →
Añadir a pantalla de inicio · Chrome: ⋮ → Añadir a pantalla principal).

**En este ordenador:** doble clic en [`app/index.html`](app/index.html). No hace
falta servidor.

**Sin conexión (avión, metro):**

```bash
python3 scripts/build_standalone.py     # escribe app/gre-movil.html
```

Genera **un solo archivo** de 1.2 MB, sin dependencias, que se manda por AirDrop
o Drive y abre al tocarlo.

> El progreso se guarda en el navegador de cada dispositivo. Lo que estudies en el
> móvil no se mezcla con lo del portátil: elige uno como el oficial.

**El plan de estudio hasta el examen está en [`PLAN.md`](PLAN.md)**, con checklist
semanal y una tabla para llevar el registro.

## Los ocho formatos

| Formato | Qué entrena |
|---|---|
| **Repaso del día** | Lo que vence hoy según el Leitner, con los formatos mezclados |
| **Discriminar** | Una oración con un hueco; las opciones son todas del mismo grupo |
| **Reconocer** | Definición → palabra, en la dirección difícil |
| **Escribir** | Producir la palabra sin verla (*generation effect*) |
| **Cara a cara** | Solo el par que confundiste, hasta cerrarlo |
| **Leer la oración** | Text Completion en registro de examen (115 ítems) |
| **Equivalencia** | Las dos que dejan la oración con el mismo sentido (35 ítems) |
| **Intensidad** | Colocar cuatro palabras del grupo sobre su eje |

El **sábado** la portada cambia sola: sesión mixta de 18, sin mirar nada antes.

## Cómo funciona por dentro

- **Leitner 0 · 1 · 3 · 7 · 16 días.** Acertar sube de caja, fallar devuelve a la 0.
- **Matriz de confusión dirigida.** Al fallar se guarda *qué* palabra elegiste, no
  solo que fallaste. El par queda **abierto** hasta que lo aciertes dos veces cara
  a cara.
- **Dominado por pares, nunca por promedio.** Un grupo se domina cuando todas sus
  palabras están en caja ≥3 **y** no le queda ningún par abierto.
- **Interleaving duro.** Nunca dos ítems seguidos del mismo grupo.
- **El nombre del grupo no se muestra durante la pregunta**, solo al responder.

## Estructura

```
Greg Mat Vocab List (...).csv   fuente, no se toca
data/words.json                 universo extraído del CSV (1112 palabras)
data/groups/gNNN-slug.json      un archivo por grupo, editable a mano  ← aquí se trabaja
data/tc_bank.json               banco TC/SE en registro de examen (150 ítems)
data/cloze_verdicts.json        veredictos de unicidad, indexados por hash
data/data.json · data.js        dataset ensamblado que consume la app
app/index.html                  la app (un archivo, sin servidor)
scripts/build_standalone.py     empaqueta la app + los datos en un solo archivo
reports/latest.txt              informe de la última corrida
docs/trampas.md                 campos que ya fallaron; se lee antes de armar un grupo
PLAN.md                         plan día a día hasta el examen
```

`data.js` existe además de `data.json` porque `fetch()` sobre `file://` está
bloqueado por CORS: la app tiene que abrir desde el sistema de archivos.

## Añadir palabras a mano

Los grupos se editan a mano; lo demás se genera. **Nunca edites `data/data.json`
ni `data.js`.**

1. **Lee [`docs/trampas.md`](docs/trampas.md) entero** antes de proponer un campo.
   Ahí está lo que ya se intentó y falló; saltárselo es cómo se reintenta un campo
   muerto.

2. **Verifica los candidatos antes de escribir nada:**

   ```bash
   python3 scripts/check_candidates.py --field "sumiso adj" obsequious subservient servile
   ```

3. **Crea `data/groups/gNNN-slug.json`** siguiendo el esquema de cualquier grupo
   existente: `axis` con polos `lo`/`hi`, y por palabra `w`, `pos`, `def` (en
   inglés), `disc` (en español), `tone`, `axisPos`, `ej` con `___`, `twin` y
   `whyNotTwin`.

4. **Ensambla y juzga la unicidad:**

   ```bash
   python3 scripts/build_clusters.py
   python3 scripts/record_verdicts.py --list
   python3 scripts/record_verdicts.py --unique "palabra:hermano_más_cercano:por qué los demás no encajan"
   ```

   **El juicio lo haces tú, no el script.** Si un hermano también encaja en la
   oración, se reescribe la oración — no se marca `unique`.

5. **Comprueba que todo sigue en verde:**

   ```bash
   python3 scripts/run_all.py
   ```

### Si una palabra no cabe en ningún grupo

No fuerces un grupo: **escribe un ítem del banco**. Es lo que se hizo con las 75
palabras que no formaban campo.

- Dos **sinónimos verdaderos** que ningún cloze separa → un ítem **SE**, donde las
  dos son la respuesta (que es como aparecen en el examen).
- Una palabra **suelta**, sin pareja ni campo → un ítem **TC1**, que no necesita
  campo semántico ni categoría gramatical uniforme.

Escribe el lote con un script que valide antes de tocar `tc_bank.json` (hay
ejemplos en el historial): las respuestas deben estar en el dataset **en su forma
base** — ni conjugadas ni en plural, o no cruzan con `words.json`.

## Reglas duras

Las verifica `scripts/validate.py` y `run_all.py` tiene que salir en verde:

| | |
|---|---|
| R1 | tamaño de grupo 5–9 |
| R2 | cobertura contra `words.json`; nada inventado |
| R3 | campos obligatorios, `tone` ∈ {neg,neu,pos}, `axisPos` 0–100 |
| R4 | el `ej` contiene `___` |
| R5 | cada `ej` necesita veredicto de unicidad vigente |
| R6 | dos palabras a <4 puntos del eje con el mismo `tone` exigen `whyNotTwin` mutuo |
| R7 | una palabra vive en un solo grupo |
| R8 | el `twin` existe y está en el mismo grupo |
| R9 | el eje declara `lo` y `hi`; `loose` exige `looseReason` |
| R10 | `def` en inglés, `disc` en español |
| R11 | integridad del banco TC/SE |
| R12 | el sufijo pegado al hueco produce una palabra que existe |

## Estado

- **186 grupos · 1037 palabras agrupadas** (93.3%)
- **75 palabras más en el banco** → cobertura efectiva **1112/1112 (100%)**
- **Banco TC/SE: 150 ítems** (TC1 = 105, TC2 = 10, SE = 35)
- 8 formatos · las 9 restricciones anti-interferencia cumplidas
- `run_all.py` en verde, 0 errores
