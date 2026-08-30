# Trampas conocidas — registro de lo que ya se intentó y falló

> Lo lee **quien vaya a escribir un grupo nuevo**, en el paso 1 del "Flujo de un lote"
> de `CLAUDE.md`. Vive fuera de `CLAUDE.md` porque ese archivo se carga en cada turno
> y esto solo hace falta al armar grupos.

Cada entrada es un campo que se intentó y no salió, o un par de palabras que no pueden
ser hermanas. **Antes de proponer un campo, busca aquí sus palabras.**

---

- **El hash del cloze incluye a los hermanos.** Si cambia la composición del grupo, los
  veredictos caducan y hay que volver a juzgar. Es a propósito: la unicidad depende de contra
  qué distractores compite la oración.
- **Sinónimos verdaderos no pueden ser hermanos.** `hamper`/`hinder`/`impede` no tienen firma
  colocacional que los separe: como hermanos no producen cloze únicos. Necesitan un grupo
  diseñado por dominios (`occlude`→conducto, `inhibit`→proceso, `circumscribe`→alcance).
- ~~Campo "presagiar" bloqueado~~ **resuelto en g148**: los 4 verbos proféticos (`presage`,
  `portend`, `forebode`, `prefigure`) llegaron a cinco al sumarles `antedate`, que no
  presagia nada — solo es anterior — y entra como polo de contraste del eje. `harbinger`
  sigue suelto: es sustantivo.
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
- **`prescient` y `prophetic` no se separan por «acertó antes».** «Her 1997 memo was eerily
  prescient» y «…was eerily prophetic» son las dos inglés corriente: cualquier cloze de texto
  releído después lo llenan las dos. Lo que sí separa en g132 es el **soporte**: prescient
  nombra una **capacidad de una persona que la lleva a actuar** — *___ enough to sell every
  bond* —, y prophetic un **texto de profecía todavía sin cumplir** — la secta que espera el
  año que nombra el último capítulo. Un libro no es *prescient enough to* nada, y una decisión
  de venta no es prophetic.
- **`tangible` se traga cualquier hueco de «no se nota».** *No ___ difference*, *no ___ change*,
  *no ___ effect*: «no tangible difference» es tan idiomático como con `discernible`, así que
  ese marco no discrimina. La salida en g134 fue llevar a `discernible` al **límite del ojo**
  — la orilla lejana en la niebla, «a darker grey against the grey» —, donde tangible queda
  fuera porque una orilla no se toca.
- **En verbos causales la estructura argumental es la distinción, no un atajo.** En g135
  `ensue` (intransitivo puro) y `render` (objeto + atributo) solo se separan por el marco que
  rigen, y sus cloze quedan registrados con `--basis grammatical`. Es honesto y está bien: la
  subcategorización *es* lo que hay que aprender de esos dos verbos. Distinto sería resolver
  el ítem por la categoría gramatical, que es lo que prohíbe la regla 2.
- **`condone`, `countenance` y `sanction` se pisan en «aprobar lo indebido».** Los tres llenan
  *the government would not ___ kidnapping*, así que el contenido moral no separa nada. Lo que
  sí separa en g136 es **el tiempo y el soporte**: `condone` mira **hacia atrás** — perdona una
  falta ya cometida y extingue el agravio (la *condonation* del divorcio antiguo); `countenance`
  respalda **lo que aún no ha ocurrido** y no admite delitos por objeto, solo ideas y planes;
  `sanction` deja **papel** — un órgano con potestad, por escrito, con condiciones. El cloze de
  countenance necesita además decir que el sujeto **no tiene poder** («no power to start it or
  stop it»), o `sanction` se cuela.
- **`brook` se cuela en cualquier hueco de «no soportar».** El primer cloze de `abide` en g136
  («could not ___ the sound of cutlery») lo llenaba igual de bien. Dos anclas lo excluyen a la
  vez: que el objeto sea **sensorial y menudo** (brook rige abstractos de oposición o demora —
  *no dissent*, *no delay*) y que quien lo sufre **no pueda impedirlo** (brook negado significa
  «no lo permitiría», y supone poder). Al revés, el cloze propio de brook se sostiene con un
  **sujeto que no es nadie**: un rescate, un plazo, una química que no admite demora.
- **`evasive` se cuela en «la reseña que no se moja».** El primer cloze de `tepid` en g139
  decía «nobody attacked the book and nobody recommended it», y eso es exactamente esquivar el
  veredicto. `tepid` necesita que **el juicio se haya dado entero** y solo falte calor —
  «polite, three paragraphs each, delivering their verdict in full» —, porque lo suyo es la
  temperatura, no la evasión.
