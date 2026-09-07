# Equipo — datos de contacto

Directorio interno para completar el bloque de contacto de las propuestas.

**Antes de generar, preguntale al asesor quiénes van en los datos de contacto.**
No lo deduzcas de quién te está hablando: la mayoría trabaja en dupla y el
cliente tiene que poder escribirle a los dos. Ver criterio 43.

| Nombre | Email | Teléfono |
|---|---|---|
| Delfina Mitre | dmitre@max.capital | 11 3140 3595 |
| Gimena Neveleff | gneveleff@max.capital | 11 2875 0278 |
| Juan Esteban Muñoz | jmunoz@max.capital | 11 4960 8686 |
| Marcos Sanchez Negrete | msancheznegrete@max.capital | 11 2251 5949 |
| Maricel Mega | mmega@max.capital | 11 3683 7121 |
| Nicolás Horacio Alderete Duggan | nalderete@max.capital | 11 6210 0499 |
| Pablo Haro | pharo@max.capital | 11 6235 3857 |
| Santiago Polak | spolak@max.capital | 11 5024 5469 |
| Segundo Smith Estrada | ssmith@max.capital | 11 4937 8629 |

## Notas

- Los teléfonos van **tal como los usa el equipo**, sin prefijo de país. Si
  alguna propuesta necesita formato internacional, se agrega en el JSON de esa
  propuesta, no acá.
- Si falta un dato de alguien, el bloque sale sin él. No se inventa un número ni
  se reutiliza el de otra propuesta.
- Si aparece alguien que no está en esta tabla, pedile el dato al asesor y
  agregalo acá — no lo pongas sólo en el JSON de esa propuesta.

## Cómo se cargan en la propuesta

Un solo contacto:

```json
"asesor": { "nombre": "Pablo Haro", "email": "pharo@max.capital",
            "telefono": "11 6235 3857" }
```

Varios, que es el caso habitual:

```json
"asesores": [
  { "nombre": "Pablo Haro", "email": "pharo@max.capital", "telefono": "11 6235 3857" },
  { "nombre": "Marcos Sanchez Negrete", "email": "msancheznegrete@max.capital", "telefono": "11 2251 5949" }
]
```

El orden importa: el primero es quien encabeza la relación y es el que aparece
en el bloque "Presentado por" de la portada.

**El área no se carga**: todos son Wealth Management y el generador lo pone solo
(`CONFIG["AREA"]`). Sólo hace falta el campo `cargo` si alguna vez firma alguien
de otra área.