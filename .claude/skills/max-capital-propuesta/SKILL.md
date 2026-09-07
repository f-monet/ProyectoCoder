---
name: max-capital-propuesta
description: >-
  Genera propuestas de inversión de Max Capital en PDF on-brand, en tres formatos:
  one-pager (una hoja, para clientes poco sofisticados), deck 16:9 (presentación
  completa) y documento largo (comités de inversión y mandatos institucionales).
  Usá esta skill siempre que un asesor de banca privada / wealth management quiera
  armar, actualizar o rehacer una propuesta para un cliente, aunque no diga la
  palabra "propuesta": alcanza con que traiga una cartera sugerida, un asset
  allocation, una hoja de cálculo con instrumentos y montos, la posición actual de
  un cliente, o pida "algo para mandarle al cliente", "la presentación de la
  cartera", "el PDF para la reunión". También cuando pida analizar una cartera
  vigente, recomendar qué comprar y qué vender, o armar un canje de un instrumento
  por otro. El asesor puede sumar fact sheets,
  carteras modelo, la posición actual o cualquier otro contexto del cliente: la
  skill los interpreta y produce el PDF final sin que nadie toque el diseño.
  — v1.2 (06/09/2026)
---

# Max Capital — Propuestas de Inversión

**Versión 1.2 · 6 de septiembre de 2026**

Si el asesor pregunta qué versión tiene instalada, es esta. La última siempre
está en la carpeta de Drive del equipo.

**Qué cambió desde la v1.1**, todo salido de armar el deck de Jimena Laino:

- Capítulo **`trades`** para movimientos emparejados — sale este bono, entra este
  otro. Es el hermano de `cartera_actual`, que sigue siendo el formato del
  rebalanceo por estrategia. Ver criterio 63.
- El **criterio 53 se reescribió por intención**: la proyección de retiro va si
  entra dinero nuevo, no según cómo se llame el caso. La excepción anterior
  ("no va en un reposicionamiento") se aplicó mal mirando la etiqueta.
- Campo **`orden`** en el bloque `acciones`, para elegir la secuencia de las
  columnas: en un rebalanceo se vende primero.
- **Tres bugs arreglados**: los puntos de una etiqueta de gráfico se convertían en
  comas ("EE.UU." salía "EE,UU,"); el `nota` de `instrumentos` se aceptaba y no se
  dibujaba; `subtotales` emitía subtotal para grupos de una sola fila.
- Las tarjetas de **`deltas`** dejan de repartirse el ancho cuando hay menos de
  tres: miden lo que mide su contenido y el sobrante queda vacío.
- Criterios nuevos: **63** (trade ≠ rebalanceo), **64** (dos números que contestan
  lo mismo), **65** (un instrumento no se confirma de memoria), **66** (sin puntos
  en las etiquetas de gráficos), **67** (cuando hay dos carteras, cada slide dice
  cuál muestra).

Convierte lo que traiga el asesor en un PDF terminado y on-brand. La división de
trabajo es deliberada: **el asesor y vos discuten el contenido; el script hace
todo el diseño.** Nadie elige colores, tipografías ni layout, y por eso dos
asesores distintos producen propuestas que se ven como la misma casa.

El proceso tiene un solo punto de traducción: leés lo que haya (una planilla, un
PDF, notas sueltas, un audio transcripto) y lo escribís como un JSON de propuesta.
De ahí en adelante es determinista.

```
inputs libres  →  propuesta.json  →  generate_propuesta.py  →  PDF
  (interpretás vos)                        (diseño fijo)
```

## Los tres formatos

Elegí según **quién lo va a leer**, no según cuánta información haya.