- ~~Campo «codicia» bloqueado~~ **resuelto en g186**: los tres adjetivos de codicia (`avaricious`,
  `rapacious`, `acquisitive`) llegaron a cinco al sumarles los dos que **no desean nada**:
  `content` (renuncia expresa: podría haber más y no lo quiere) y `affluent` (solo informa de que
  hay mucho, y entra como polo de contraste, igual que `antedate` en g148). Eso convierte el campo
  en un eje real —**del que ya tiene bastante al que se lo arranca a otro**— porque los tres de
  arriba se ordenan por lo que hace la mano: `acquisitive` la extiende y **paga** (colecciones,
  no dinero), `avaricious` la cierra y **no suelta** (la casa sin calentar con la cuenta llena),
  `rapacious` la mete **en el bolsillo ajeno** (siempre hay víctima). `covet` sigue libre pero es
  verbo, y no existen en la lista *venal*, *mercenary* ni *covetous*.
- **`avaricious` y `rapacious` se separan por el hoarding, no por el dinero.** Los dos llenan
  *the tenants called him ___*: doblar la renta es igual de bien avaricia que rapiña. Lo que separa
  en g186 es **negar el atesoramiento** — *nothing was hoarded: the rents went out on horses as fast
  as they came in* —, porque avaricious exige que el dinero entre y no vuelva a salir; lo que queda
  entonces es la víctima (el campo de la viuda, las dos familias en la calle), que es lo propio de
  rapacious. Al revés, `avaricious` se aísla con *never took a penny that was not his own* (fuera
  rapacious) y con que **no compra nada**, solo retiene (fuera acquisitive).
- **De los tres sinónimos de desastre el segundo turno le tocó a `catastrophic` (g185).** `calamitous`
  está en g169 y `catastrophic` en g185; **`cataclysmic` sigue libre y no puede convivir con ninguno
  de los dos**. La regla vieja se mantiene: nunca más de uno de los tres en el mismo grupo.
- **`innocuous` se cuela en cualquier tarea fácil e indiscutida.** El primer cloze de `irksome` en g185
  («nothing was hard to work out and nothing was ever in dispute: nine boxes, the same nine figures,
  every Friday for eleven years») lo llenaba: una obligación que no cuesta nada y no perjudica a nadie
  *es* inofensiva. Lo que excluye a innocuous es **hacer que alguien pague el precio**: *the clerks drew
  lots every Friday to decide who would have to sit down with it*. innocuous significa que no pasa nada;
  irksome significa que alguien pone la paciencia.
- **`irksome` y `nettlesome` se separan por el aburrimiento, y hay que decirlo en las dos oraciones.**
  `irksome` es **una tarea fácil que hay que repetir** y cansa por repetirse (*duty, chore, restriction*);
  `nettlesome` es **un asunto que pincha y no se deja zanjar** (*issue, question*), y por eso su cloze
  necesita negar el tedio en voz alta — *nobody finds the seabed question dull — quite the opposite* —,
  o irksome se cuela. «A nettlesome chore» y «an irksome question» no son colocaciones corrientes.
- **`invasive` se ancla en su colocación técnica.** *Minimally ___* solo lo admite invasive: «minimally
  innocuous / irksome / catastrophic» no son inglés. Y la prueba de la oración tiene que ser **anatómica**
  (incisión de dos milímetros frente a tórax abierto), no de magnitud del daño, o catastrophic se acerca.
- **`conspire` no puede ser hermana de `collude`.** En el sentido humano son el mismo verbo: los
  tres licitadores que se reparten los contratos igual «colluded» que «conspired», y cualquier
  cloze de acuerdo secreto lo llenan las dos. Lo único propio de conspire es el **sujeto que no
  es nadie** — *the weather, the timetable and a burst main all conspired to…* —, y eso no basta
  para un hermano: g140 se cerró con cinco (`cluster`, `coalesce`, `amalgamate`, `collaborate`,
  `collude`) y `conspire` volvió al fondo libre, para un grupo futuro de «tramar» donde no esté
  collude.
- **`collude` ⊂ `collaborate` es par de inclusión**, y por eso admite cláusula de rechazo
  (regla 3): collude es collaborate más el secreto y el perjuicio a un tercero. Sin ella no se
  separan — «the three firms had collaborated for years, taking the contracts in turn» es inglés
  corriente. El cloze de g140 empieza negando la obra en común: *Nobody produced a single joint
  document: the two heads had simply ___d.*
