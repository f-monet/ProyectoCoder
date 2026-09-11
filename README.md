# Rolling Stones — Dashboard de Discografía

Primera aproximación de una página para controlar la colección de discos de The Rolling Stones.

## Qué es

Página web estática (HTML + CSS + JS, sin backend) con:

- Listado de álbumes (estudio, en vivo, recopilatorios) con año y tipo.
- Checkbox para marcar qué discos ya tenés.
- Formato (Vinilo / CD / Digital / Cassette) y notas por disco.
- Buscador y filtros por tipo.
- Estadísticas de progreso (total, en colección, faltantes, % completado).
- Diseño responsive, pensado para verse bien desde el celular.

Los datos de ejemplo están en `data.js` (discografía base) y el estado de "tengo/no tengo" se guarda en el navegador (`localStorage`), por dispositivo.

## Cómo verla

Abriendo `index.html` en cualquier navegador (no necesita instalación ni servidor).

Para acceder desde el celular vía internet, se puede publicar con **GitHub Pages**:
1. En GitHub → Settings → Pages.
2. Source: Deploy from a branch → elegir la rama y carpeta `/ (root)`.
3. GitHub genera una URL pública (tipo `https://usuario.github.io/proyectocoder/`) accesible desde cualquier dispositivo.

## Próximos pasos

Falta cargar la información definitiva de la discografía (lista completa, ediciones, formatos específicos) y ajustar las características del dashboard según lo que se necesite controlar.