| Formato | Qué es | Cuándo |
|---|---|---|
| `onepager` | Una hoja A4 apaisada: KPIs, tabla de cartera, distribuciones | Cliente que quiere ver todo de un vistazo. Poco sofisticado, o una reunión corta. Es el default cuando el asesor dice "algo simple" |
| `deck` | Presentación 16:9, tantas slides como capítulos | Reunión de presentación. Permite argumentar, mostrar la cartera actual, explicar instrumento por instrumento |
| `documento` | A4 vertical, secciones numeradas, prosa | Comités de inversión, mandatos institucionales, licitaciones, IPS. Cuando la propuesta se va a leer sin nadie que la presente |

Si el asesor no lo dice y no se deduce del contexto, preguntá. Es una pregunta
barata y cambia todo el output. Podés generar más de uno del mismo JSON: es común
que a una reunión vaya el deck y quede el one-pager como resumen.

## El flujo

### 0. Preguntá quiénes firman

Antes de nada, **preguntale al asesor quiénes van en los datos de contacto**. Se
trabaja en dupla y el cliente tiene que poder escribirle a los dos; no lo
deduzcas de quién te está hablando. El directorio del equipo está en
[`reference/equipo.md`](reference/equipo.md).

### 1. Juntá y leé todo el input

El asesor puede subir cualquier cosa: la planilla de la cartera, un fact sheet, la
posición actual del cliente, una cartera modelo, el IPS, notas de la reunión.
Leelo todo antes de escribir nada — el fact sheet de un fondo es lo que te permite
escribir qué hace ese fondo dentro de la cartera, y la posición actual es lo que
convierte una propuesta genérica en una recomendación.

Si falta el dato central (la cartera sugerida, o los montos), pedilo. No lo
inventes.

### 2. Revisá la oferta antes de armar la cartera

**[`reference/oferta.md`](reference/oferta.md) tiene la política comercial del
equipo**, y conviene leerla antes de escribir la cartera sugerida.

Lo esencial: en **banca privada** se propone bajo esquema de honorario de
administración, no de comisión por transacción. Hay tres instrumentos que van en
toda propuesta salvo que el caso lo desaconseje —FCI Max Renta Fija Dólares,
cartera de CEDEARs de ETFs y notas estructuradas desde USD 250.000— y otros que
suman cuando el caso lo permite.

Si el asesor te trae una cartera armada sin ningún vehículo administrado,
**decíselo**: la comodidad empuja al modelo de trading y para banca privada eso
alinea mal los incentivos. No lo cambies por tu cuenta — planteáselo y que
decida él.

En propuestas para **empresas** la lógica es otra y se evalúa caso por caso:
preguntá antes de asumir.

Ese archivo también trae material listo para usar: el argumento de cuentas
administradas, el esquema de bolsillos de liquidez y los seis pilares del
servicio para el capítulo `forma_de_trabajo`.

### 3. Decidí los capítulos

No hay plantilla fija. Elegí los capítulos que el caso pide y ordenalos como los
contarías en la reunión. El catálogo completo está en
[`reference/capitulos.md`](reference/capitulos.md) — leelo antes de armar el JSON
la primera vez.

**Y leé también [`reference/criterios.md`](reference/criterios.md).** Son los
criterios del equipo, cada uno con el porqué y el caso del que salió. Casi todos
corrigen cosas que sólo se descubren mirando un PDF terminado, y varios
corrigen errores que ya se cometieron una vez.

Un orden que funciona bien y podés variar:

1. `perfil` — quién es el cliente, para que confirme o corrija
2. `kpis` — los números que resumen la propuesta
3. `proyeccion` — a dónde llega el capital, si hay horizonte largo
4. `glidepath` — cómo evoluciona la asignación con los años
5. `forma_de_trabajo` — cómo es la relación (si el cliente es nuevo)
6. `cartera_actual` — la posición vigente y qué comprar/vender (si la hay)
7. `trades` — los canjes, si el argumento es comparar un instrumento con otro
8. `cartera_sugerida` — el detalle de la cartera propuesta
9. `distribuciones` — cómo queda repartida
10. `instrumentos` — qué hace cada componente
11. `texto` — por qué esta cartera y no otra
12. `cierre`

