# Criterios de propuestas

Los criterios del equipo de Wealth Management, cada uno con el porqué y el caso
real del que salió. Leelos antes de armar la primera propuesta: casi todos son
cosas que sólo se descubren mirando un PDF terminado, y varios corrigen errores
que ya se cometieron una vez.

Están ordenados por cuándo aparecieron, no por importancia. **El único que no
tiene excepciones es el 42: nada entra al PDF si no lo pidió el asesor.** Si
tenés que elegir tres más: no inventar datos de la casa (20), lo que la casa
hace o cobra se confirma (34) y escribir desde la mirada del cliente (19).

---

## 1. La clase de cuotaparte no se identifica

En material de cliente el fondo se nombra sin la clase: **"Max Renta Fija
Dólares"**, no "Max Renta Fija Dólares (Clase A)".

*Por qué:* la clase es una distinción comercial interna (fee, mínimo de
suscripción). Al cliente no le agrega información y abre una pregunta que no
hace falta contestar en una propuesta.

*Origen:* revisión de Javier Lago, 27/08/2026.

---

## 2. Nada de gráfico de distribución por vehículo

La torta "por vehículo" o "por fondo" no va nunca: repite exactamente lo que ya
dice la columna de ponderación de la tabla, con menos precisión.

*Por qué:* un gráfico tiene que mostrar algo que la tabla no muestra. Si es la
misma información en otro formato, ocupa espacio sin agregar nada.

*Origen:* revisión de Javier Lago, 27/08/2026.

---

## 3. Un gráfico de distribución solo si la distribución varía

La torta por clase de activo **sí** es relevante en general, pero no cuando la
cartera es de una sola clase. Una propuesta 100% renta fija no necesita un
gráfico que diga "renta fija 100%".

El criterio general: antes de poner un gráfico, mirar si la distribución tiene
dispersión real. Si no la tiene, el corte relevante es otro — en Javier Lago,
por ejemplo, la clase de activo era uniforme pero la moneda era 50/50, y esa sí
era la torta que valía.

*Por qué:* un gráfico de una sola categoría no informa, y ocupa el lugar del
corte que sí importaba.

*Origen:* revisión de Javier Lago, 27/08/2026.

---

## 4. En formato compacto, los instrumentos van como nota

En el one-pager, el "qué hace cada instrumento" es una **nota al pie chica**, una
línea por vehículo — o directamente no va. Nunca tarjetas.

El espacio de una hoja sola se lo tienen que quedar la tabla de cartera y las
distribuciones, que es lo que el cliente vino a ver. En el deck es distinto: ahí
los instrumentos son un capítulo propio con tarjetas y datos.

*Implementado:* el campo `resumen` de cada ficha (una cláusula corta) se usa en
el one-pager; `que_hace` (el texto largo) se usa en el deck.

*Origen:* revisión de Javier Lago, 27/08/2026.

---

## 5. El texto legal es el del `CONFIG`, y no se toca por propuesta

El disclaimer y las matrículas viven en el `CONFIG` de
`generate_propuesta.py`. **No se redactan, no se resumen y no se ajustan caso
por caso.** Si hace falta un cambio, se cambia ahí y vale para todas las
propuestas del equipo.

Hay una distinción que sí importa:

- **Una propuesta no puede decir que no es una recomendación.** El disclaimer de
  informes arranca con "no constituye oferta, invitación o recomendación". En
  una propuesta esa frase contradice el contenido del propio PDF, que recomienda
  instrumentos concretos para un cliente concreto. Por eso el texto de
  propuestas reconoce la recomendación y la funda en el perfil que aportó el
  cliente, conservando que no es oferta pública.
- **Las matrículas CNV van completas**, con el texto oficial y una sola vez por
  documento, junto al disclaimer.

*Origen:* pregunta de Pablo, 27/08/2026; texto vigente definido el 28/08/2026.

---

## 6. En propuestas 100% dólares, mostrar el interés compuesto

Cuando toda la cartera está en dólares, la propuesta lleva **renta anual
esperada** y **capital proyectado a N años** capitalizando. Es el modelo que ya
usan las propuestas del equipo: Latosinski muestra "Rendimiento anual esperado
USD 25.500" y "Capital Proyectado a 5 años USD 328.867"; la cartera conservadora
de banca privada muestra "USD 6.400" y "USD 136.367" a 5 años.

*Por qué:* proyectar a varios años solo tiene sentido en moneda dura. En pesos,
capitalizar una tasa nominal produce un número grande que no dice nada, porque
la inflación se come la diferencia — por eso una propuesta mixta o en pesos se
queda en el rendimiento del período y no proyecta.

*Cuándo NO:* carteras con tramo en pesos (como Javier Lago) o con horizonte
menor a un par de años.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 7. La liquidez de los FCI de Max es 24 horas

No 48. El plazo de liquidación de los fondos es 24 hs y así va en el KPI de
disponibilidad. Las 48 hs corresponden a otros vehículos (fondos de terceros en
la plataforma de Uruguay, por ejemplo), así que el dato hay que tomarlo del
fact sheet de cada instrumento y no por defecto.

*Origen:* corrección de Pablo, 27/08/2026.

---

## 8. Escala de color del nivel de riesgo: verde → azul → amarillo

- **Bajo / Conservador** → verde
- **Medio / Moderado** → azul
- **Alto / Agresivo** → amarillo

Nunca rojo. El rojo queda reservado para resultados negativos y para el bloque
de "vender".

*Por qué:* un nivel de riesgo alto es una característica del instrumento, no un
problema. Pintarlo de rojo lo lee como una alarma y desalienta una posición que
puede estar perfectamente justificada dentro de la cartera.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 9. En el one-pager, la distribución va debajo de la tabla

La tabla de cartera toma el ancho completo de la hoja; los gráficos de
distribución van debajo, en fila. Las tarjetas de KPI arrancan pegadas al
encabezado, sin aire arriba.

*Por qué:* la tabla es lo que el cliente viene a leer y sus columnas necesitan
espacio — con la distribución al costado, la descripción de los instrumentos se
partía en varias líneas. Y con un solo gráfico, la columna lateral dejaba media
hoja vacía.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 10. La nota de instrumentos cierra la hoja

En el one-pager va apoyada contra el disclaimer, al pie, a ancho completo — no
al costado de un gráfico ni flotando en el medio. Es contexto de lectura final,
posterior a la propuesta, y ese es su lugar en el orden de lectura.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 11. Todo documento va fechado y la fecha tiene que verse

Formato **mes/año** (`ago/2026`), en el encabezado, junto al nombre del cliente
y con el mismo tratamiento tipográfico que él —mayúsculas y tracking— apenas más
chica. No en letra chica al pie.

Se fecha por mes y no por día: el día exacto en que se armó la propuesta no le
dice nada al cliente y envejece el documento más rápido de lo que corresponde.
El generador deriva `ago/2026` de la fecha completa automáticamente; el campo
`fecha_corta` permite escribir un período propio si hace falta.

*Por qué:* una propuesta sin fecha visible no se puede archivar ni comparar
contra una posterior — y con tres clientes en paralelo, saber cuál versión es
cuál deja de ser un detalle. La fecha estaba al pie en gris de 7,6px y ni el
propio autor la encontró; si no la ve quien la armó, no la ve el cliente.

*Origen:* indicación de Pablo, 27/08/2026.

---

## 12. Capítulo `perfil` — quién es el cliente

No es el perfil de riesgo: es la persona. Edad, horizonte, dónde invierte hoy,
a qué se dedica, condiciones particulares — y un texto que le devuelve al
cliente lo que el asesor entendió de la charla.

Va **primero**, antes de cualquier número, y con una bajada que invite a
corregirlo. Una propuesta construida sobre un malentendido se cae en la reunión;
este capítulo hace barato descubrirlo antes.

*Implementado:* tipo `perfil`, con `rasgos` (etiqueta/valor, se leen como ficha
de datos) y `notas` (párrafos).

*Origen:* pedido de Pablo para Alejandro Vallejos, 28/08/2026.

---

## 13. Capítulo `proyeccion` — con los supuestos a la vista

Los números grandes arriba (capital aportado, rendimiento generado, capital al
retiro, retiro sostenible, TIR) y **los supuestos siempre visibles** en la misma
slide: rendimiento de acciones, de bonos, inflación, tasa de retiro.

*Por qué:* una proyección sin sus supuestos a la vista se lee como una promesa.
Mostrarlos convierte el número en el resultado de un modelo discutible, que es
lo que efectivamente es.

*Implementado:* tipo `proyeccion`, con `kpis` y `supuestos`.

*Origen:* pedido de Pablo para Alejandro Vallejos, 28/08/2026.

---

## 14. La proyección y la cartera propuesta tienen que cerrar entre sí