- **`divulge` se cuela en cualquier hueco de insinuar si el hueco admite «that».** «She divulged
  that the department would not survive» es tan inglés como con `intimate`. Lo que lo excluye es
  decir que **no se dijo en voz alta** — *would not say it outright, but…* —, porque divulgar es
  decirlo. Al revés, un límite que **todavía no existe** («a boundary nobody had ever thought to
  fix») deja fuera a divulge del cloze de `delineate`: no se revela lo que nadie ha fijado.
- **`passable` se cuela en «no era justo pero servía».** El primer cloze de `expedient` en g142
  («The decision was fair to nobody, but it was ___») lo llenaba igual de bien. La salida es
  **nombrar al beneficiario**: *but for the minister it was ___*, más la lista de lo que ella
  ganó. passable no se dice relativo a nadie; expedient siempre le conviene a alguien.
- **`brevity` y `economy` solo se separan por lo que miden.** Brevity se mide con el **reloj o el
  recuento** (once minutos, nueve palabras); economy mide **el desperdicio**, y su colocación fija
  es *___ of means*. Un dibujo no tiene brevity — no transcurre —, y una ceremonia de once minutos
  no demuestra economy de nada.
- **`thorough` no puede ser hermana de `exhaustive`.** Cualquier cloze de «no dejó nada fuera»
  lo llenan las dos: *the appendix is thorough* y *the appendix is exhaustive* son las dos inglés
  corriente, y la distinción teórica — thorough es el **cuidado del que lo hace**, exhaustive es la
  **cobertura de lo hecho** — no sobrevive a ninguna oración natural. g145 se cerró poniendo
  `universal` en su lugar (propiedad de **lo afirmado**: vale en todos los casos, y por eso un
  catálogo no es universal ni un reflejo exhaustive). `thorough` sigue libre, pero para un grupo
  donde no esté exhaustive.
- **`ploy` se cuela en cualquier hueco de engaño con propósito.** El primer cloze de `feint` en g146
  («He won the round on ___s: a dropped shoulder, a shift of weight») lo llenaba igual de bien, y
  también lo llena la versión militar («two divisions moved north as a ___»). Lo que sí lo excluye es
  **igualar el golpe con la palabra**: *Half the blows he threw were never meant to land: they were
  ___s*. Un golpe puede ser un feint; no puede ser un ploy, que es un plan y no un movimiento.
- **`empirical`, `documentary` y `circumstantial` comparten «evidence».** Los tres llenan *the case
  rests on ___ evidence*, así que la palabra evidence no separa nada. Lo que separa en g144 es **de
  dónde sale el dato**: empirical lo **produce quien investiga** (seiscientas trampas vaciadas),
  documentary lo **encuentra escrito** y se puede enseñar (un recibo firmado), circumstantial **no
  existe como dato** — hay que inferirlo del barro y la llave. El cloze de documentary necesita además
  negar la inferencia explícitamente («nothing reconstructed or inferred») o circumstantial se cuela.
- **`archetype` y `paragon` se separan por el origen, no por la calidad.** Los dos son «el ejemplo
  que representa a los demás», y *the ___ of public thrift* lo llenan las dos. Lo que separa en g153
  es **quién fue primero**: archetype es el molde del que descienden las copias («every detective
  since is a variation on him»), paragon es el mejor ejemplar aunque haya llegado el último. El cloze
  de paragon necesita negar la prioridad expresamente — *nobody claimed she invented the style* — o
  archetype se cuela. Y el de intermediary necesita **no hablar por ninguna de las partes** («carried
  it in both directions and spoke for neither side»), o lo llena `proxy`.
- **`competent` y `proficient` no pueden ser hermanas.** «Competent in Mandarin» y «proficient in
  Mandarin» son las dos inglés corriente, y ni el nivel ni el marco las separan: competent es llegar
  al mínimo exigible, proficient es el nivel alcanzado con práctica, pero ninguna oración natural
  excluye a la otra. g154 se cerró con cinco que sí tienen dominio propio (`multifaceted` → caras de
  un asunto, `versatile` → usos sucesivos, `apt` → *an ___ pupil*, `resourceful` → persona en apuro,
  `ingenious` → lo discurrido). Las dos siguen libres, pero cada una para un grupo sin la otra —
  y `apt` tampoco puede convivir con `proficient`: *never had so proficient a pupil* también es inglés.