Para un cliente nuevo, saltea `cartera_actual`. Para una revisión de cartera
vigente, `cartera_actual` es el capítulo más importante y `forma_de_trabajo`
probablemente sobre. **Y elegí bien entre `cartera_actual` y `trades`**: el
primero justifica cada posición contra el mandato, el segundo compara el
instrumento que sale con el que entra. Ver criterio 63. Un deck de 6 a 10 slides es el rango cómodo.

### 4. Escribí el JSON

El contrato está en [`reference/esquema.md`](reference/esquema.md). Hay un ejemplo
completo, que usa todos los tipos de capítulo, en
[`ejemplos/propuesta_ejemplo.json`](ejemplos/propuesta_ejemplo.json) — la forma más
rápida de arrancar es copiarlo y borrar lo que no aplique.

Dos cosas que conviene tener presentes al escribirlo:

- **Los montos y porcentajes van como texto ya formateado** (`"USD 20.000"`,
  `"6,4%"`). El renderer imprime lo que le des. La excepción son los `valor` de los
  gráficos, que van como número porque se normalizan sobre el total.
- **Ningún campo es obligatorio salvo `cliente` y `capitulos`.** Lo que falta no se
  dibuja. Es mejor omitir un campo que rellenarlo con un placeholder.

### 5. Validá

```bash
python scripts/generate_propuesta.py --json propuesta.json --validar
```

Es instantáneo y detecta tablas vacías, gráficos sin datos y filas descuadradas.
Corrigiendo acá te ahorrás mirar un PDF con una tabla en blanco.

### 6. Generá el PDF

```bash
python scripts/generate_propuesta.py --json propuesta.json --formato deck --out "Propuesta - <Cliente>.pdf"
```

`--formato` es `deck`, `onepager` o `documento`. Presentá el PDF al asesor con la
herramienta de entrega de archivos que tengas disponible.

Dependencias: `playwright` (con chromium). Si falla el navegador:
`python -m playwright install chromium`.

## Cómo iterar con el asesor

Una propuesta no sale bien la primera vez: sale bien a la tercera o la cuarta.
Lo que decide cuánto cuesta llegar ahí es cómo se organizan las vueltas.

**Pedí los cambios de una slide todos juntos.** Cada vuelta cuesta una
regeneración y una revisión; cinco cambios en un mensaje salen en un ciclo y de
a uno salen en cinco. Si el asesor te manda uno solo y sospechás que hay más,
preguntale si quiere revisar la slide entera antes de que regeneres.

**Referite a las slides por el título, no por el número.** "La de *A dónde van
los fondos*" es inequívoco; "la slide 8" no lo es, porque hay dos numeraciones
que no coinciden: la del badge y la de la página del PDF. Ver criterio 55.

**Mostrá sólo lo que cambió.** Después de editar, la slide afectada alcanza: no
hace falta que el asesor recorra el PDF entero para ver una corrección.

### Ofrecele editar el JSON directamente

**Cuando el asesor te pida varios cambios de redacción, contale que puede editar
el JSON él mismo.** La mayoría no sabe que esa opción existe y es la que más
tiempo les ahorra: el JSON es texto plano y legible, así que puede abrirlo,
escribir las frases exactamente como las quiere y pedirte que regeneres. Se
saltea el paso de explicarte qué quiere decir, que es donde se pierden las
vueltas.

Ofrecelo una vez, sin insistir, y sólo cuando aplique — sirve para redacción,
no para cambios de layout ni de datos, donde hay que medir o recalcular.

### Dictar desde el celular

Si el asesor conecta Claude Code al remoto, puede dictarte los cambios desde el
teléfono mientras mira el PDF en la computadora: **un dispositivo para ver y
otro para hablar**. Para revisar un deck y corregirlo sobre la marcha es bastante
más cómodo que alternar entre ventanas en la misma pantalla.

