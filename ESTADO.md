# ESTADO — auditoría del 29 de agosto de 2026

**55 días para el examen (23 de octubre de 2026).**

Auditoría de Fase 0. Nada se modificó salvo este archivo y la corrida de verificación
(`reports/run_20260829_233215.txt`).

---

## 1. Git

| | |
|---|---|
| Rama | `main`, limpia — 0 cambios sin commitear |
| Último commit | `12d8201` — "CLAUDE.md de 44KB a 7.8KB: las trampas salen a docs/trampas.md" (24 ago) |
| Remoto | `https://github.com/many1026/gre-vocab-discriminacion.git`, **sincronizado** |
| Ramas colgadas | ninguna |
| Stashes | ninguno |

No hay trabajo perdido ni a medio guardar. El repo quedó cerrado en un punto limpio.

## 2. Qué existe

El proyecto está **mucho más avanzado de lo que asume el prompt de reanudación**. No hay
`PROMPT_VOCAB_CLUSTERS.md` ni `vocab-clusters.html` ni `clusters.json`: esa etapa se superó
hace ~30 commits. Lo que hay es un pipeline con validación automática y 186 grupos.

```
Greg Mat Vocab List (37 Groups, 1,110 Words) - Word List.csv   fuente (131 filas × 38 cols)
data/words.json           1112 palabras únicas extraídas
data/groups/*.json        186 archivos, uno por grupo   ← el trabajo real
data/cloze_verdicts.json  1038 veredictos de unicidad, hasheados
data/tc_bank.json         banco TC/SE auténtico: 36 ítems (TC1=24, TC2=2, SE=10)
data/parked.json          8 palabras apartadas con razón documentada
data/form_confusions.json pares que se confunden por forma (ingenuous/ingenious)
data/data.json + data.js  dataset ensamblado que consume la app
scripts/*.py              extract → build → validate → run_all
reports/latest.txt        informe; reports/status.json, estado legible por máquina
app/index.html            la app, 528 líneas, un archivo, sin servidor
docs/trampas.md           campos que ya fallaron
```

**Verificación de hoy — `python3 scripts/run_all.py` sale VERDE:**

```
extract ok · build ok · validate ok
cobertura : 1037/1112 (93.3%)
grupos    : 186  (loose: 2)
sin grupo : 75
errores   : 0
```

## 3. Cobertura

| | |
|---|---|
| Palabras en el CSV | **1112** únicas (el título dice 1110; hay 1113 celdas, una duplicada — `cumbersome` — y un typo corregido, `all-ecompassing`) |
| Clusterizadas | **1037 (93.3%)** en 186 grupos |
| Sin grupo | **75** |
| — de esas, apartadas a propósito | **8** (`data/parked.json`) |
| — pendientes reales | **67** |

Las 8 apartadas no son un olvido: son casos donde la discriminación por cloze no es posible.
`placate` / `mollify` / `appease` son sinónimos verdaderos; ninguna oración los separa. Meterlos
en un grupo produciría exactamente el ítem ambiguo que el proyecto entero existe para evitar.

Las 67 restantes son **las sobras**: lo que quedó tras 186 pasadas es lo más difícil de agrupar,
porque cada una necesita 4 compañeras del mismo POS y del mismo campo que aún estén libres.
Son ~3 lotes en el mejor caso y bastantes más si hay que abrir campos nuevos.

## 4. La app: lo que está y lo que no

`app/index.html` es un MVP funcional: abre con doble clic, guarda progreso en `localStorage`,
muestra el eje semántico en el feedback. Pero contra lo que pide el spec:

**Formatos: 6 de 6** (eran 2 al empezar la auditoría).

| Formato | Estado |
|---|---|
| Cloze ("Discriminar") | ✅ |
| Reconocer (def → palabra) | ✅ |
| Contrastivo forzado | ✅ bloque B |
| Escribir (producción) | ✅ bloque C |
| Equivalencia (SE) | ✅ bloque C — limitado a los 10 ítems SE del banco |
| Ordenar por intensidad | ✅ bloque C |

**Restricciones anti-interferencia: 1 de 9 cumplida.**

