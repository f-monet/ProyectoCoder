# Rolling Stones — Dashboard de Discografía

Primera aproximación de una página para controlar la colección de discos de The Rolling Stones.

## Qué es

Página web estática (HTML + CSS + JS, sin backend) con dos vistas:

**The Rolling Stones (banda)**
- Álbumes de estudio 1964-2023, con ediciones UK/US separadas cuando el título o tracklist difiere (Decca, London Records, ABKCO, Rolling Stones Records, etc.)
- Álbumes en vivo 1966-2023
- Recopilatorios, desde el primero (1966) hasta Honk (2019)
- Singles y EPs, 1963-2023
- Bootlegs de interés para coleccionistas (selección curada, ampliable)
- Box sets, cada uno con su propio checkbox aunque reedite un álbum ya cargado

**Discografía Solista** — Mick Jagger, Keith Richards, Bill Wyman, Charlie Watts, Ron Wood, Mick Taylor, Andrew Loog Oldham y Brian Jones, con sus álbumes de estudio, en vivo y box sets.

Cada disco tiene: checkbox de "lo tengo", región, sello discográfico (para la banda), formato (Vinilo/CD/Digital/Cassette) y notas. Hay buscador, filtros por tipo, y estadísticas de progreso (total, en colección, faltantes, % completado) calculadas sobre la vista/filtro actual.

Los datos están en `data.js` y el estado de "tengo/no tengo" se guarda en el navegador (`localStorage`), por dispositivo.

## Cómo verla

Abriendo `index.html` en cualquier navegador (no necesita instalación ni servidor).

Para acceder desde el celular vía internet, se puede publicar con **GitHub Pages**:
1. En GitHub → Settings → Pages.
2. Source: Deploy from a branch → elegir la rama y carpeta `/ (root)`.
3. GitHub genera una URL pública (tipo `https://usuario.github.io/proyectocoder/`) accesible desde cualquier dispositivo.

## Próximos pasos

- Revisar y corregir la data cargada (es investigación de v1, puede tener errores u omisiones).
- La lista de bootlegs es una selección curada, no exhaustiva — se puede seguir ampliando.
- Podría faltar alguna edición regional muy específica (compilados solo-mercado, variantes de vinilo de los 70s/80s, etc.) — se agregan a medida que se detecten.