- **`metaphorical` y `figurative` son inseparables en «no literal».** Cualquier cloze de sentido no
  literal lo llenan las dos («in the figurative sense» / «in the metaphorical sense»), así que el
  campo del lenguaje figurado no se puede armar con las dos dentro. `figurative` sí tiene dominio
  propio en el sentido **artístico** — pintura que representa figuras reconocibles, opuesta a
  `abstract` —, y por ahí entra sin metaphorical al lado. `allegorical` (correspondencia sostenida
  en toda la obra) y `allusive` (remite a otro texto que el lector debe reconocer) sí discriminan.
- **`cataclysmic`, `catastrophic` y `calamitous` son tres sinónimos verdaderos.** Los tres llenan
  *the ___ failure of the scheme*: la escala, el daño y el registro coinciden. El campo «desastre
  adj» no se puede armar con más de uno de ellos dentro; `harrowing` (lo que se pasa mal viéndolo o
  viviéndolo) y `blighted` (arruinado poco a poco) sí tienen terreno propio, pero son solo dos.
- **El artículo vuelve a delatar en adjetivos, no solo en sustantivos.** El primer cloze de
  `ingenious` en g154 decía *an ___ arrangement of three brass cams*, y ese `an` reducía las cinco
  opciones a las dos que empiezan por vocal (`apt`, `ingenious`). Se reescribió con el hueco de
  atributo — *The design is frankly ___* —, que sirve para los cinco.
- **En g156 tres cloze se sostienen en la preposición y está bien.** `adhere to`, `deviate from` y
  `renege on` rigen marcos distintos, y eso *es* lo que hay que aprender de esos verbos (mismo caso
  que g135): quedan registrados con `--basis grammatical`. Los otros dos sí separan por contenido:
  `heed` pide un **aviso** como objeto directo y vive del contrafáctico («had anyone ___ed it»), y
  `flout` pide una **regla ajena rota en público**, delante de quien debería hacerla cumplir.
- **`distressed` se cuela en cualquier hueco de espanto si el que recibe la noticia sufre el daño.**
  El primer cloze de `aghast` en g157 («Told how much of the coast the storm had taken, she sat back
  ___») lo llenaba igual de bien: si a ella le duele la pérdida, está distressed. La salida fue poner
  a **alguien que no sufre el daño** — un topógrafo al que le leen la cifra — y hacerle **pedir que
  la repitan**: eso es incredulidad ante la magnitud, no sufrimiento. Regla práctica para `aghast`:
  quien lo siente tiene que ser **espectador**, no víctima, y nadie debe haber cometido injusticia
  (o entra `indignant`) ni haber repetido nada (o entra `exasperated`).
- **`gratify` se cuela en «no le des lo que pide».** El primer cloze de `coddle` en g159 («told the
  tutors not to ___ her: no extra time, no second reading») lo llenaba gratify, porque lo enumerado
  son justamente cosas que ella querría. Lo que excluye a gratify es **nombrar el daño de la
  blandura** — *a student who is never once allowed to struggle never learns how* —: gratify satisface
  un deseo y no perjudica a nadie; coddle sobreprotege y por eso se reprocha. Al revés, `gratify` se
  aísla poniéndole por objeto **la vanidad y no la persona**: *___ his vanity* no lo llenan ni
  enthrall ni coddle, que solo rigen personas.
- **Campo «librar de culpa» inviable de raíz**: solo quedan libres `exculpate` y `exonerate`, que
  además son sinónimos verdaderos («exonerated by the inquiry» / «exculpated by the inquiry»), y los
  dos verbos de achacar que podrían acompañarlos, `ascribe` y `attribute`, tampoco se separan entre
  sí. No llega a cinco ni sumándolos todos.
- **`accord`, `compromise` y `consensus` se pisan en «acuerdo».** Los tres llenan *the ___ held for a
  decade*, así que la duración y las partes no separan nada. Lo que separa en g161 son **tres negaciones
  explícitas**: el cloze de consensus dice que *nadie llegó con una exigencia* (sin exigencias no hay
  renuncia, y sin renuncia no hay compromise) y que *no se firmó nada* (sin papel no hay accord); el de
  compromise enumera **lo que cada lado soltó** y añade que *nunca se puso por escrito*; el de accord se
  apoya en el instrumento — *initialled … in Lisbon*, noventa páginas, anexos firmados por separado. Sin
  esas negaciones el ítem se resuelve a cara o cruz. `detente` es el fácil del grupo: no se firma, no se
  concede nada y **exige enemistad previa**, que ninguna de las otras tres supone.