| # | Restricción | Estado |
|---|---|---|
| 1 | Distractores siempre del mismo grupo | ✅ `currentOptions()` usa `e.g.words` |
| 2 | Nunca mostrar el nombre del grupo en la pregunta | ✅ **arreglado en el bloque A** (era la violación grave) |
| 3 | Nunca dos ítems seguidos del mismo grupo | ✅ **arreglado en el bloque A** (antes solo ×0.25) |
| 4 | El repaso mezcla grupos **y formatos** | ✅ **bloque B** — "Repaso del día" |
| 5 | Matriz de confusión por par | ✅ **arreglado en el bloque A** (antes se descartaba el `pick`) |
| 6 | Pares confundidos → contrastivo automático | ✅ **bloque B** |
| 7 | Dominado solo al resolver todos los pares | ✅ **bloque B** |
| 8 | Leitner 0·1·3·7·16 | ✅ **bloque B** |
| 9 | Sesión de sábado mezclada | ✅ **bloque B** |

**Las 9 están cumplidas.**

La #2 es el hallazgo grave: **cada sesión que estudies hoy te está regalando la categoría
mientras contestas**, que es literalmente la interferencia asociativa que el proyecto combate.
Es un arreglo de una línea.

La #5 es la más cara en tiempo: los datos de qué palabra confundiste **no se están guardando**,
así que cada día que estudias sin arreglarlo es un día de diagnóstico perdido para siempre.

## 5. Banco TC/SE

36 de 150 ítems (24%). Es el material en registro auténtico de examen, con palabras señal y
`trapNote`. Alimenta el modo "Leer la oración" y el Simulacro — **ninguno de los dos existe
todavía en la app**, así que hoy esos 36 ítems no se usan.

## 6. Choques entre el prompt de reanudación y lo construido

Cinco, y necesito tu decisión en dos de ellos (§8).

1. **`def` en español (spec) vs. inglés (repo).** Las 1037 definiciones están en inglés por
   decisión documentada: son la pista del modo Reconocer, y en español entrenarían traducción
   en vez de recuperación concepto→palabra. Cambiarlo es rehacer 1037 campos.
2. **`pos` 0–100 (spec) vs. el esquema real.** El repo usa `pos` para la categoría gramatical y
   `axisPos` 0–100 para la intensidad. Mismo contenido, dos campos en vez de uno; el del repo es
   más rico y `validate.py` depende de él.
3. **"Respeta los Vocab Groups de GregMat" (spec Fase 1) — no aplica.** Verificado leyendo el
   CSV: los "Group 1..38" son **lotes de estudio alfabéticos de 30 palabras**, no campos
   semánticos. Group 1 = `abound, amorphous, austere, belie, capricious, cerebral…`. No hay
   agrupación semántica que respetar; reclusterizar desde cero era la única salida.
4. **Test de unicidad "automatizado" (spec Fase 3) vs. juicio manual.** Un script no puede
   decidir si un hermano también encaja en la oración: eso es criterio semántico. El repo lo
   resuelve con veredictos juzgados a mano y hasheados contra los hermanos, de modo que si
   cambia el grupo, el veredicto caduca. Hay 1038 vigentes.
5. **`VALIDACION.md` (spec) ya existe con otro nombre**: `reports/latest.txt` + `status.json`.

Discrepancia menor de documentación: `CLAUDE.md` dice que `tc_bank.json` vive en la raíz; está
en `data/`.

## 7. Orden de ataque propuesto

El criterio es **días de estudio ganados**, no completitud. Con 55 días, lo que decide tu score
es cuántas sesiones buenas hagas, no si el dataset llega a 100%.