Antes de emitir, cruzar los supuestos de la proyección contra los rendimientos
de los instrumentos que realmente se proponen. Si no coinciden, decirlo — y
elegir a conciencia si se mantiene la proyección original (por consistencia con
el anexo que se entrega) o se recalcula.

*Caso Vallejos:* el anexo asumía bonos genéricos al 5,00%; la cartera propuesta
tiene renta fija al 6,84% ponderado (6,17% del fondo + 7,50% de las ONs). La
propuesta proyecta **más** que el anexo: USD 633.458 contra USD 618.446 en USD
de hoy. Se mantuvieron los números del anexo por consistencia entre los dos
documentos, aclarando en la slide que los supuestos de renta fija son
conservadores.

*El desajuste está en la renta fija, no en la asignación.* Despejando el peso en
acciones que reproduce el número del anexo, da 60,88% constante: el glidepath de
un horizonte de seis años ya arranca cerca del piso 60/40, así que contra una
cartera 60/40 fija la diferencia de asignación es 0,16% — ruido. Todo el desvío
lo explica el supuesto de bonos.

*Cómo verificarlo:* reconstruir el modelo del anexo (aportes a fin de año
ajustados por inflación, capitalizando al rendimiento ponderado del año) y
chequear que los aportes nominales den el mismo total que el reporte. Si cierran
los aportes, cualquier diferencia restante está en el camino de rendimiento y se
puede despejar.

*Origen:* verificación al armar Alejandro Vallejos, 28/08/2026.

---

## 15. El logotipo es el archivo oficial de marketing, sin modificar

Los únicos archivos válidos son los que provee marketing:

- `logo_negativo.png` — blanco, para fondos oscuros (portada del deck, divisores,
  cierre, banda del encabezado del one-pager)
- `logo_positivo.png` — negro, para fondos claros (portada del documento largo)

**No se recolorea, no se le baja la opacidad, no se le recortan los márgenes.**
Los márgenes del archivo son el área de resguardo de la marca; el generador
compensa el ancho (factor 0,648) para que el logotipo visible quede del tamaño
buscado sin tocar el archivo.

*Qué había mal:* la skill venía usando un SVG heredado de la skill de fact sheet
que **no es el logotipo oficial** — trazo más pesado y menos tracking que el de
marketing. Además se lo estaba tintando: 50% de opacidad en la portada del deck
y 92% en el encabezado del one-pager. Ese SVG se eliminó del repositorio para
que nadie lo use por error.

*Si aparece una variante nueva* (isologotipo, monograma, versiones "Tip B"),
agregarla como archivo aparte y elegirla por contexto — nunca derivarla
editando otra.

*Origen:* logos provistos por marketing vía Pablo, 28/08/2026.

---

## 16. El logotipo va siempre arriba a la derecha

Misma posición en todos los formatos y en todas las slides de marca: **esquina
superior derecha**.

- **Portada del deck:** grande (150px de logotipo visible). Es la firma de la
  marca en la primera hoja y tiene que lucirse.
- **Divisores y cierre:** mismo lugar, tamaño menor (84px).
- **Encabezado del one-pager:** en la banda negra, arriba a la derecha.
- **Slides de contenido:** no llevan logotipo. Ahí la esquina superior la ocupan
  el número de slide y el nombre del cliente, y la firma institucional ya va en
  la leyenda regulatoria del pie.

*Qué había mal:* la portada del deck lo tenía abajo a la izquierda mientras el
one-pager lo tenía arriba a la derecha. Dos documentos del mismo cliente abrían
con la marca en lugares distintos.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 17. Barras: normalizar sólo si son partes de un todo

El gráfico de barras reparte los valores sobre el total por defecto, que es lo
correcto para una distribución. Pero cuando las barras comparan **magnitudes
independientes** —un antes contra un después, dos carteras distintas— hay que
pasar `"normalizar": false`, porque sumarlas no significa nada.

*Qué pasaba:* "riesgo argentino hoy 63,9% / después 38,8%" salía impreso como
62,2% / 37,8%, sólo porque los dos valores sumaban 102,7 y se repartían sobre
ese total. Números inventados por el renderer, en una slide de cliente.

*Cómo detectarlo:* si los porcentajes del gráfico no coinciden con los del texto
de la misma propuesta, es esto.

*Origen:* error encontrado al armar Fernando Rodriguez, 28/08/2026.

---

## 18. Los encabezados de la tabla tienen que decir lo que la tabla hace

Las columnas traen títulos por defecto pensados para una cartera que se compra
("Rendimiento esperado", "Monto a invertir"). En una tabla de posiciones **que
se venden** eso dice lo contrario de lo que pasa: van "Resultado realizado" y
"Valuación".

Se resuelve pasando `columnas` como objetos con `clave`, `titulo` y `align` en
vez de sólo la clave.

*Origen:* revisión al armar Fernando Rodriguez, 28/08/2026.

---

## 19. Escribir desde la mirada del cliente, no como ficha interna

El capítulo de perfil describe al cliente, pero **lo lee el cliente**. No se
escribe "Alejandro es especialista en…" —ya sabe su nombre y a qué se dedica—:
se escribe en segunda persona, como devolución de lo conversado.

Sirve igual como antecedente escrito de lo que se acordó; lo que cambia es el
registro, no el contenido.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 20. No inventar nada de la casa: ni URLs, ni textos, ni datos

La slide de cierre traía "WWW.MAX.CAPITAL" como valor por defecto. **Lo había
puesto yo**, no salía de ningún material de la casa. Se eliminó del `CONFIG` y
ahora, si el capítulo no trae `url`, la slide no la muestra.

Vale para todo: URLs, leyendas, textos legales, nombres de producto, teléfonos.
Si no está en el material que aportó el asesor, no va — y si hace falta, se
pide.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 21. Capítulo `glidepath` — la trayectoria de la asignación

Muestra cómo evoluciona el asset allocation a lo largo del horizonte. Sirve
tanto para un desarme gradual de riesgo como para mostrar que la asignación **no
cambia** — que también es una decisión y conviene que esté dicha.

Los tramos marcados `"tentativo": true` se dibujan atenuados y punteados: son
los que todavía no están decididos y no deben leerse como compromiso.

*Caso Vallejos:* 60/40 fijo durante los seis años de aportes, y una revisión
hacia 40/60 al llegar al retiro, dibujada como tentativa.

*Origen:* pedido de Pablo, 28/08/2026.

---

## 22. El riesgo se cuenta con el tiempo de recuperación, no sólo con la caída

Para un horizonte definido, lo que importa no es cuánto cae el portfolio sino
**cuánto tarda en volver**. Una caída del 36% que se recupera en seis meses es
menos problema que una del 22% que tarda casi dos años, si el retiro está cerca.

Los dos datos salen del fact sheet: "Caída máxima" y "Recuperación" (la racha
más larga bajo el agua). Conviene dar también la del índice de referencia: la
serie del portfolio suele ser corta y subestima el peor caso.

*Datos CEDEARs de ETFs al 07/2026:* caída máxima -36,2% (feb–mar 2020);
recuperación 1,7 años (nov 2021 – jul 2023). ACWI: -33,5% y 2,3 años
(nov 2021 – mar 2024).

*Origen:* indicación de Pablo, 28/08/2026.

---

## 23. Las barras de un gráfico apilado van todas del mismo largo

En un apilado al 100% cada columna representa el total, así que todas tienen que
medir exactamente lo mismo. Una más corta que otra se lee como "acá hay menos",
que es justo lo contrario de lo que el gráfico dice.

*Qué pasaba:* el pie de cada columna crecía con su contenido, y las que llevaban
una nota debajo de la etiqueta —"2026", "Retiro · 2032", "A definir"— le robaban
alto a su propia barra. Se resolvió dándole alto fijo al pie, lleve una línea o
dos.

*Cómo verificarlo:* medir los altos en el navegador antes de dar por buena la
slide. Deben ser idénticos, no parecidos.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 24. El mismo instrumento dice lo mismo en todas las propuestas

Si dos clientes reciben una propuesta con el mismo vehículo, la descripción y
los datos tienen que ser idénticos. Un cliente con -28,05% de caída máxima y
otro con -36,2% para el mismo portfolio es un problema, no un matiz.

*Qué pasaba:* actualicé la ficha de CEDEARs de ETFs en Vallejos con la
definición oficial nueva y el dato correcto, y quedó desincronizada con la de
Rodriguez, que seguía con el texto viejo del PDF anterior.

*Cómo evitarlo:* al cambiar la descripción de un instrumento, revisar qué otras
propuestas lo usan. Con el tiempo conviene que las fichas vivan en un archivo
compartido y las propuestas las referencien por nombre.

*Origen:* detectado al actualizar Fernando Rodriguez, 28/08/2026.

---

## 25. En la página de resumen, las cifras van abreviadas con M y K

La primera página —la de KPIs que resume la propuesta— usa **M para millones y
K para miles**: `USD 1,3M`, `+USD 450K`. El detalle completo va en las tablas,
que es donde se audita.