- **`remote from` y `divorced from` comparten preposición.** *Remote from ordinary experience* es inglés
  corriente, así que un cloze de «alejado de la realidad» lo llenan las dos. Lo que excluye a remote es
  que los dos términos **estuvieran unidos y se hayan separado por un acto**: *pay has been entirely ___
  from performance: the two are calculated in different offices* — «pay is remote from performance» no es
  inglés, porque remote mide distancia de grado, no un vínculo cortado. Y `estranged` no compite ahí:
  solo rige personas.
- **`alacrity` se cuela en cualquier hueco de energía si hay algo que hacer.** El primer cloze de
  `vitality` en g163 («At eighty-one she had more ___ than the students: three flights of stairs, and she
  was the first one in the room») lo admitía: subir primero es prontitud en responder a una tarea. La
  salida fue quitar la tarea y dejar solo **el organismo a lo largo del tiempo** — jardinear hasta el
  anochecer, enfermar dos veces en diez años —, donde alacrity no tiene a qué responder. Al revés,
  alacrity se aísla **cronometrando el sí**: el abrigo puesto antes de que acabe la frase.
- **`complacent` se cuela en cualquier hueco de dejadez, y `lax` en cualquier hueco de descuido.**
  En g165 hubo que blindar los dos por separado. Lo que los separa es **de qué falla cada uno**:
  `lax` supone **una norma escrita y alguien encargado de aplicarla** (el fallo es de cumplimiento),
  `complacent` supone **una racha de éxito mal leída** (el fallo es de vigilancia). El cloze de
  complacent necesita negar la pereza — *the office worked as hard as ever* —, o entra lax; el de
  lax necesita decir que **sí veían el peligro** — *every inspector knew which sites were dangerous* —,
  o entra complacent. Y `ascetic` se aísla nombrando **comodidades entregadas y una orden religiosa
  como vara de medir**: sin eso, *a stern household* también es inglés corriente.
- **`ad hoc` y `makeshift` no se separan por «arreglo provisional».** *Government by makeshift
  committee* y *by ad hoc committee* son las dos inglés corriente. Lo que separa en g166 es qué mide
  cada una: `ad hoc` mide el **alcance** (vale para este caso y para ninguno más, aunque esté hecho
  con todo el rigor — por eso su cloze pone **tres jueces nombrados** para esa sola pregunta), y
  `makeshift` mide los **medios** (*not one object in the room made for the purpose*). El cloze de
  makeshift necesita además **negar el caso único** — el quirófano improvisado *took every case in
  the district* durante seis semanas —, o ad hoc se cuela. `auxiliary` es el fácil: es permanente y
  está revisado, y por eso ni es apaño ni es provisional.
- **`eclipse` se separa de `emulate` y de `transcend` por la víctima.** Un cloze de «llegó más lejos
  que su modelo» lo llenan las tres. `eclipse` exige que **al otro le pase algo**: la madre queda
  como nota a pie de página y el archivo se cataloga con el nombre de la hija. `transcend` no tiene
  víctima — rebasa **un marco** (*___ the genre*), no una persona —, y `emulate` iguala al modelo sin
  reducirlo. Al revés, `emulate` se aísla **negando la copia**: *not to copy its machinery … but to
  reach the same numbers by other means* deja fuera a mimic, que va a por la apariencia.
- **Los sustantivos de persona sí discriminan bien.** Al revés que los adjetivos de calma
  o los verbos de estorbar, cada tipo humano trae su escena propia (el martinet y la
  hebilla, el recluse y el correo sin recoger), y esa escena excluye sola a los hermanos.
  Quedan libres para un grupo futuro `miscreant`, `reprobate` y `libertine`, pero son solo
  tres: hacen falta dos personajes reprobables más.
- **De los tres sinónimos de desastre solo entra uno, y el que entra es `calamitous`.** g169 lo
  resolvió dejando fuera a `cataclysmic` y `catastrophic` (siguen libres, pero nunca juntos ni
  con calamitous). Lo que hace viable el campo es que los otros cuatro miden cosas distintas:
  `adverse` solo va **en contra** (su prueba en la oración es el antónimo *favourable*, y su
  objeto típico es un fallo o unas condiciones), `debilitating` **quita fuerzas sin destruir**,
  `harrowing` mide **el sufrimiento del que lo cuenta o lo oye** (*a ___ account*), y `blighted`
  arruina **despacio y dejando la cosa en pie**. El cloze de calamitous necesita decir que no
  quedó nada — *both firms had gone under, the name sold off for scrap* —, o debilitating se cuela.