**Bloque A — desbloquear el estudio (1 sesión de trabajo). Primero, sin discusión.**
Arreglar lo que hoy sabotea cada repaso: ocultar el nombre del grupo (#2), guardar la palabra
elegida al fallar (#5), interleaving duro (#3). Son cambios pequeños en `app/index.html`.
Al terminar esto **empiezas a estudiar los 1037 que ya existen**, mientras se construye el resto.

**Bloque B — el motor anti-interferencia (~4-6 días).**
Leitner 0·1·3·7·16, matriz de confusión → contrastivo forzado automático, dominado por pares,
sesión mixta y sesión de sábado. Es la razón de existir del proyecto y hoy no está.

**Bloque C — los 4 formatos que faltan (~3-4 días).**
Escribir, Equivalencia (SE), Contrastivo, Ordenar por intensidad. Equivalencia y el modo de
oración auténtica activan los 36 ítems TC/SE que hoy están muertos.

**Bloque D — cobertura, por lotes, en paralelo (continuo).**
Las 67 palabras libres, en lotes de 4–5 grupos con el flujo de `CLAUDE.md`. Va en paralelo
porque cada lote es independiente y cerrable.

**Bloque E — banco TC/SE de 36 a 150 (continuo, prioridad alta a partir de la semana 3).**
Es lo que más se parece al examen real. Cuando A–C estén listos, esto pasa a ser el trabajo
principal.

**Bloque F — cierre**: `README.md`, `BACKLOG.md`, push.

Razón del orden: A y B convierten la app en un instrumento de diagnóstico. Cada día que
estudias antes de B es un día cuyos errores no quedan registrados por par. La cobertura (D)
es el 6% final y son las palabras más difíciles: rinde menos por hora que arreglar el motor.

## 8. Decisiones tomadas (29 ago, checkpoint 1)

1. **Orden aprobado:** A → B → C, con D (cobertura) en paralelo por lotes y E (banco TC/SE)
   subiendo de prioridad desde la semana 3.
2. **Las 8 palabras apartadas:** no se fuerzan a un grupo. Van a una lista aparte donde **el
   grupo SÍ es la respuesta correcta** — que es como aparecen en Sentence Equivalence. Cobertura
   real objetivo: 99.3%, sin ítems ambiguos. *(Pendiente de construir: bloque C o D.)*
3. **Los cinco choques del §6:** se mantiene todo lo construido. Las definiciones siguen en
   inglés, el esquema `pos`+`axisPos` se queda, el clustering propio no se rehace, los veredictos
   siguen juzgándose a mano y los informes siguen en `reports/`. **No se rehace nada.**

## 9. Bloque A — hecho y verificado (29 ago)

Tres arreglos en `app/index.html`:

- **Nombre del grupo fuera de la pregunta.** El `eyebrow` ahora muestra solo el modo mientras
  la pregunta está abierta; `gNNN · nombre del campo` aparece al responder, con el feedback.
- **Matriz de confusión.** `record()` recibe la palabra elegida y la guarda en `store.pairs`
  como `"objetivo>elegida"`, dirigida. El formato plano anterior se **migra** al arrancar, así
  que el progreso ya guardado no se pierde.
- **Interleaving duro.** `pickQuestions()` da peso 0 al grupo del ítem anterior. Antes solo lo
  penalizaba ×0.25, así que sí podían salir dos seguidos.

**Verificación** (Chromium sobre un servidor local temporal, ambos modos):

| Comprobación | Resultado |
|---|---|
| Ítems ejercitados | 72 (5 rondas de Discriminar + 1 de Reconocer) |
| Grupo filtrado antes de responder | **0** |
| Grupo visible tras responder | 72/72 |
| Opciones ajenas al grupo | **0** — restricción 1 confirmada empíricamente |
| Grupos consecutivos repetidos | **0** |
| Pares de confusión registrados | 50 con dirección (`dirge>clangor`, `comity>decorum`…) |
| Progreso antiguo migrado | íntegro (`assuage {r:3,w:1}`, `mitigate {r:0,w:2}`) |

Ya puedes estudiar. Cada sesión que hagas desde ahora alimenta la matriz de pares que el
bloque B convierte en contrastivo forzado.

## 10. Bloque B — el motor anti-interferencia (29 ago)

**Decisión de alcance:** el formato **Contrastivo** se movió del bloque C al B. La restricción 6
dice que los pares confundidos entran automáticamente a contrastivo forzado; sin el formato no
hay a dónde entrar, así que el consumidor de la matriz viaja con la matriz. En C quedan los
otros tres: Escribir, Equivalencia y Ordenar por intensidad.

- **Leitner 0·1·3·7·16.** Cada palabra lleva `box` y `due`. Acertar sube una caja y aleja el
  repaso; fallar devuelve a la caja 0 y la palabra vuelve enseguida. `weightOf()` pondera por
  días de retraso, así que lo más vencido sale primero.
- **Contrastivo forzado.** Un par que fallaste queda **abierto** hasta que lo aciertes **dos
  veces** cara a cara, con solo esas dos palabras en pantalla. Los pares abiertos ocupan hasta
  un tercio del repaso del día y entran los primeros. El acierto abona las dos direcciones:
  lo que se resuelve es el par, no la palabra.
- **Dominado por pares (regla 7).** Un grupo se domina cuando **todas** sus palabras están en
  caja ≥3 **y** no le queda ningún par abierto. Nunca por promedio de aciertos.
- **Repaso del día y sesión de sábado.** El repaso mezcla formatos y grupos. Los sábados la
  portada cambia sola: 18 ítems, todo mezclado, sin filtrar por vencimiento.

**Un fallo encontrado al verificar, y corregido:** la cola de pares ordenaba por "más
confundido primero", así que un par con un acierto ya hecho se hundía bajo los recién fallados
y **no se cerraba nunca**. Ahora los pares a medio cerrar van delante. Sin ese arreglo, la
restricción 6 se cumplía de boquilla y ningún grupo llegaría jamás a dominado.

**Verificación** (Chromium, ~150 ítems ejercitados):

| Comprobación | Resultado |
|---|---|
| Leitner tras acertar | caja 0 → 1, `due` exactamente +1 día |
| Reparto de cajas tras 6 sesiones | box0: 71 · box1: 8 · box2: 23 |
| Contrastivos por sesión | 6 de 18, **siempre los primeros**, siempre 2 opciones |
| Cierre de pares | 6 → 12 → 12 → 18 → 18 → 24 a lo largo de 6 sesiones |
| **Regla 7** | 5 palabras en caja 4 con 100% de aciertos y 1 par abierto → **0 dominados**; cerrado ese par sin tocar el promedio → **1 dominado** |
| Repaso del día (forzando miércoles) | 12 ítems, 3 formatos mezclados, contrastivos primero |
| Sesión de sábado (hoy lo es) | 18 ítems, aparece sola en la portada |
| Grupos consecutivos repetidos | **0** en todas las sesiones |

## 11. Bloque C — los tres formatos que faltaban (30 ago)

- **Escribir.** La definición en inglés, el POS y el número de letras; la palabra la produces tú
  en un input. No abre pares de confusión: no elegiste una hermana, así que no hay par que abrir.
- **Equivalencia (SE).** Las **dos** opciones que dejan la oración con el mismo sentido, con el
  contador `1/2` y opciones que se marcan y desmarcan. Al responder muestra el `why` y el
  `trapNote` del banco.
- **Ordenar por intensidad.** Cuatro palabras del mismo grupo con `axisPos` distintos; se tocan
  de menor a mayor con los polos del eje a la vista. Al fallar abre **el par exacto que
  invertiste** — son hermanas, así que el contrastivo lo puede cerrar.

También: `data.json` ahora incluye el banco TC/SE (`tcBank`), que antes no llegaba a la app; y
se puede **abandonar una sesión a medias** ("salir" en la cabecera) — antes había que terminar
los 12 ítems o recargar. Lo encontré probando, no leyendo el código.

**Límite honesto:** Equivalencia vive de los **10 ítems SE** del banco. No se pueden fabricar
desde los grupos: cada `ej` está construido para que encaje una sola palabra, que es justo lo
contrario de lo que pide SE. Hasta que el banco crezca, el modo se agota en una sesión.

**Verificación** (Chromium, los tres formatos y el repaso mixto):

| Comprobación | Resultado |
|---|---|
| Escribir | acierto/fallo bien marcados, muestra la correcta al fallar, **0 pares creados** |
| Equivalencia | 6 opciones, contador 0/2→1/2, marca las 2 correctas y las 2 falladas, trampa visible |
| — su regla de pares | de 3 fallos abrió **1** par: el único entre hermanas del mismo grupo |
| Intensidad | 4 palabras del mismo grupo, polos visibles; al invertir dos abrió ese par exacto (`decry>denounce`) |
| Repaso del día | 12 ítems con **los 6 formatos** mezclados, 0 grupos consecutivos |
| Salir a media sesión | vuelve a la portada y conserva lo respondido |

## 12. Bloque E, primer lote — el banco TC/SE (30 ago)

Banco de **36 → 50 ítems**; los SE, que son los que alimentan Equivalencia, de **10 → 24**.

El criterio de este lote: **priorizar palabras sin grupo**. Los sinónimos verdaderos que ningún
cloze separa (`lassitude`/`torpor`, `penchant`/`predilection`, `propensity`/`proclivity`,
`exculpate`/`exonerate`, `impede`/`hinder`, `buttress`/`bolster`) son exactamente lo que SE
pide. Es la decisión 2 del checkpoint puesta a trabajar: donde el grupo falla, el banco entra.

**Efecto en cobertura:** 16 de las 75 palabras sin grupo ya se ejercitan en la app a través del
banco. Cobertura efectiva **1053/1112 (94.7%)**, aunque el informe siga diciendo 93.3% — ese
número solo cuenta grupos. Quedan **59** palabras que no aparecen todavía en ningún sitio.

Todas las opciones de los 14 ítems nuevos salen del dataset, así que cada ítem pone 6 palabras
reales en circulación, no solo las 2 correctas.

**Verificación:** `run_all.py` verde (R11 pasa), 0 problemas estructurales en los 14, y los 12
ítems que entraron en una sesión se renderizaron, se respondieron y mostraron su `why` y su
`trapNote`.

## 13. Bloques D y E — cobertura efectiva 100% (30 ago)

### D: agotado por la vía de los grupos, y se puede demostrar

Las 75 palabras sin grupo **no forman ningún campo nuevo de 5 del mismo POS**. Los ocho campos
que formarían están todos registrados como bloqueados en `docs/trampas.md`, cada uno con su
razón: inclinación (n), cansancio (n), librar de culpa (v), calmar (v), lo impropio (adj), fase
y tiempo (adj), efecto sobre el público (v) y personas reprobables (n) — esta última por faltar
dos personajes, no por defecto de diseño. Las 36 restantes son un cajón de sastre sin cinco del
mismo POS entre ellas.

Se descartó también **ampliar grupos existentes** (todos tienen sitio: 637 plazas libres). El
caso más prometedor, meter `miscreant`/`reprobate`/`libertine` en g120 «tipos difíciles de
tratar», rompe su eje: g120 va de *apartarse de todos* a *imponer su norma a todos*, y esos tres
no están en esa dimensión — infringen, que es otra cosa. Cada ampliación cuesta además rejuzgar
todos los cloze del grupo (el hash incluye a los hermanos) para colocar una o dos palabras.

### E: el banco absorbe lo que los grupos no pueden

**Banco de 50 → 109 ítems** (TC1=83, TC2=2, SE=24), en cuatro tandas. La clave: **TC1 no
necesita campo semántico ni POS uniforme** — la palabra es la respuesta única entre cinco
opciones impresas. Es el vehículo natural para una huérfana suelta.

| | |
|---|---|
| En grupos | 1037 |
| Solo en el banco | 75 |
| Sin aparecer en ningún sitio | **0** |
| **Cobertura efectiva** | **1112/1112 (100%)** |

El informe seguirá diciendo 93.3%: ese número solo cuenta grupos, y es correcto que lo haga.

Varios ítems aprovechan la ocasión para enseñar distinciones que `trampas.md` documenta y que
ningún grupo puede contener: `ennui` frente a `lassitude` (no querer / no poder), `coercion`
frente a `duress` (quien aprieta / quien firma), `thorough` frente a `exhaustive`, `competent`
frente a `proficient`, `cataclysmic` frente a sus dos sinónimos, `metaphorical` frente a
`figurative`, `ascribe` frente a `attribute`. La palabra ausente se nombra en el `trapNote`,
que es justo la disciplina que pide el examen.

### El modo «Leer la oración» (séptimo formato)

Al terminar las tandas, los 83 TC1 **no los mostraba nadie** — el mismo fallo que el banco
entero tenía antes del bloque C. Se añadió el modo: oración con un hueco, cinco opciones y, al
responder, la señal, la relación lógica y la pista subrayadas. Sin él, la cobertura del 100%
habría sido de papel.

**Verificación** (Chromium): 12 ítems TC ejercitados, todos con 5 opciones correctas,
acierto/fallo bien marcados y las tarjetas de señal y trampa presentes; y el repaso del día sale
con **siete formatos** mezclados (cara a cara, equivalencia, leer la oración, intensidad,
discriminar, reconocer, escribir) y 0 grupos consecutivos.