Vale la pena mencionarlo si ves que el asesor está iterando mucho sobre un mismo
documento.

## Cómo escribir el contenido

El diseño está resuelto; lo que decide si la propuesta sirve es el texto. Tres
cosas marcan la diferencia:

**Escribí para este cliente, no para cualquiera.** El tono de `forma_de_trabajo`
para una tesorería corporativa que necesita cash management no es el mismo que
para un family office que pregunta por custodia. Usá el nombre del cliente y el
vocabulario que el asesor usó en sus notas.

**En `instrumentos`, explicá el rol, no la ficha.** El fact sheet dice qué es el
instrumento; el cliente necesita saber qué hace *en su cartera*. "Es el colchón de
liquidez: cubre el rescate de 48 horas sin desarmar ninguna otra posición" sirve;
"fondo money market que invierte en instrumentos de corto plazo" es la categoría
repetida. Lo mismo con los datos: si el argumento es la liquidez, mostrá el plazo,
no el desvío estándar.

**En `cartera_actual`, el porqué es el contenido.** Una lista de qué comprar y qué
vender sin razones es una orden, no una recomendación. Una frase concreta por
posición sobre qué gana el cliente con ese movimiento.

## Reglas que no conviene romper

Las de acá son las que más caro salen. El resto está en
[`reference/criterios.md`](reference/criterios.md).

**Nada entra al PDF si no lo pidió el asesor.** Esta es la primera y la que no
tiene excepciones. Trabajando sobre una cartera vas a encontrar cosas que el
asesor no te pidió mirar: una concentración por emisor, un costo alto, una
posición que no cierra. **Eso se le dice a él, en el chat, y ahí termina tu
parte.** No va a la propuesta, ni como columna, ni como nota al pie, ni como
"tema de la próxima conversación".

El asesor es quien decide qué ve el cliente y con qué palabras. Una línea que
dice "esto la propuesta no lo resuelve" le traslada al cliente un problema que
la casa no eligió plantearle, en un documento firmado, que queda y se reenvía.
Aunque el hallazgo sea correcto —sobre todo si es correcto— la decisión de
contarlo y cómo contarlo no es tuya.

Y no existe la versión suave: no hay forma de redactar bien una limitación que
el asesor no aprobó. Si te parece importante, decíselo y esperá. Ver criterio
42.

**Nada de tensiones, dilemas ni preguntas incómodas.** Prohibido escribir en una
propuesta cosas como "lo que esta propuesta no resuelve", "la tensión que hay
que definir", "la pregunta incómoda es", "el punto débil de este esquema" o "hay
que reconocer que". Ni con esas palabras ni con otras.

Es un vicio de conversación: plantear tensiones y contradicciones genera diálogo
con quien te está hablando y suena a honestidad intelectual. **En un documento de
venta es autosabotaje.** El cliente no está discutiendo con vos, está evaluando
una recomendación de su asesor. Los riesgos se exponen con datos —cuánto cayó,
cuánto tardó en recuperar— y no como dilemas irresueltos que le quedan a él.
Ver criterio 46.

**De los costos se habla en positivo, o no se habla.** Si el costo entra en la
propuesta es para decir lo que el cliente gana: que no hay arancel de entrada ni
de salida, que el rebalanceo no cuesta, que el marco impositivo genera
eficiencias. Nunca como advertencia, nunca erosionando los números propios. El
foco es el beneficio del cliente y el valor del servicio. Ver criterio 47.

**No inventes nada.** Ni números ni datos de la casa: montos, rendimientos, TIR,
ponderaciones, URLs, leyendas, nombres de producto, teléfonos. Todo tiene que
salir de algo que el asesor aportó. Si falta, preguntá o dejá el campo afuera —
lo que no está, no se dibuja. Un PDF con la identidad de la casa y una cifra
inventada es peor que un PDF incompleto: parece verificado.