- **`figurative` en el sentido no literal se traga cualquier cloze de `allegorical`.** La primera
  versión en g170 («The poem is ___ from the first line: the seven sisters are the seven
  virtues…») la llenaba figurative, porque la alegoría *es* lenguaje no literal: es un par de
  inclusión, `figurative` ⊃ `allegorical`. La salida es la cláusula de rechazo de la regla 3,
  negando la figura suelta: *Not one line of it is a metaphor standing on its own: the poem is
  ___ from first to last*. Por eso `figurative` entra en el grupo solo por su **sentido pictórico**
  (figuras reconocibles, opuesto a `abstract`), con el otro sentido registrado en `sense2`.
- **`aesthetic` y `abstract` chocan en la fórmula `purely ___`.** *A purely aesthetic objection* y
  *a purely abstract objection* son las dos inglés corriente. Lo que separa es qué acota cada una:
  aesthetic acota a **la belleza** (el cloze tiene que decir que lo seguro y lo barato no se
  discuten, *only that it was ugly*), abstract acota a **la teoría**, al caso que aún no tiene
  nombre ni fecha.
- **`empathetic` se cuela en cualquier hueco de tono amable.** El primer cloze de `conciliatory` en
  g171 («opened in a deliberately ___ register: an apology and an offer to drop two demands») lo
  llenaba igual de bien. Lo que excluye a empathetic es **negar que se hable del sentir ajeno**:
  *though he said nothing at all about what the strikers had been going through*. Y al revés,
  `egalitarian` se blinda contra `altruistic` añadiendo **voz igual**, no solo trabajo compartido
  (*no decision was taken until the last of the twenty had spoken*): repartir no es dar.
- **`coercion` y `duress` no pueden ser hermanas.** Los dos llenan *a signature given under ___ binds nobody*: «under coercion» es inglés corriente. Lo propio de coercion es **el lado del que aprieta** (*govern by ___* — ejércitos, cárceles, alguaciles) y lo de duress **el lado del que firma** (*under ___*, *plead ___*), pero ninguna oración de consentimiento viciado — que es donde viven las dos — excluye a la otra. g180 se cerró con `duress`, y `coercion` volvió al fondo libre para un grupo de «forzar» donde no esté duress.
- **`amend` se cuela en cualquier hueco de trámite cuyo objeto sea un papel.** El primer cloze de `expedite` en g177 («hired purely to ___ the applications already in the queue») lo admitía: enmendar solicitudes es inglés corriente. La salida es **negar el cambio de letra** — *not a word in any of them was altered* —, porque expedite solo mueve el reloj y no toca el texto.
- **`recourse` se cuela en «margen» si el hueco no dice para qué.** *A head teacher has more ___ than in any system in Europe* lo llenan las dos (más instancias a las que acudir / más libertad). Lo que separa es el infinitivo: *more ___ to decide for herself* deja fuera a recourse, que no se ejerce para decidir sino para reclamar cuando lo normal ya falló.
- **`suspect` (adj) se cuela en cualquier reproche a un informe.** El cloze de `partial` en g179 necesitó tres negaciones seguidas: *not a sentence in it is untrue* (fuera suspect y fallible), *keeps his own opinions out of it entirely* (fuera subjective), y solo entonces queda lo único que falla — que se oyó a una parte y no a la otra. Al revés, `fallible` se aísla con *as anyone is at that hour*: lo que es de todos no es sospechoso de nadie.
- **`mettlesome` solo se separa de `impetuous` quitando el acto.** Cualquier escena en que el animal o el joven **haga** algo (el potro que se lanza a la cuesta) la llena impetuous, porque es exactamente un arranque. La salida en g178 fue medir el brío por lo que **no lo apagó** — dos inviernos de mala ración, y la yegua sigue saliendo al trote con la cabeza alta —: ahí no hay acto precipitado que reprochar, solo temple que aguanta.
- **`tortuous` va en sentido figurado y `sinuous` en literal.** Los dos describen curvas, pero
  tortuous **reprocha** las vueltas (un trámite, un razonamiento) y sinuous **admira** la
  continuidad (un río, un brazo que baila): el cloze de sinuous se sostiene con *a single line,
  without a break or an angle*. Para `intertwined` hace falta **consecuencia mutua entre dos
  cosas** — *taking out the dead one would have killed the other* —, o tortuous se cuela: lo
  enredado son dos recorridos, lo tortuoso es uno solo.

