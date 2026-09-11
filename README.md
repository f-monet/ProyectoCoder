# Rolling Stones — Dashboard de Discografía

Página para controlar la colección de discos de The Rolling Stones. Versión actual: **v1.2** (visible al pie de la página).

## Qué es

Página web estática (HTML + CSS + JS, sin backend) con dos vistas:

**The Rolling Stones (banda)**
- Álbumes de estudio 1964-2026, con ediciones UK/US separadas cuando el título o tracklist difiere (Decca, London Records, ABKCO, Rolling Stones Records, etc.)
- Álbumes en vivo 1966-2024, incluyendo lanzamientos "de archivo" editados muchos años después del show
- Recopilatorios, desde el primero (1966) hasta On Air (2017)
- Singles y EPs, 1963-2026
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

## Historial de versiones

- **v1.2**: agrega "Foreign Tongues" (2026, álbum de estudio nuevo + singles + box), "On Air" (2017, estándar y deluxe), "A Bigger Bang: Live on Copacabana Beach" (2021), "Live at the Wiltern" (2024), "Live At Racket, NYC" (2024), "Welcome to Shepherd's Bush" (2024), la reedición de "Main Offender" de Keith Richards (2026) y "Fearless: Anthology 1965-2025" de Ron Wood. Se agrega el número de versión visible al pie de la página.
- **v1.1**: primera carga completa — discografía de la banda (estudio, vivo, recopilatorios, singles/EPs, bootlegs, box sets) + discografía solista de los 8 integrantes/afines.
- **v1.0**: primera aproximación del dashboard, con datos de ejemplo.

## Próximos pasos

- v1.3: mover el guardado de "tengo/no tengo" a la nube, para que no dependa del navegador/dispositivo.
- Revisar y corregir la data cargada (puede tener errores u omisiones).
- La lista de bootlegs es una selección curada, no exhaustiva — se puede seguir ampliando.
- Podría faltar alguna edición regional muy específica (compilados solo-mercado, variantes de vinilo de los 70s/80s, etc.) — se agregan a medida que se detecten.

