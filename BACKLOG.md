# Backlog — lo que quedó fuera

Estado al 30 de agosto de 2026, con el proyecto funcionalmente terminado:
186 grupos, cobertura efectiva 1112/1112, banco de 150 ítems, 8 formatos y las
9 restricciones anti-interferencia cumplidas.

Lo de aquí abajo **no hace falta para estudiar**. Está ordenado por lo que de
verdad cambiaría el resultado del examen.

---

## Lo que más valdría la pena

### 1. Modo Simulacro
Una tanda cronometrada con la mezcla del examen real (unos 20 ítems TC/SE
seguidos, sin feedback hasta el final) y un informe al cerrar. Hoy el banco tiene
material de sobra —150 ítems— pero se estudia de uno en uno, con corrección
inmediata. **El examen no corrige sobre la marcha, y aguantar veinte ítems sin
saber cómo vas es una habilidad aparte.**

### 2. El progreso no viaja entre dispositivos
Vive en el `localStorage` de cada navegador: móvil y portátil llevan cajas
Leitner separadas. La salida barata es un botón de **exportar/importar** el
progreso como texto para pegarlo de un lado a otro. La cara sería un backend, que
este proyecto no quiere.

### 3. Un historial de las cuatro métricas
`PLAN.md` pide anotar a mano `vistas`, `pares abiertos`, `grupos dominados` y
`toca hoy` cada semana. La app podría guardar una foto semanal sola y pintar la
curva. Es el tipo de cosa que hace que uno siga apuntando.

---

## Contenido

### 4. Los tres campos descartados por eje falso
Documentados en `docs/trampas.md`, con sus palabras ya colocadas en el banco:
verbos de efecto sobre el público (`enchant`, `croon`, `invigorate`, `confound`,
`alienate`), adjetivos de lo impropio (`unseemly`, `indecorous`, `odious`,
`abject`, `laudable`) y adjetivos de fase y tiempo (`dwindling`, `convalescent`,
`recrudescent`, `valedictory`, `temporal`). **No se arreglan buscando una palabra
más**: el problema es que ningún eje ordena sus miembros. Si algún día se arman,
van `loose`, y un grupo `loose` exige que las cinco sean confundibles entre sí.

### 5. Grupos que podrían crecer
Los 186 tienen sitio (ninguno llega a 9; hay 637 plazas libres). Pero cada palabra
añadida **invalida los veredictos de todos los cloze del grupo** —el hash incluye
a los hermanos—, así que hay que rejuzgarlos a mano. Solo compensa si la palabra
encaja de verdad en el eje, no por rellenar.

### 6. Más TC de dos huecos
Son 10 de 150. En el examen pesan más que esa proporción, y son los que mejor
enseñan a leer la oración entera antes de elegir. Es el hueco más claro del banco.

### 7. TC3 (tres huecos)
El esquema y el validador ya los contemplan (`optionGroups` con tres columnas);
la app no los pinta. Aparecen poco en el examen: es lo último que haría.

---

## Técnico

### 8. `data.js` pesa 1.1 MB
Todo el dataset viaja en cada carga, incluidas las 186 fichas completas con
`disc`, `root` y `sense2`. En móvil con mala señal se nota la primera vez (luego
lo cachea). Se podría partir en un índice ligero y cargas por grupo, pero
complica el "un archivo sin servidor", que es lo que hace que esto funcione.

### 9. Las pruebas son ad hoc
Cada lote se verificó con un script de Playwright escrito para ese lote. No hay
una suite que se pueda volver a correr. Con el proyecto terminado importa menos,
pero si se retoma en serio, un puñado de pruebas fijas sobre los ocho formatos
evitaría los tropiezos que hubo (ítems que ningún modo consumía, opciones
conjugadas que no cruzaban con `words.json`).

### 10. El repo es público con el CSV de GregMat dentro
Se hizo público para poder usar GitHub Pages. Eso deja a la vista el CSV del curso
—material de pago de un tercero— y el correo del autor en el historial de
commits. Se puede sacar el CSV (la app no lo necesita: solo el pipeline) o volver
el repo privado y usar el archivo único de `build_standalone.py`.

---

## Decidido y cerrado — no volver sobre esto

- **`def` en inglés.** En español entrenaría traducción en vez de recuperación
  concepto→palabra.
- **Las 8 palabras apartadas** (`placate`/`mollify`/`appease`, `objurgation`,
  `phony`…) no se fuerzan a ningún grupo: son sinónimos verdaderos y viven en el
  banco, donde el grupo *sí* es la respuesta correcta.
- **La cobertura por grupos se queda en 93.3%.** El resto se estudia por el banco,
  y está bien así: el informe cuenta grupos, no palabras estudiables.
- **Un ítem nuevo no sirve si ningún modo lo consume.** Pasó tres veces. Al añadir
  material al banco, comprobar la app **es** parte de escribirlo.