**Lo que la casa hace, cubre o cobra, preguntalo.** El alcance del servicio, la
cobertura y los costos de Max Capital no se deducen del material: del fact sheet
de un fondo no sale qué servicios presta la firma. Escribir "esto no lo
contemplamos" sobre algo que la casa sí hace es peor que no decir nada, porque el
cliente lo lee como política institucional. Ver criterio 34.

**El logotipo es el archivo oficial, sin modificar.** `logo_negativo.png` sobre
fondo oscuro, `logo_positivo.png` sobre fondo claro. No se recolorea, no se le
baja la opacidad y no se le recortan los márgenes, que son el área de resguardo
de la marca.

**Verificá los gráficos contra el texto.** Si un porcentaje del gráfico no
coincide con el mismo dato escrito en la propuesta, hay un error de
normalización. Y en un apilado al 100%, todas las barras miden lo mismo:
medilas, no las mires.

**Marcá las estimaciones como estimaciones.** Los rendimientos esperados son
supuestos, no promesas. El disclaimer institucional va siempre (lo pone el script
solo), pero cuando una slide muestra rendimientos proyectados, agregá la
advertencia en su `nota` — donde el cliente la lee, no sólo al final.

**Cuidá los datos del cliente.** No pongas números de cuenta, CUIT, documentos ni
datos de contacto del comitente en el JSON ni en el nombre del archivo. El nombre
del cliente en la portada alcanza. Si el asesor quiere una versión anonimizada
para uso interno, poné un identificador en `cliente.nombre` y listo.

**Revisá los totales.** Si la suma de los montos no coincide con el capital
inicial, o las ponderaciones no dan 100%, avisale al asesor antes de generar. El
script no lo chequea: es una decisión de negocio, no de formato, y a veces la
diferencia es intencional.

## Ajustar el diseño

Los criterios del equipo están centralizados en el diccionario `CONFIG`, al inicio
de `scripts/generate_propuesta.py`. Cambiar un criterio es cambiar una línea:
cuántas filas entran por slide, la paleta de los gráficos, el disclaimer, la
leyenda regulatoria del pie.

La capa visual son tres hojas de estilo en `assets/`: `base.css` (tokens de marca y
primitivas compartidas), más `deck.css`, `onepager.css` y `documento.css`. Los
tokens de `:root` en `base.css` están alineados con los de la skill
`max-capital-factsheet`, para que un fact sheet y una propuesta del mismo cliente
se lean como la misma familia.

Para editar el diseño visualmente:

```bash
python scripts/generate_propuesta.py --json propuesta.json --formato deck --design-html preview.html
```

Exporta el HTML con los datos reales. Editalo en Claude Design y pegá el CSS
actualizado de vuelta en el archivo de `assets/` que corresponda (todo menos las
reglas `@font-face`, que se generan solas). La próxima generación usa el diseño
nuevo sin tocar el script.

## Estructura

```
max-capital-propuesta/
├── SKILL.md
├── reference/
│   ├── esquema.md        el contrato JSON, campo por campo
│   ├── capitulos.md      catálogo de capítulos con ejemplos
│   ├── criterios.md      los criterios del equipo, con el porqué de cada uno
│   ├── oferta.md         política comercial: qué proponer y con qué lógica
│   └── equipo.md         directorio de contactos del equipo
├── ejemplos/
│   └── propuesta_ejemplo.json    ejemplo completo, usa todos los tipos
├── scripts/
│   └── generate_propuesta.py     CONFIG + parseo + render + PDF
└── assets/
    ├── base.css · deck.css · onepager.css · documento.css
    ├── fonts/            Inter 400/500/600/700 (woff2, embebidas)
    ├── logo_negativo.png  logotipo oficial, fondo oscuro
    ├── logo_positivo.png  logotipo oficial, fondo claro
    └── qr.svg
```