- **`infelicity` se cuela en cualquier metedura de pata que sea verbal.** El primer cloze de `gaffe`
  en g173 («the minister congratulated the widow on her husband's promotion») lo llenaba: una frase
  desafortunada dicha en voz alta *es* una infelicity. La salida fue quitarle las palabras al error —
  **la corona depositada en el monumento equivocado** —: sin frase no hay infelicity, y quedan las
  cámaras, que es lo propio de gaffe. Al revés, `infelicity` se aísla con su colocación fija,
  *an ___ of phrasing*, que ninguna hermana admite.
- **`frailty` se cuela en cualquier falta pequeña si no se la llama falta.** El primer cloze de
  `peccadillo` en g173 («the missing case of wine looks like a ___: nobody was poorer for it») lo
  admitía, porque «su una debilidad era el vino» es lectura natural. Lo que excluye a frailty es
  **nombrar el acto como acto**: *is a ___: an offence, certainly, but not one anybody thought worth
  raising*. frailty es disposición y no se comete; peccadillo se fecha y se cuenta.
- **`squander` se cuela en cualquier hueco de dinero desviado.** El primer cloze de `cloak` en g176
  («the payments were ___ed in a charitable trust») lo admitía en la lectura «malgastados en una
  fundación». La salida es **negar el daño y nombrar el fin del disfraz**: *nothing was denied and
  nothing was destroyed … so that the name of the man receiving them appeared on no document*.
  cloak no quita ni gasta: solo tapa.
- **Campo «provecho» resuelto por lo que rinde cada uno (g174).** `lucrative` solo mide **dinero
  contable** y su cloze tiene que cancelar el producto («no book, no students, no idea»), `fruitful`
  solo mide **obra** y el suyo tiene que cancelar el ingreso («nobody was paid a penny»). Sin esas dos
  negaciones cruzadas el ítem se resuelve a cara o cruz. `conducive` es el fácil: rige **`to` + el
  resultado que favorece**, marco que ninguna hermana admite — queda registrado con `--basis grammatical`.

- **`remarkable` se cuela en cualquier escena rara, porque «raro» es exactamente «digno de mención».**
  El primer cloze de `disconcerting` en g181 («She lost her thread for a moment: it is faintly ___ to be
  greeted by name … by a man one has never met») lo llenaba: que un desconocido sepa tu nombre es de las
  cosas que se cuentan luego. Lo que excluye a remarkable es **negarle el mérito de mención** — *the
  explanation is dull enough … nothing in it worth repeating to anybody afterwards* —, y entonces queda
  lo único que sigue en pie: que a ella se le fue el hilo. Regla práctica: `remarkable` se mata diciendo
  que la cosa no se cuenta; `disconcerting` se sostiene con su colocación, *faintly ___*.
- **`cathartic` se cuela en cualquier esfuerzo físico.** «Rowing is cathartic» es inglés corriente: el
  ejercicio como desahogo. El cloze de `exhilarating` en g181 necesita cancelar la carga previa —
  *there was nothing on her mind to be worked off* —, porque catarsis exige **algo acumulado que sacar**;
  sin eso, lo que queda es el cuerpo levantado y las ganas de repetir, que es lo propio de exhilarating.
  Al revés, `cathartic` se aísla con *in the older sense* + llanto sostenido y alivio al salir.
- **`sensational` no puede ser hermana de `exhilarating`.** En registro corriente significa «espectacular»
  (*the descent was sensational*), así que cualquier cloze de experiencia intensa lo llenan las dos. g181 se
  cerró sin ella; sigue libre, pero para un grupo de **prensa y exageración**, donde su sentido GRE — lo
  redactado para excitar al lector — sí tiene terreno propio.
- **`keen` e `inquisitive` se separan por la preposición y por el objeto del deseo.** keen quiere **hacer**
  y rige *___ to* + infinitivo o *___ on* + actividad; inquisitive quiere **enterarse** y rige *___ about* +
  gente o asuntos ajenos. «Keen about other people» no es inglés corriente, y ahí es donde se corta: el cloze
  de inquisitive de g182 pone preguntas sobre lo que pagaron los vecinos, no sobre lo que ella va a estudiar.
- **`improvise` no llena un hueco cuyo objeto sea `the term`.** Es lo que separa a `coin` en g183: se
  improvisa **una ejecución entera** (los cincuenta minutos que quedaban de charla), y se acuña **una sola
  palabra que además queda** — *it now appears in the statutes of forty states*. Lo improvisado no dura;
  lo acuñado circula como la moneda de la que viene la imagen.
- **`conspire` se aísla con el sujeto que no es nadie, y `premeditate` con el acto por objeto directo.**
  En g183 conviven sin pisarse porque rigen marcos distintos: *a burst main, a rail strike and the wettest
  June ___d to* (conspire, sujetos que no son personas, siempre *to* + infinitivo) frente a *whether he ___d
  the killing* (premeditate, objeto directo y una sola persona que planea). Nadie «conspira un asesinato».
  El de `prime` también vive del marco — objeto persona y pasiva, *had been ___d* — y queda registrado con
  `--basis grammatical`.
- **Una diferencia con causa explicada ya no es una paradoja.** En g184 el cloze de `divergent` decía al
  principio que las dos encuestas se hicieron la misma semana y preguntaron lo mismo «y aun así» daban 31 y
  58: ese *yet* invita a `paradoxical`. La salida fue **dar la causa** — *the samples came from different
  registers* —: con la contradicción deshecha solo queda la distancia entre dos cifras, que es divergent.
  Al revés, `paradoxical` exige **una sola relación que va al revés de lo esperado** y está documentada.

- **Tres campos descartados en el lote de g185–g186 por eje falso, no por falta de palabras.** Quedan
  anotados para no volver a intentarlos igual:
  - **Verbos de efecto sobre el público** (`enchant`, `croon`, `invigorate`, `confound`, `alienate`).
    El eje «atraer → expulsar» no ordena la mitad de abajo: mover `croon` treinta puntos, por encima o
    por debajo de `invigorate`, no cambia nada. Son cinco verbos del mismo campo sin dimensión que los
    gradúe; si se arman, van `loose`.
  - **Adjetivos de lo impropio** (`unseemly`, `indecorous`, `odious`, `abject`, `laudable`). Dos
    problemas a la vez: `unseemly`/`indecorous` son casi sinónimos (*unseemly haste* / *indecorous
    haste*), y `abject` no está en la dimensión del reproche — describe la degradación del propio
    sujeto (*abject apology*, *abject poverty*), no lo que merece.
  - **Adjetivos de fase y tiempo** (`dwindling`, `convalescent`, `recrudescent`, `valedictory`,
    `temporal`). El campo es un cajón de sastre: nadie confunde `valedictory` con `dwindling`, así que
    ni siquiera como distractores se sostienen. Un grupo `loose` necesita que las cinco sean confundibles
    entre sí; que compartan tema no basta.

---

## Cierre del backfill por grupos (30 ago 2026)

- **El bloque D se dio por agotado, y la salida es el banco.** Las 75 palabras que quedaron sin
  grupo no forman ningún campo nuevo de 5 del mismo POS: los ocho que formarían están todos
  arriba, cada uno con su razón. Las 36 restantes son un cajón de sastre.
- **Ampliar un grupo existente casi nunca compensa.** Hay 637 plazas libres (ningún grupo llega
  a 9), pero cada palabra añadida invalida los veredictos de **todos** los cloze del grupo,
  porque el hash incluye a los hermanos. Y el eje manda: meter `miscreant`, `reprobate` y
  `libertine` en g120 parecía natural por ser tipos humanos, pero el eje de g120 va de
  **apartarse de todos** a **imponer su norma a todos**, y esos tres no están en esa dimensión
  — infringen. Compartir «tema» no basta, igual que en los grupos `loose`.
- **Regla nueva: si una palabra no cabe en un grupo, escribe un ítem del banco, no fuerces un
  grupo.** Sinónimos verdaderos → **SE** (las dos son la respuesta, que es como aparecen en el
  examen). Huérfana suelta, sin pareja ni campo → **TC1**, que no necesita campo semántico ni
  POS uniforme: basta con cinco opciones impresas donde solo una encaje. Así se cerró la
  cobertura efectiva al 100% sin fabricar un solo ítem ambiguo.
- **El `trapNote` es donde viven las distinciones que ningún grupo puede contener.** `ennui` vs
  `lassitude` (no querer / no poder), `coercion` vs `duress` (quien aprieta / quien firma),
  `thorough` vs `exhaustive`, `competent` vs `proficient`, `cataclysmic` vs sus dos sinónimos,
  `metaphorical` vs `figurative`, `ascribe` vs `attribute`. Se nombra la palabra **ausente** de
  las opciones y se explica por qué habría valido: es exactamente la disciplina del examen.
- **Un ítem nuevo no sirve de nada si ningún modo lo consume.** Pasó dos veces: el banco entero
  estuvo fuera de `data.json` hasta el bloque C, y los 83 TC1 no los mostraba nadie hasta que se
  añadió el modo «Leer la oración». Al añadir material al banco, comprueba que la app lo usa.