*Por qué:* la tarjeta de resumen se lee de un vistazo y desde lejos. "USD
1.300.056" obliga a contar dígitos para saber de qué orden de magnitud se está
hablando; "USD 1,3M" se entiende de una.

*Dónde no:* en las tablas de detalle y en el menú de instrumentos, donde el
número exacto es el dato.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 26. Las tarjetas de una fila se alinean pieza por pieza

En una fila de tarjetas, cada parte se ancla por separado: **la etiqueta arriba,
el número siempre a la misma altura, la nota al pie**. No alcanza con alinear el
bloque entero.

*Qué pasaba:* las tarjetas de KPI iban todas alineadas al pie
(`justify-content:flex-end`), así que la que tenía nota empujaba su número una
línea hacia arriba y la que no la tenía lo dejaba abajo. En una fila de cuatro
donde dos tienen nota y dos no, los números quedan a dos alturas distintas.

Lo mismo con las etiquetas: si una envuelve a dos líneas y otra no, el número se
corre. Por eso la etiqueta lleva alto mínimo de dos líneas.

*Cómo verificarlo:* medir en el navegador los `top` de `.k-label` y `.k-value`
de la fila. Tienen que ser todos el mismo número, no parecidos:

```js
[...document.querySelectorAll('.kpi-grid.hero .k-value')]
  .map(e => Math.round(e.getBoundingClientRect().top))
```

*Vale como método general:* cuando un bloque se repite en fila o en grilla,
comparar las posiciones de sus partes antes de dar la slide por buena. Los
desalineados de una o dos líneas no se ven mirando, y se ven todos juntos en la
reunión.

*Origen:* propuesta armada por un asesor del equipo, 28/08/2026.

---

## 27. No renunciar por escrito a lo que la casa sí hace

Una advertencia del tipo "esto no lo contemplamos, fijate vos" es una renuncia
de servicio escrita en la propuesta. Antes de escribir que algo queda fuera,
verificar si la casa efectivamente lo cubre.

*Caso concreto:* Max Capital **sí provee cierto grado de asesoramiento
impositivo**. La propuesta de Vallejos decía que los impuestos no estaban
contemplados y que "siendo tu especialidad, es el primer ajuste que corresponde
hacer" — le pasaba el tema al cliente en algo sensible que nosotros sí
acompañamos. Quedó reescrito como: el anexo está antes de impuestos, definir el
tratamiento es parte de lo que trabajamos con vos, y conviene hacerlo antes de
la primera operación.

Reconocer la especialidad del cliente está bien. Usarla para delegarle el tema,
no.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 28. Los costos se dicen una vez, en su lugar

Los honorarios y costos van declarados con claridad **donde informan la
decisión** —en la descripción del producto o en la estructura de la relación—,
no repetidos después como advertencia que erosiona los números propios.

*Qué pasaba:* la propuesta ya decía en el punto de partida que los tres
componentes son productos de administración, sin costo de entrada ni salida y
con honorario anual. Estaba bien dicho y en el lugar correcto. Pero una slide
más adelante volvía sobre el tema para agregar que esos honorarios "tampoco
están descontados de la proyección". Redundante y defensivo: llevaba al frente
el costo propio como si fuera una objeción.

Esto **no es ocultar costos** —el dato sigue estando, completo y temprano—: es
no repetirlo en tono de disculpa.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 29. La cuenta internacional entra cuando el patrimonio la habilita

Una propuesta instrumentada solo a través de Argentina conviene que diga que lo
es, y que anticipe el salto: **superados los USD 250.000 bajo administración se
sugiere abrir una cuenta internacional a través de Max Capital**, que habilita
notas estructuradas y fondos del exterior.

Poné la fecha estimada del cruce calculándola con los aportes proyectados: dice
mucho más "hacia 2028" que "cuando crezca". Es un capítulo de crecimiento de la
relación, no una limitación de la propuesta.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 30. El título de la slide de riesgos no puede sonar a lista de problemas

"Las cuatro decisiones que hay que discutir" le tira el quilombo al cliente:
suena a que la propuesta viene con pendientes que él tiene que resolver. **"Cuatro
puntos bajo la mira"** dice lo mismo sin trasladarle la carga — son temas que el
asesor ya identificó y sobre los que va a estar encima.

El contenido de la slide no cambia: los riesgos se siguen exponiendo de frente.
Lo que cambia es de quién parece ser el problema.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 31. No decir "la más larga" si sólo se mira una ventana corta

Los indicadores de racha bajo el agua y caída máxima de un fact sheet se miden
sobre **la historia disponible del portfolio**, no sobre la historia del mercado.
Para el portfolio de CEDEARs de ETFs eso son poco más de seis años (desde fines
de 2019).

Escribir "la racha más larga fue de 1,7 años" sugiere un máximo histórico que no
es. Corresponde acotar la ventana —"desde el inicio del portfolio, a fines de
2019"— y decir que con más historia de mercado aparecen episodios más largos.

Si hace falta afirmar un máximo real, hay que ir a buscar la serie del índice
desde los 90 en adelante. No se infiere del fact sheet.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 32. El tratamiento impositivo local es un argumento, no una advertencia

En una cartera instrumentada en Argentina, los impuestos juegan a favor y hay que
contarlo así:

- **Los instrumentos con cotización pública local no están alcanzados por el
  impuesto a las ganancias de capital.** Es un beneficio concreto de operar
  localmente.
- Dentro de una cartera con CEDEARs, el único ítem alcanzado por ganancias son
  **los dividendos**, con incidencia baja (rendimiento por dividendos en torno
  al 2%).
- Eso conecta con la custodia: la cuenta internacional se sugiere cuando el
  patrimonio la justifica, y el tramo local **es donde están los mayores
  beneficios impositivos**.

Los tres puntos se sostienen entre sí: explican por qué la propuesta arranca en
Argentina y por qué el salto al exterior llega después, por diversificación y no
por conveniencia fiscal.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 33. El dato va escrito, la lectura la da el asesor en la reunión

Una propuesta expone los riesgos con datos. **La interpretación dramática de esos
datos no se escribe.**

*Qué pasaba:* la slide de riesgos cerraba con "un episodio así arrancando en 2030
se resuelve dentro del horizonte; arrancando en 2031, no". Es un escenario
inventado, con fecha puesta, sobre algo que no sabemos cuándo va a pasar ni si va
a pasar. Quedó reemplazado por el dato pelado: cuánto cayó, cuánto tardó en
recuperarse, y sobre qué ventana se mide.

*Por qué:* un riesgo dramatizado por escrito no se puede matizar después. El
asesor puede decir esa misma frase en la reunión, leyendo la cara del cliente y
respondiendo la repregunta en el momento. El PDF queda, se reenvía, y se lee
solo dentro de dos años.

No es esconder el riesgo: es dejar el dato completo y no ponerle encima una
conclusión que nadie puede sostener.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 34. Lo que la casa hace, cubre o cobra se confirma — nunca se infiere

Cualquier afirmación sobre **alcance de servicio, cobertura o costos de Max
Capital** se verifica con el asesor antes de escribirla. No se deduce del
material aportado: del fact sheet de un fondo no sale qué servicios presta la
casa, y de una propuesta anterior tampoco.

Es la categoría donde el error sale más caro, porque el PDF lleva la identidad
de la firma y se lee como institucional. Un cliente que lee "esto no lo
contemplamos" asume que es política de la casa.

Errores reales de esta clase, todos en una misma tarde:

| Lo que se escribió | Por qué estaba mal |
|---|---|
| `WWW.MAX.CAPITAL` en el cierre | Inventada; no salía de ningún material |
| El disclaimer legal, redactado condensando otro | El texto legal vive en el `CONFIG` y no se reescribe por propuesta |
| "El anexo no contempla impuestos, es el primer ajuste que te corresponde" | La casa **sí** provee asesoramiento impositivo |
| "Los honorarios tampoco están descontados de la proyección" | Llevaba el costo propio al frente, ya declarado antes |

Ante la duda: preguntar. Cuesta un mensaje y evita un PDF que dice algo que la
casa no dice.

Ver también [20](#20-no-inventar-nada-de-la-casa-ni-urls-ni-textos-ni-datos),
[27](#27-no-renunciar-por-escrito-a-lo-que-la-casa-sí-hace) y
[28](#28-los-costos-se-dicen-una-vez-en-su-lugar).

*Origen:* patrón detectado repasando las correcciones de Pablo, 28/08/2026.


---

## 35. El texto legal nunca se recorta

Ningún disclaimer ni leyenda de matrículas puede quedar cortado por una caja de
alto fijo. Si no entra, se agranda el espacio o se achica la tipografía — nunca
se recorta.

*Qué pasaba:* el disclaimer del one-pager estaba dentro de una caja de
`max-height:64px` con `overflow:hidden`, y el del cierre del deck en una de
118px. Con el texto corto no se notaba. Al cargar el disclaimer oficial completo
—de 1.076 a 2.592 caracteres— el texto legal empezó a cortarse **en silencio**:
la caja medía 64px y el contenido 104px, sin ninguna señal visible.

*Cómo verificarlo:* comparar `scrollHeight` contra el alto real de la caja. Si
difieren, hay texto cortado:

```js
const d = document.querySelector('.disclaimer');
d.scrollHeight > d.getBoundingClientRect().height  // true = recortado
```

Hacerlo cada vez que cambie el texto legal, y también cada vez que cambie el
layout del pie.

*Origen:* detectado al cargar el disclaimer oficial, 28/08/2026.


---

## 36. Una proyección tiene que decir en qué moneda está

Si las cifras están en moneda constante —"USD de hoy", ya descontada la
inflación— hay que decirlo **sobre los números**, no en la bajada de la slide,
que se saltea. Y conviene dar también el equivalente nominal.

*Por qué:* sin la aclaración, el cliente lee el rendimiento como nominal y le
parece flojo. Seis años de aportes que generan USD 108.446 se leen distinto
cuando al lado dice USD 177.199 nominales y arriba dice que el primero ya tiene
la inflación descontada. **La cifra real es la honesta; la nominal es la que el
cliente reconoce.** Las dos juntas cuentan la historia completa; una sola, a
medias.

*Implementado:* `base` en el capítulo `proyeccion` dibuja la franja sobre los
KPIs; `valor_nominal` en cada ítem agrega la cifra secundaria debajo del número
principal.

*Vale igual para la TIR:* "5,4% real / 8,2% nominal" en vez de "TIR real 5,4%"
con el nominal escondido en la nota al pie.

*Origen:* indicación de Pablo, 28/08/2026.

---

## 37. "Riesgo argentino" hay que definirlo, no suponerlo

No todo lo emitido por una entidad argentina cuenta como riesgo argentino. La
definición del equipo:

**Riesgo argentino = soberano argentino (hard dollar y pesos) + equity argentino.**

Quedan **fuera**, deliberadamente:

- **ONs corporativas bajo ley NY** de empresas de primera línea (Vista, YPF,
  PCR). Es riesgo de crédito corporativo con legislación extranjera: otra cosa.
- **Deuda provincial.**

*Qué pasaba:* mezclé todo en un solo número —"riesgo argentino 63,9%"— sumando
soberano, provincial, ONs corporativas y equity. Con las ONs adentro, el
indicador se movía por razones que no tenían que ver con el riesgo país, y la
propuesta parecía reducir una exposición que en realidad se mantenía a
propósito. Con la definición correcta, el número real de la operación de
Rodriguez es **47,0% → 12,9%**.

*Y siempre declarar la definición al pie del gráfico.* Un porcentaje de "riesgo
argentino" sin decir qué incluye es un número que cada lector interpreta
distinto — empezando por el asesor.

*Origen:* corrección de Pablo, 28/08/2026.

---

## 38. Clasificar por tipo de activo, nunca por cuenta

Las posiciones se agrupan por **qué son**, no por dónde están custodiadas. Un
cliente con cuenta en Argentina y en Uruguay tiene los mismos tipos de activo
repartidos entre las dos.

*Qué pasaba:* tomé el bloque "Renta Variable USD — Max Argentina" (USD 533.020)
y lo etiqueté "Renta variable Argentina" en la propuesta. Pero ese bloque son
**todos** los CEDEARs de la cuenta argentina: SPY, MELI, AMD, TSM y compañía.
El equity argentino real era USD 237.588, menos de la mitad. Por el mismo error
las ONs corporativas figuraban como USD 158.056 en vez de 245.869, porque las
dos de Uruguay quedaban en otro bloque.

*Cómo evitarlo:* antes de escribir un solo monto, reconstruir la cartera por
tipo de activo y **pasarle la tabla al asesor para que la confirme**. Cuesta un
mensaje y evita que toda la propuesta se apoye en una clasificación equivocada.

*Origen:* error propio detectado por Pablo, 28/08/2026.

---

## 39. Lo que se mantiene tiene que sumar tanto como lo que se vende

En una propuesta de reposicionamiento, el bloque "mantener" debe cubrir **todo**
lo que no se vende. Si el cliente suma lo que ve y no le da el total de su
cartera, la propuesta pierde credibilidad justo donde más la necesita.

*Qué pasaba:* la propuesta de Rodriguez listaba en "mantener" las ONs, el equity
argentino, la nota estructurada, Santa Fe y TMVE8 — USD 552.418. Pero lo que no
se vendía eran USD 774.927. Faltaba un bloque entero: **USD 213.828 de equity
internacional (MELI, SPY, DIA, PBR, AMD, TSM), el 16,4% de la cartera**, el
mayor bloque de renta variable que quedaba en pie y no figuraba en ninguna
slide.

*Cómo verificarlo, siempre:*

```
total de la cartera − suma de lo que se vende = suma de lo que se mantiene
```

Si no cierra al peso, falta un bloque. Y contar también las posiciones nuevas:
"de 32 posiciones a 19" era 20 — quedaban 17 y entraban tres líneas.

*Origen:* verificación pedida por Pablo, 29/08/2026.

---

## 40. En columnas de altura pareja, el sobrante se reparte entre los ítems

Las columnas de comprar / vender / mantener las estira la grilla al mismo alto,
pero casi nunca tienen la misma cantidad de entradas. Sin repartir, la columna
con menos ítems deja un hueco muerto al pie y las tres se ven desbalanceadas.

Cada ítem toma `flex:1 0 auto`: se reparte el espacio sobrante y el aire se
convierte en interlineado. El `0 auto` evita que un ítem se comprima por debajo
de su contenido cuando la columna va llena.

*Cómo verificarlo:* medir el hueco entre el último ítem y el pie de la columna.
Tiene que ser el mismo en las tres, no sólo parecido.

*Origen:* indicación de Pablo, 29/08/2026.


---

## 41. Si la slide compara un antes y un después, escribí el delta

Dos gráficos lado a lado muestran los dos estados pero **no muestran el cambio**:
el lector tiene que restar de memoria, y el cambio es justamente la conclusión de
la slide.

Va una franja de tarjetas **arriba de los gráficos** con cuánto se movió cada
cosa —`riesgo argentino −34,1 pp`, `renta variable +2,8 pp`— con el antes y el
después en letra chica debajo. Una sola tarjeta destacada, la que sostiene el
argumento.

*Arriba y no al pie:* el delta es la conclusión, y la conclusión se lee primero.
Debajo van los gráficos, que son el detalle que la sostiene. Es el mismo orden
que usan las slides de ficha de portfolio — métricas arriba, composición abajo
(criterio 45) — y hace que el deck tenga una sola gramática. Sin línea
divisoria: separar los dos bloques con una raya le mete fricción a la slide.

*Ojo con el color:* una baja no siempre es mala noticia. "Riesgo argentino
−34,1 pp" es el mejor número de la propuesta. Por eso los deltas no usan la
escala verde/rojo: el signo lo dice todo y el color sólo confundiría.

*Implementado:* campo `deltas` del capítulo `distribuciones`.

*Origen:* indicación de Pablo, 29/08/2026.


---

## 42. Nada entra al PDF si no lo pidió el asesor

**El criterio más importante de esta lista, y el único sin excepciones.**

Trabajando sobre una cartera vas a encontrar cosas que nadie te pidió mirar: una
concentración por emisor, un costo alto, una posición que perdió su tesis, un
número que no cierra. **Ese hallazgo se le dice al asesor, en el chat, y ahí
termina.** No entra a la propuesta: ni como columna, ni como nota al pie, ni
como "tema de la próxima conversación".

*Qué pasó:* en la propuesta de Rodriguez metí una columna titulada **"Lo que
esta propuesta no resuelve"**, contándole al cliente que tenía 12,3% en YPF y
12,2% en Vista, que eran concentraciones que no se veían en su estado de cuenta,
y que era el tema de la próxima conversación. El análisis era correcto. La
decisión de ponerlo en un PDF firmado no era mía, y nadie me la pidió.

*Por qué es tan grave:*

- **Le traslada al cliente un problema que la casa no eligió plantearle.** El
  asesor decide qué conversación se da, cuándo y con qué palabras.
- **Queda por escrito y se reenvía.** Una frase dicha en una reunión se matiza
  con la repregunta; una línea en un PDF no.
- **Erosiona la propuesta desde adentro.** Un documento que dice lo que no
  resuelve se está discutiendo a sí mismo.
- **Suena a que la casa entrega trabajo incompleto**, aunque el hallazgo sea
  exactamente lo contrario: evidencia de que se miró en profundidad.

*No existe la versión suave.* No hay forma de redactar bien una limitación que
el asesor no aprobó: el problema no es el tono, es quién decidió incluirla.

*La regla operativa:* si el hallazgo no está en lo que el asesor te pidió, va al
chat. Si te parece importante, decíselo con todas las letras — pero en el chat,
y esperá su respuesta antes de tocar el PDF.

*Origen:* error propio, señalado por Pablo, 29/08/2026.


---

## 43. Preguntá quiénes van en los datos de contacto

**No lo deduzcas de quién te está hablando.** En Max Capital lo habitual es
trabajar en dupla, y el cliente tiene que poder escribirle a los dos. El asesor
que arma la propuesta no siempre es el único que atiende la relación.

*Qué pasaba:* las tres propuestas salieron con un solo contacto, el de quien me
estaba dictando. Pablo trabaja siempre con Marcos Sanchez Negrete y sus datos no
figuraban en ninguna — algo que el generador no puede adivinar y que yo nunca
pregunté.

*El directorio del equipo está en* [`equipo.md`](equipo.md) *y se completa así:*

```json
"asesores": [
  { "nombre": "Pablo Haro", "cargo": "Wealth Management", "email": "pharo@max.capital" },
  { "nombre": "Marcos Sanchez Negrete", "cargo": "Wealth Management", "email": "msancheznegrete@max.capital" }
]
```

El orden importa: el primero encabeza la relación y es quien aparece en
"Presentado por" de la portada. `asesor` en singular sigue funcionando para una
sola persona.

*Si falta un teléfono o un dato, va sin él.* No se inventa ni se reutiliza el de
otra propuesta — ver criterio 34.

*Origen:* indicación de Pablo, 29/08/2026.


---

## 44. En banca privada se propone fee based, no por transacción

Una propuesta para persona física va bajo **esquema de honorario de
administración**. Si la cartera que trae el asesor no tiene ningún vehículo
administrado, planteáselo antes de escribirla.

*Por qué:* la comodidad empuja al modelo de trading — es más rápido proponer lo
que el cliente ya opera. Para **empresas** ese modelo tiene sentido y se evalúa
caso por caso. Para **banca privada alinea mal los incentivos**: cobra por
operar en vez de por administrar, encarece cada rebalanceo y convierte al asesor
en ejecutor.

*Los tres que van siempre* (salvo que el caso lo desaconseje): FCI Max Renta
Fija Dólares, cartera de CEDEARs de ETFs, y notas estructuradas para inversores
desde USD 250.000. El detalle completo está en [`oferta.md`](oferta.md).

*Planteáselo, no lo cambies.* La cartera la decide el asesor — ver criterio 42.
Lo que corresponde es decirle que la propuesta quedó sin componente
administrado y por qué eso importa.

*Origen:* política comercial definida por Pablo, 29/08/2026.

---

## 45. Mostrá el vehículo que el cliente todavía no conoce

Cuando la propuesta incorpora una cartera administrada que el cliente no tenía,
dedicale **una slide propia**: métricas de rendimiento y riesgo arriba,
composición debajo.

*Por qué:* un cliente que viene de posiciones directas necesita entender qué
está comprando antes de aceptar delegar. Una línea en la tabla de cartera no
alcanza para eso, y es justo donde se cae la conversación de cuentas
administradas.

*Qué mostrar,* según lo que tenga el fact sheet:

- **Renta variable:** anualizado a 5 años, desde inicio, volatilidad, caída
  máxima y cuánto tardó en recuperar. Composición por región y por sector.
- **Renta fija:** TIR, duration y calidad crediticia promedio — son los tres
  datos que un cliente con bonos directos va a comparar contra los suyos.
  Composición por calificación, tipo de emisor y región.

*Mostrá la calificación completa*, incluido el tramo de alto rendimiento. Es
mejor que lo vea en la propuesta y no cuando revise el fondo por su cuenta.

*Implementado:* el capítulo `distribuciones` acepta `kpis` de encabezado.

*Origen:* propuesta de Fernando Rodriguez, 29/08/2026.


---

## 46. Prohibidas las tensiones, los dilemas y las preguntas incómodas

Nunca, en ninguna propuesta, construcciones del tipo:

- "Lo que esta propuesta **no resuelve**"
- "La **tensión** que hay que definir"
- "La **pregunta incómoda** es"
- "El **punto débil** de este esquema"
- "**Hay que reconocer que**…"
- "Lo que **queda pendiente**"

Ni con esas palabras ni con sinónimos. No es cuestión de redacción: es la
construcción misma.

*Por qué aparece:* plantear tensiones y contradicciones es un hábito
conversacional. En un chat genera diálogo y suena a honestidad intelectual —el
interlocutor engancha, repregunta, discute. **En un documento de venta es
autosabotaje.**

*Por qué está mal acá:* el cliente no está conversando, está evaluando una
recomendación de su asesor. Una propuesta que se plantea dilemas a sí misma se
está discutiendo por escrito, y le deja al cliente un problema que la casa no
eligió plantearle. Encima queda en un PDF que se reenvía y se lee dentro de dos
años, sin nadie que lo matice.

*Qué sí se hace:* los riesgos se exponen **con datos**. "La caída más profunda
fue -36,2% y tardó 1,7 años en recuperarse" informa el mismo riesgo sin
convertirlo en un dilema del cliente. La lectura de ese dato la da el asesor en
la reunión — ver criterio 33.

*Origen:* corrección de Pablo, 29/08/2026. Es la extensión del criterio 42.

---

## 47. De los costos se habla en positivo, o no se habla

Cuando el costo entra en una propuesta es **para decir lo que el cliente gana**:

- No hay arancel de entrada ni de salida
- El rebalanceo no tiene costo asociado
- El esquema de administración alinea los incentivos
- El marco impositivo local genera eficiencias concretas — instrumentos con
  cotización pública exentos de ganancias de capital

**Nunca como advertencia ni erosionando los números propios.** Frases como "los
honorarios tampoco están descontados de la proyección" o "a esto hay que
restarle nuestro fee" no van: llevan al frente el costo propio como si fuera una
objeción que el cliente todavía no hizo.

*El foco es el beneficio del cliente, la propuesta y el servicio.* Esa es la
conversación; el costo es un dato dentro de ella, no su eje.

*Esto no habilita ocultar nada.* Los costos se declaran completos y donde
informan la decisión —en la descripción del producto o en la estructura de la
relación, ver criterio 28—. Lo que cambia es el registro: factual y positivo, no
apologético.

*Origen:* corrección de Pablo, 29/08/2026.


---

## 48. Un decimal en los porcentajes, nunca dos

`10,1%` y no `10,11%`. `7,0%` y no `7,00%`.

*Por qué:* es lo mismo que hablar de centavos cuando el monto está en dólares —
no aporta precisión útil y le quita seriedad al número. Un rendimiento de
"10,11% anualizado a 5 años" sugiere una exactitud que la estimación no tiene.

Vale para rendimientos, TNA, TEA, volatilidades, ponderaciones y puntos
porcentuales. **Los fact sheets suelen venir con dos decimales: hay que
redondear al pasarlos a la propuesta.**

*Cómo verificarlo:* buscar en el JSON el patrón `dígito,dígito dígito%` antes de
generar.

*Origen:* indicación de Pablo, 30/08/2026.

---

## 49. Escala de riesgo: Bajo, Medio, Alto — y es relativa al inversor

La escala del equipo tiene tres niveles. La referencia por tipo de activo:

| Instrumento | Nivel |
|---|---|
| Fondos de renta fija (Max Renta Fija Dólares, mutual funds RF) | **Bajo** |
| ONs corporativas | **Medio** |
| CEDEARs de ETFs | **Alto** |

**Pero el nivel es relativo al punto de partida del inversor.** A alguien que
sólo hizo plazo fijo, un fondo de renta fija en dólares se le presenta como
**medio**: no es devengamiento, el valor de la cuotaparte se mueve, y para él eso
es riesgo aunque la volatilidad sea baja.

*La decisión es del asesor.* Preguntale de dónde viene el cliente antes de
asignar niveles, y si el caso lo pide, corré la escala.

*Cuando el fact sheet dice otra cosa:* el fact sheet de Max Renta Fija Dólares
dice "perfil moderado, riesgo 2 de 5" y el equipo lo trata como bajo. Prevalece
el criterio del asesor para la propuesta; el fact sheet queda como anexo con su
propia escala.

**El badge va rotulado.** Una pastilla que dice "Alto" arriba a la derecha no se
entiende sola: lleva "Nivel de riesgo" al lado. Para quien ve la propuesta por
primera vez, no es obvio a qué se refiere.

*Origen:* definido por Pablo, 30/08/2026.

---

## 50. Detrás de cada producto hay gestión activa, y hay que decirlo

En los tres vehículos que más se proponen —CEDEARs de ETFs, mutual funds de
renta fija y FCI Max Renta Fija Dólares— **es importante señalar que hay
management activo detrás**, buscando las mejores oportunidades para optimizar el
patrimonio del cliente.

*Cuidado con el vocabulario.* Escribir que "la cartera **replica** los
principales índices" es un error grave: suena a que no hacemos nada, describe
algo pasivo. La construcción correcta es **"invierte en instrumentos que
replican"** — el que replica es el ETF, no nuestra gestión.

Otras palabras que restan: "sigue", "espeja", "copia". Las que suman: invierte,
selecciona, utiliza, construye, ajusta.

En los fondos de terceros, decir explícitamente que **la selección es nuestra**,
hecha en base a nuestro análisis y a nuestra visión de mercado. Sin eso, una
lista de cinco fondos parece un menú y no una decisión.

**Las descripciones oficiales están en [`oferta.md`](oferta.md) y se usan
literales.** No se resumen ni se reescriben. Comprimirlas pierde matices que sí
importan: que los ETFs cotizan como CEDEARs en el mercado local, que la
diversificación es también por clase de activo, que el oro descorrelaciona
*frente a los mercados accionarios*. Si no entran en el espacio, recortá
oraciones enteras del final antes que parafrasear.

*Cómo se rompió:* al comprimir la descripción oficial quedó "la cartera replica
los principales índices" en lugar de "invierte en instrumentos que replican los
principales índices del mercado". Una palabra, y el sentido pasó de gestión
activa a producto pasivo.

*Origen:* corrección de Pablo, 30/08/2026.

---

## 51. La propuesta termina mostrando cómo queda la cartera

Antes del cierre va una slide con **la composición resultante**: qué queda, en
qué proporción y con qué nivel de riesgo.

*Por qué:* sin eso, una propuesta de reposicionamiento muestra lo que se vende y
lo que se compra, pero nunca la foto final. El cliente tiene que poder ver el
resultado de la operación completa, no reconstruirlo sumando slides.

Se arma con `cartera_sugerida`, reutilizando los KPIs de encabezado y los badges
de riesgo. Incluí **todo** lo que queda, también lo que no se tocó — ver
criterio 39.

*Origen:* indicación de Pablo, 30/08/2026.

---

## 52. Los encabezados no se mueven entre slides

El número, el nombre del cliente y el título tienen que estar **en la misma
posición en todas las slides**. Si una comprime su contenido, se comprime el
cuerpo, nunca la cabecera.

*Qué pasaba:* el modo denso achicaba el padding superior y el tamaño del título,
así que al pasar de una slide normal a una comprimida el número y el título
saltaban de lugar. Pasando páginas se ve como un temblor.

*El criterio general:* al ajustar el espacio de una slide hay que mirar **de
dónde viene el lector**, no sólo si el contenido entra. Una slide puede estar
perfecta sola y estar mal en la secuencia.

*Cómo verificarlo:* medir el `top` del badge en todas las slides del deck. Debe
haber un solo valor.

*Origen:* corrección de Pablo, 30/08/2026.

---

## 53. La proyección de retiro va en toda propuesta de primera vez

En una propuesta a un cliente nuevo, **sugerí incorporar la proyección de
retiro** aunque el asesor no la pida.

*Por qué:* es lo que estimula al inversor a hacer **aportes recurrentes**. Y los
aportes recurrentes permiten hacer DCA sobre la cartera objetivo, lo que vuelve
mucho más robusta la generación de rendimientos a largo plazo y mejora
considerablemente la experiencia del cliente con su portfolio.

No es un capítulo decorativo: es el que convierte una inversión única en un plan
de aportes.

*Cómo:* capítulo `proyeccion`, con la base declarada y los supuestos a la vista
— ver criterio 36. Si el asesor no tiene una proyección armada, pedísela antes de
inventar los números.

**La regla es por los aportes, no por el nombre del caso: si entra dinero nuevo,
proyectá.** No importa que la propuesta sea de primera vez, una revisión o un
reposicionamiento. Lo único que decide es si hay capital entrando: eso es lo que
la proyección tiene para proyectar.

Cuando la propuesta sólo reordena una cartera que ya existe y no entra nada, la
proyección no tiene materia prima y el argumento es cómo queda la cartera. Fue el
caso de Fernando, 30/08/2026.

*Por qué está escrito así:* antes decía "no va en un reposicionamiento", y esa
excepción se aplicó mal en Jimena Laino (06/09/2026). El caso se clasificó como
reposicionamiento por la palabra —había una cartera vigente que se reordenaba— y
se salteó la proyección, sin mirar que ese año había entrado USD 44.470 en
aportes y estaban entrando otros USD 25.000. La pidió Pablo varias rondas después.
Una regla con un "salvo que" invita a resolverla mirando la etiqueta del caso en
vez del hecho que importa.

*Origen:* indicación de Pablo, 30/08/2026.

---

## 54. Los gajos del donut son arcos, no guiones

Cada gajo se dibuja como un `<path>` con un arco explícito. **Nunca con
`stroke-dasharray` sobre un `<circle>`.**

*Por qué:* un `<circle>` es un path que abre y cierra en el mismo punto. Si un
gajo cae sobre esa costura —y el último gajo siempre termina ahí—, el navegador
lo traza como un tramo continuo que la cruza y le aplica un *join*. El resultado
es una punta que se escapa del anillo, con forma de flecha. No es antialiasing
ni un gajo demasiado chico: es geometría mal planteada, y aparece más cuanto más
chico es el último gajo.

*Cómo se rompió:* en la propuesta de Fernando, el donut "Perfil de la cartera
hoy" tenía Cash en 0,7%. Ese gajo salió impreso como un zigzag azul claro que
atravesaba el borde del anillo. Pasó la validación, pasó la generación del PDF y
lo encontró el asesor mirando la lámina.

*Cómo verificarlo:* exportar con `--design-html`, abrir el SVG del donut y
comprobar que hay un `<path d="M ... A ...">` por gajo y ningún
`stroke-dasharray`. Visualmente, ampliar el donut que tenga el gajo más chico:
los bordes entre gajos tienen que ser radios rectos.

*Ojo con el 100%:* un arco de 360° empieza y termina en el mismo punto y no
dibuja nada. Un gajo único va como `<circle>` completo — está contemplado en el
código.

*Origen:* lo detectó Pablo en la propuesta de Fernando, 30/08/2026.

---

## 55. "La slide 8" es ambiguo: contestá con el título

**Cuando el asesor identifica una slide por número, respondé nombrándola por su
título antes de tocar nada.** "Dale, en *A dónde van los fondos* saco las pills"
— si le erraste, te corrige ahí, antes de la regeneración.

*Por qué:* un deck tiene **dos numeraciones que no coinciden**. El badge no
cuenta la portada, así que ya arranca corrido; y cualquier capítulo que pagine
—fichas, tablas largas— agrega páginas que el badge tampoco cuenta. Cuanto más
larga la propuesta, más se separan. El asesor mira el visor de PDF y dice "la 8"
pensando en la página; el badge de esa página puede decir 7.

*Antes de preguntar, usá lo que ya tenés.* Casi siempre el propio pedido
desambigua: si dice "los badge" en plural, es una lámina con varias fichas y no
una con un solo badge de esquina; si dice "la columna del medio", es una de
texto; si menciona un dato, buscá en qué slide está. Preguntar es el último
recurso, no el primero — pero es infinitamente mejor que editar la equivocada.

*Si sigue sin estar claro, preguntá con los dos títulos a la vista:* "¿la de *A
dónde van los fondos* o la de *CEDEARs de ETFs*?". Nunca "¿a qué slide te
referís?", que le devuelve el problema sin ayudarlo a resolverlo.

*Cómo se rompió:* Pablo pidió sacar el badge de riesgo de "la slide 8". El badge
8 estaba en *CEDEARs de ETFs*, pero él miraba la página 8 del PDF, que es *A
dónde van los fondos*. Se editó la slide equivocada y hubo que revertirla. El
plural de "los badge" ya decía cuál era —esa lámina tiene tres fichas con tres
pills— y no se leyó.

*Origen:* indicación de Pablo, 30/08/2026.

---

## 56. Un dato en la esquina se alinea por línea de base y no le compite al título

Cuando una tarjeta lleva un dato en la esquina —el monto de una ficha, el nivel
de riesgo— se rige por dos reglas:

**Alineación por línea de base, no por el borde de la caja.** En flex es
`align-items:baseline`, no `flex-start`. Dos textos de distinto tamaño o
interlínea que arrancan sus cajas a la misma altura **no** apoyan sus letras a
la misma altura, y el ojo lee la línea de base: la de abajo, no el borde de
arriba. Con `flex-start` el dato queda flotando entre el título y el subtítulo,
sin coincidir con ninguno.

**Peso tipográfico igual o menor que el del título.** El dato acompaña, no
encabeza: quien manda en la tarjeta es el nombre del instrumento. Mismo cuerpo
que el título y un gris oscuro —`--gray-d`— rinde mejor que un cuerpo más grande
en color de marca, que se come la lámina.

*Cómo se rompió:* el monto salió a 13px, bold, en navy, contra un nombre de
instrumento de 12px. Pesaba más que el título y no coincidía con nada: ni con el
nombre, ni con el subtítulo, ni con el centro del bloque.

*Cómo verificarlo:* medir sobre el PDF, no mirar el HTML aislado —fuera del
documento no carga Inter y las medidas cambian—. Con `pypdf`, `extract_text`
acepta un `visitor_text` que entrega la matriz de texto: `tm[5]` es la línea de
base. La del dato y la del título tienen que dar el mismo número.

*Origen:* lo detectó Pablo en la propuesta de Fernando, 30/08/2026.

---

## 57. La leyenda de un gráfico no puede contradecir un KPI de la misma slide

**Si los valores de un gráfico ya vienen en porcentaje, la leyenda muestra el que
escribió el asesor.** No uno recalculado sobre la suma de los ítems.

*Por qué:* las ponderaciones de una cartera redondeadas a un decimal casi nunca
suman 100 exacto — suman 100,1 o 99,8. Si la leyenda divide cada valor por esa
suma, devuelve un número apenas distinto del original. El resultado es una slide
que dice **52,3%** en la tarjeta de arriba y **52,2%** en la leyenda de abajo,
para la misma cosa. El cliente no piensa "redondeo": piensa que uno de los dos
está mal, y a partir de ahí desconfía del resto de los números.

*La tentación es aclararlo al pie.* No: una nota que explica una diferencia de
redondeo ocupa lugar, mete ruido y no le sirve a nadie. Se arregla el número, no
se justifica.

*Cómo:* el generador detecta que los valores ya son porcentajes cuando suman
entre 99 y 101, y en ese caso imprime el valor tal cual. La geometría del gajo sí
se normaliza — esa diferencia no se ve.

*Origen:* lo detectó Pablo en la propuesta de Fernando, 30/08/2026.

---

## 58. Toda tabla lleva total, y la tabla tiene que cerrar con él

**Si una tabla tiene porcentajes o montos, lleva fila de total.** Y las filas
tienen que sumar exactamente lo que dice esa fila.

*El invariante no es "los porcentajes suman 100".* Es **que la tabla cierre con
su propio total**. Una tabla de posiciones a vender es un subconjunto: sus pesos
son sobre la cartera entera y suman 40,4%, que es correcto. Lo que nunca puede
pasar es que las filas digan una cosa y el total otra. Cuando no hay fila de
total, el único cierre posible es el 100%.

*Por qué:* el cliente suma. No toda la tabla, pero sí las dos o tres líneas que
le interesan, y si el total no da, deja de confiar en el resto de los números.
Una propuesta se sostiene sobre que las cifras cierren.

**Si no cierra, avisale al asesor y ofrecele el ajuste. No lo hagas por tu
cuenta:** cambiar un peso o un total es cambiar un número que él eligió.

*Los dos ajustes, y cuándo sirve cada uno:*

- **Rebasear.** La tabla muestra 5-86-4 sobre una base de 95 y se quiere leer
  sobre 100: cada valor pasa a `v/95`. Sirve cuando la base declarada no es la
  suma real.
- **Reparto por resto mayor.** Diez líneas redondeadas a un decimal suman 100,2%
  aunque la base esté perfecta: el desvío es la acumulación de los redondeos, no
  la base. Se baja 0,1pp a las líneas con el resto fraccionario más chico hasta
  cerrar en 100,0. **Rebasear acá no arregla nada** — recalculado da los mismos
  valores redondeados.

Diagnosticá cuál de los dos es antes de ofrecer: si al recalcular sobre la suma
real los redondeos no se mueven, es resto mayor.

*Cómo se verifica:* `--validar` lo controla solo y avisa. Compara las filas
contra la fila de total, tanto en porcentaje como en monto.

*Cómo se rompió:* en la cartera final de Fernando la columna sumaba 100,2% con
la fila de total diciendo 100%, y las valuaciones sumaban USD 1.300.052 contra
un total declarado de USD 1.300.056. Había una nota al pie que lo explicaba;
se sacó la nota —bien— pero no se arregló el número, que era lo que había que
hacer.

*Origen:* buena práctica de Pablo, 30/08/2026.

---

## 59. Ninguna fila puede medir el doble que las otras

**En una tabla o en una leyenda, todas las filas tienen la misma altura.** Si un
texto parte en dos líneas, esa fila queda del doble de alto y es lo primero que
se ve — antes que cualquier número.

*Por qué pasa:* el ancho se reparte mal. Las columnas numéricas se quedan un
espacio que no usan —`USD 1.300.056` mide lo que mide y no crece— mientras la
columna de texto, que es la única que puede necesitarlo, queda ahogada. En una
tabla ancha no se nota; cuando la tabla comparte la lámina con un gráfico, sí.

*Cómo se arregla:* **la columna de texto se lleva lo que sobra y las numéricas
ocupan lo que miden.** En la cartera con gráfico al lado el reparto es
19% / 45% / 21% / 15%. Si aun así un nombre no entra, se acorta el nombre o se
agranda la tabla — nunca se acepta la fila doble.

*Lo mismo vale para la leyenda de un donut.* En una columna angosta, "Renta
variable" al costado del gráfico parte en dos. Apilada debajo, cada fila dispone
del ancho completo de la tarjeta.

*Cómo verificarlo:* extraer el texto de la página y mirar las filas. Cada fila de
datos tiene que salir en **una sola línea**, con su etiqueta y sus números
juntos. Si aparece una línea de texto suelta, sin monto ni porcentaje, ése es el
nombre partido. Medir las líneas de base no sirve en estas tablas: las celdas
comparten la matriz de texto y el desplazamiento de fila viaja en la matriz de
transformación.

*Origen:* lo detectó Pablo en la propuesta de Fernando, 30/08/2026.

---

## 60. Una barra sin pista de fondo, salvo que la escala sea 100%

**Si las barras escalan contra el valor más grande y no contra 100%, no llevan
pista gris de fondo.**

*Por qué:* una pista se lee como "lo que falta". Eso sólo es cierto cuando la
pista llena vale 100%. Si escala contra la fila más pesada, la pista completa
equivale a esa fila —18,9% en la cartera de Fernando— y entonces no representa
nada, pero el ojo igual la interpreta como el total.

*Cómo se rompió:* la fila de Cash, con 0,7%, quedó como un punto azul contra una
pista gris entera. Parecía que le faltaba el 99% de algo. La escala relativa era
la decisión correcta —contra 100% ninguna barra de una cartera de diez líneas se
distinguiría de las otras— pero arrastraba una pista que ya no tenía sentido.

*La regla general:* **cada elemento gráfico tiene que significar algo.** Un fondo,
una línea divisoria o un ícono que están "porque quedan bien" le dan al lector
una referencia falsa. Si no se puede decir en una frase qué representa, se saca.

*Y el reverso: nada puede significar algo que el dato no dice.* La paleta de
gráficos es sólo azules, navies y grises. **Nunca verde, rojo ni amarillo**: son
los colores de positivo, negativo y atención, y en una serie de categorías se
reparten por orden de aparición, sin relación con el contenido. En la
distribución por calificación crediticia el verde le tocó a "CCC y menor" — el
peor rating pintado con el color de "bien". Esos tres colores quedan reservados
para donde sí significan: pills de riesgo, comprar/vender, variaciones.

*Origen:* lo detectó Pablo en la propuesta de Fernando, 30/08/2026.

---

## 61. Elegir una ventana es decisión del asesor, nunca tuya por omisión

**Vos no elegís ventanas. Las mostrás todas, o le preguntás al asesor cuáles
van.** Él sí puede elegir: si considera que hay un período que vale la pena
destacar, está bien y es su criterio profesional.

*La diferencia es quién decidió.* Un asesor que dice "acá lo que importa son los
12 meses desde que reposicionamos, lo anterior es otra cartera" está haciendo su
trabajo, y esa selección tiene un argumento detrás que puede defender frente al
cliente. Una selección que aparece porque se tomaron las métricas que "quedaban
bien" no tiene ningún argumento: nadie la pensó, y no hay con qué sostenerla si
el cliente pregunta.

*Por qué importa tanto:* es el error más caro, porque no se descubre en la
reunión. Se descubre después, cuando el cliente mira el fact sheet completo y
encuentra la ventana que faltaba. Ahí no perdés el argumento: perdés la
confianza en todo lo demás que dijiste, incluido lo que estaba bien.

**Tu trabajo es que el asesor decida sabiendo.** Cuando cargues una comparación
contra benchmark, mirá **todas** las ventanas del fact sheet y decile cuáles
quedan afuera y qué dicen. Si él elige destacar una, listo. Lo que no puede
pasar es que la propuesta muestre tres de cinco ventanas y nadie se haya
enterado de las otras dos.

*Si se destaca una ventana, que se entienda por qué es esa.* "Desde el
reposicionamiento de marzo" se sostiene solo; "5 años" al lado de "desde inicio",
sin los períodos del medio, invita a la pregunta que no querés.

*Ojo con la versión disimulada:* sacar la palabra "alpha" y dejar `10,1%` al lado
de `Benchmark 8,9%` es la misma afirmación escrita distinto. El lector resta. Si
se saca la comparación, se saca entera —incluida la mención al benchmark en el
subtítulo—.

*Qué siempre se puede mostrar:* el rendimiento propio del producto, sin
comparación. Y las métricas de riesgo contra el benchmark, que son otra cosa:
describen el perfil, no reclaman haberle ganado a nadie.

*Cómo se rompió:* la lámina de CEDEARs de ETFs mostraba el alpha a 5 años
(+1,2pp) y desde inicio (+0,8pp). El de 3 años es **−1,2pp** y no figuraba. No
hubo intención de esconderlo, y ése es el punto: no hubo intención de nada. Al
avisarle, Pablo decidió sacar todas las comparaciones de rendimiento.

*Origen:* decisión de Pablo, 30/08/2026, y su corrección posterior el mismo día:
"tampoco tiene que ser algo tan rígido; si el asesor considera que hay un período
al que vale la pena meterle énfasis, está ok".

---

## 62. Ninguna slide desborda, y eso se mide en el navegador

**Antes de entregar, el generador mide cada slide y avisa si el contenido se
pasa.** `.slide` tiene `overflow:hidden`: lo que sobra se recorta o se encima con
el pie, y en las dos formas el defecto es invisible desde el JSON.

*Por qué no se puede estimar:* si entra o no depende de la fuente, del texto
real de cada etiqueta y de dónde cortó cada línea. Contar filas desde el JSON
falla siempre. La única medición honesta es sobre el documento ya maquetado, y
eso ya lo tenemos: el PDF se genera con Chromium, así que alcanza con preguntarle
al navegador antes de imprimir.

*Cómo funciona:* al generar un deck, el script compara el borde inferior de cada
elemento contra el techo del pie de página. Si algo se pasa, avisa por consola
con el número de slide, cuántos píxeles y **con qué texto empieza a encimarse**,
que es lo que permite encontrarlo sin abrir el PDF:

```
DESBORDE: slide 10 ('Mutual funds de renta fija') se pasa 10px del pie.
Empieza a encimarse en: "Por calificaciónAA29,0%BB18,9%B14,6%..."
```

*Qué hacer cuando salta:* sacar contenido o partir la slide en dos. **Nunca
achicar la tipografía hasta que entre** ni dejarlo recortado — ver criterio 35.
Lo más común es que sobre una tarjeta: seis KPIs envuelven a dos filas y empujan
todo lo de abajo.

*Cómo se rompió:* la lámina de mutual funds tenía seis tarjetas. La sexta pasó a
una segunda fila, corrió los gráficos hacia abajo y la distribución por
calificación terminó encimada con la nota al pie. Se generó el PDF sin que nada
avisara.

*Origen:* lo detectó Pablo en la propuesta de Fernando, 30/08/2026.

---

## 63. Un trade no se cuenta como un rebalanceo

Hay dos clases de movimiento y no se argumentan igual.

Un **rebalanceo por estrategia** se justifica contra el mandato, posición por
posición: esto se vende porque pesa de más, esto se compra porque falta. Cada
línea se sostiene sola y el formato natural son las tres columnas de comprar /
vender / mantener del capítulo `cartera_actual`.

Un **trade** es un canje: sale este bono, entra este otro. El argumento no está en
ninguno de los dos por separado sino en la comparación —mismo segmento, por qué
el que entra es mejor que el que sale—, así que **la venta y la compra tienen que
leerse juntas**. Partidas en dos columnas, el cliente tiene que adivinar qué va
con qué.

*Cómo:* capítulo `trades`, que emite la tabla de movimientos emparejados y, si hay
razones, una lámina con una columna por movimiento. La razón nunca va como quinta
columna de la tabla: el texto largo parte las filas en dos y rompe el criterio 59.

*De dónde salió:* en Jimena Laino se armó con comprar/vender, Pablo pidió
emparejarlo, y después hubo que recuperar los porqués en una slide aparte. Salió
bien y a mano; el catálogo no tenía el formato. 06/09/2026.

---

## 64. Dos números que contestan la misma pregunta no pueden convivir

Si el deck muestra dos cifras que el cliente va a leer como lo mismo, tienen que
coincidir o llamarse distinto. No alcanza con que cada una esté bien calculada en
su propio alcance.

*Caso:* la lámina de resumen decía "Resultado acumulado **+USD 9.319**" —el P&L de
tres años de toda la cartera, incluido lo ya cerrado— y dos slides después la
tabla de posiciones cerraba en "Resultado **+USD 11.205**", que es la ganancia no
realizada de lo que está hoy en cartera. Las dos correctas, con alcances
distintos, separadas por dos páginas y con el mismo rótulo.

*Qué hacer:* rotularlas por su alcance ("Resultado de las posiciones vigentes"
contra "Resultado acumulado"), o dejar una sola. Y si la diferencia importa,
pedirle al asesor los datos que faltan para reconciliarlas antes de emitir.

*Origen:* detectado en Jimena Laino, 06/09/2026.

---

## 65. Un instrumento no se confirma de memoria

Cuando el asesor tira un ticker o un nombre de producto y pregunta si es ése,
**la respuesta no sale de la memoria**. Se verifica contra una fuente o se dice
que no se puede confirmar.

*Caso:* Pablo preguntó "creo que es VNUS el que necesito, ¿no?". VNUS no existe
como UCITS; lo que existe es VNRA, Vanguard FTSE North America, que va justo para
el lado contrario del que buscaba. Confirmarlo de memoria habría metido el ticker
equivocado en una orden.

*Y la distinción fina también se verifica:* "MSCI World ex-USA" y "FTSE All-World
ex-US" suenan igual y no lo son —el primero excluye emergentes—. Elegir mal deja
un casillero entero del mandato sin cubrir.

*Qué sí se puede afirmar:* el ISIN, que es unívoco. El ticker de pantalla cambia
según el mercado donde liste. Y **si el instrumento está disponible en la
plataforma es dato de la casa**, no se deduce: ver criterio 34.

*Origen:* Jimena Laino, 06/09/2026.

---

## 66. La etiqueta de un gráfico no lleva puntos

Escribí "Acciones USA", no "Acciones EE.UU.", en cualquier `label` de donut o de
barras.

*Por qué:* hasta la v1.1 el generador pasaba el decimal a coma con un `replace`
sobre la cadena entera, etiqueta incluida, y "EE.UU." salía impreso "EE,UU,". El
bug está arreglado desde la v1.2 —`pct_coma()` formatea sólo el número— así que
hoy es seguro. Queda anotado porque el defecto pasó la validación, pasó la
generación del PDF y lo encontró Pablo mirando la lámina.

*El criterio general que deja:* cualquier formateo que se aplique a una cadena
armada tiene que tocar sólo la parte que corresponde. Si el `replace` está fuera
del `f-string` del número, está mal.

*Origen:* Jimena Laino, 06/09/2026.

---

## 67. Cuando hay dos carteras, cada slide dice cuál está mostrando

Una propuesta que aplica un aporte nuevo tiene **dos carteras conviviendo en el
mismo PDF**: la de hoy y la que queda después. Y varias slides se ven iguales —una
tabla de posiciones, un donut por clase de activo, una fila de tarjetas—, así que
sin rótulo el cliente no sabe cuál está mirando.

**El rótulo va en el título, no en la bajada ni al pie.** Es donde el lector ya
tiene puesto el ojo, y es lo primero que necesita para leer el resto de la slide.

**Y el par tiene que usar la misma palabra en los dos lados.** "Hoy" contra
"Después de la operación" obliga a traducir de una slide a la otra; *pre aporte*
contra *post aporte* se lee sin pensar. Elegí un par y sostenelo.

*Por qué importa más de lo que parece:* con dos carteras cambia la base de los
porcentajes. En Jimena Laino el oro pasó de **5,4% a 4,3% sin que se vendiera un
solo gramo** — la posición quedó igual en USD 5.207 y lo que creció fue el
denominador, de 95.547 a 120.547. Un cliente que compara las dos cifras sin saber
que son de carteras distintas lee una venta que nunca ocurrió.

*Lo mismo vale para el resultado.* Una cifra medida sobre la cartera vigente y
otra sobre la resultante no son comparables aunque se llamen igual — ver criterio
64.

*Origen:* pedido de Pablo, 06/09/2026: "las slides que son pre-aporte habría que
indicarlas también porque es un lío si no entender". Quedaron como "Cómo está
compuesta, pre aporte", "El detalle, pre aporte", "Cómo queda la cartera, post
aporte" y "El detalle, post aporte".
