#!/usr/bin/env python3
"""
Max Capital — Generador de Propuestas de Inversión.

Toma un JSON normalizado (la "propuesta") y emite un PDF on-brand en uno de
tres formatos. La idea de fondo: el asesor y Claude discuten el CONTENIDO en
lenguaje natural, y este script se encarga de TODO el diseño. Nadie toca
colores, tipografías ni layout a mano.

    python generate_propuesta.py --json propuesta.json --formato deck      --out d.pdf
    python generate_propuesta.py --json propuesta.json --formato onepager  --out o.pdf
    python generate_propuesta.py --json propuesta.json --formato documento --out c.pdf

Flags:
    --design-html <ruta>  exporta el HTML con datos reales (para Claude Design)
    --validar             revisa el JSON y reporta problemas, sin renderizar
    --assets <dir>        carpeta de recursos (default: ../assets)

El contrato del JSON está documentado en reference/esquema.md y el catálogo de
capítulos en reference/capitulos.md.
"""

import argparse
import base64
import html
import json
import math
import os
import re
import sys
import tempfile

# ============================ CONFIG (criterios) ============================ #
# Los criterios del equipo viven acá. Cambiar un criterio = cambiar una línea.
CONFIG = {
    # --- Paginación automática -------------------------------------------- #
    # Una slide 16:9 no puede crecer: si un capítulo trae más filas/fichas que
    # esto, el generador lo parte en varias slides con "(cont.)" en el título,
    # en vez de dejar que el contenido se desborde fuera de la hoja.
    "FILAS_POR_SLIDE": 13,
    "FILAS_POR_SLIDE_DENSA": 19,
    "FICHAS_POR_SLIDE": 6,
    "PASOS_POR_SLIDE": 6,

    # A partir de esta cantidad de filas/fichas la slide entra en modo denso
    # (tipografía y padding proporcionalmente más chicos).
    "UMBRAL_DENSO": 9,

    # --- One-pager --------------------------------------------------------- #
    # El one-pager es UNA hoja. Según cuántas filas tenga la cartera, se aplica
    # compresión progresiva antes que permitir un desborde.
    # Umbrales más bajos que antes: desde que las distribuciones van debajo de la
    # tabla (y no al costado), el contenido se apila y la altura se consume más
    # rápido, así que la compresión tiene que entrar antes.
    "OP_FILAS_TIGHT": 7,
    "OP_FILAS_TIGHTER": 11,

    # La nota de instrumentos es una línea por vehículo: pasado este largo se
    # recorta, porque dos líneas por fondo empujan el bloque contra el pie.
    "OP_NOTA_MAX_CARACTERES": 150,
    # Más filas que esto no entran de forma legible en una sola hoja: el script
    # avisa y sugiere el deck. No trunca en silencio.
    "OP_FILAS_MAXIMO": 22,

    # --- Gráficos ---------------------------------------------------------- #
    # Paleta de las distribuciones. Es una escala de azules de marca + acentos;
    # el orden importa porque las categorías se pintan en el orden en que vienen.
    # Sólo azules, navies y grises. Nada de verde, rojo ni amarillo: son los
    # colores de positivo, negativo y atención, y en una serie de categorías se
    # aplican por orden, sin relación con el significado. En la distribución por
    # calificación crediticia el verde le tocó a "CCC y menor" —el peor rating
    # con el color de "bien"—. Ver criterio 60.
    "COLORES_GRAFICO": ["#006FEE", "#0B2545", "#6BA8F7", "#00396F", "#99C5FA",
                        "#71717A", "#CCE3FD", "#3F5A78", "#A1A1AA", "#D4D4D8"],
    # Con más categorías que esto, el donut se vuelve ilegible y conviene barras.
    "DONUT_MAX_CATEGORIAS": 7,

    # --- Textos fijos ------------------------------------------------------ #
    # ADAPTACIÓN del disclaimer oficial de informes de Max Capital S.A.
    # ------------------------------------------------------------------
    # El texto de informes arranca diciendo que el documento "no constituye
    # recomendación". Una PROPUESTA sí lo es: recomienda instrumentos concretos
    # para un cliente concreto. Sostener esa frase acá sería contradecir el
    # contenido del propio PDF.
    #
    # Cambios respecto del original, y son los únicos:
    #   1. El primer párrafo reconoce que hay recomendación y la funda en el
    #      perfil que aportó el cliente. Se conserva que no es oferta pública.
    #   2. "informe" -> "documento", por coherencia.
    #   3. Se agrega un párrafo sobre proyecciones: una propuesta proyecta
    #      rendimientos, un informe reporta lo ya ocurrido.
    # No se quitó ninguna cláusula del original.
    #
    # Este es el texto vigente para propuestas. No se edita por propuesta: si
    # hace falta un cambio, se cambia acá y vale para todas.
    "DISCLAIMER": (
        "El presente documento contiene recomendaciones de inversión elaboradas por Max "
        "Capital S.A. sobre la base de la información aportada por su destinatario respecto "
        "de sus objetivos de inversión, horizonte temporal y tolerancia al riesgo. No "
        "constituye una oferta ni una invitación dirigida al público para la compra o venta "
        "de los valores negociables y/o de los instrumentos financieros mencionados en él, y "
        "no debe ser considerado un prospecto de emisión u oferta pública. El destinatario "
        "deberá evaluar por sí mismo la conveniencia de la inversión en los valores "
        "negociables o instrumentos financieros mencionados y deberá basarse en la "
        "investigación personal que considere pertinente realizar. Algunos de los valores "
        "negociables bajo análisis pueden no estar autorizados a ser ofrecidos públicamente "
        "en la República Argentina. Aunque la información contenida en el presente documento "
        "ha sido obtenida de fuentes que Max Capital S.A. considera confiables, tal "
        "información puede ser incompleta o parcial y Max Capital S.A. no ha verificado en "
        "forma independiente la información contenida, ni garantiza la exactitud de la "
        "información, o que no se hayan producido cambios en la situación (económica, "
        "financiera o de otro tipo) relativa a los emisores descripta en este documento. Max "
        "Capital S.A. no asume responsabilidad alguna, explícita o implícita, en cuanto a la "
        "veracidad o suficiencia de la misma para efectuar la toma de decisión de su "
        "inversión. Ninguna persona ni funcionario de Max Capital S.A. ha sido autorizada a "
        "suministrar información adicional a la contenida en este documento. Los rendimientos "
        "y proyecciones expuestos constituyen estimaciones elaboradas sobre supuestos de "
        "mercado y no representan rendimientos garantizados ni resultados asegurados; los "
        "rendimientos pasados no garantizan rendimientos futuros. Todas las opiniones o "
        "estimaciones vertidas en el presente documento constituyen nuestro juicio y pueden "
        "ser modificadas sin previo aviso. Asimismo, bajo ningún concepto podrá entenderse "
        "que Max Capital S.A. asegura y/o garantiza resultado alguno en relación a posibles "
        "inversiones en valores negociables o instrumentos financieros mencionados en el "
        "presente documento, siendo el destinatario del mismo plenamente consciente de los "
        "riesgos inherentes a la actividad bursátil y/o financiera, incluida la pérdida del "
        "capital invertido. Consecuencia de lo reseñado, el destinatario desiste de realizar "
        "reclamo alguno a Max Capital S.A., por eventuales daños y perjuicios que pudiera "
        "padecer, sustentando su reclamo en la información brindada por el presente "
        "documento."),

    # Pie de cada slide: corto, porque se repite en todas.
    "FOOTER_BRAND": "Max Capital S.A. | ©2026 | Todos los derechos reservados.",

    # Área de los asesores. Es siempre la misma, así que no se carga por
    # propuesta ni se pregunta: se usa como valor por defecto del campo `cargo`.
    "AREA": "Wealth Management",

    # Matrículas completas, texto oficial. Va una sola vez por documento, junto
    # al disclaimer: en el pie de cada slide no entra en una línea y repetirlo
    # nueve veces no agrega nada.
    "LEYENDA_REGULATORIA": (
        "Agente de Liquidación y Compensación y AN Propio N° 570/CNV. Agente de "
        "Administración de Productos de Inversión Colectiva - Fiduciario Financiero "
        "Nº 78/CNV. Agente de Colocación y Distribución Integral de Fondos Comunes de "
        "Inversión N° 13/CNV y Agente de Colocación y Distribución de Fondos Comunes "
        "de Inversión Nº 60/CNV."),
}

COLORES = CONFIG["COLORES_GRAFICO"]


# ============================== Utilidades ================================= #

def esc(s):
    """Escapa para HTML. None -> cadena vacía, para que un campo faltante no
    rompa el render ni imprima 'None' en el PDF."""
    return html.escape(str(s)) if s is not None else ""


def esc_md(s):
    """Como esc(), pero deja pasar **negrita**.

    Se escapa TODO primero y recién después se convierte el marcador, así que
    no hay forma de inyectar HTML desde el JSON: lo único que sobrevive es el
    <b>. Sirve para destacar la frase que sostiene un argumento sin partir el
    párrafo en dos.
    """
    t = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t, flags=re.S)


def get(d, *claves, default=None):
    """Lee la primera clave presente. Los asesores (y Claude) escriben las
    claves de formas distintas ('valor'/'value', 'titulo'/'title'); aceptar
    sinónimos evita que la propuesta falle por un nombre."""
    if not isinstance(d, dict):
        return default
    for k in claves:
        if k in d and d[k] not in (None, ""):
            return d[k]
    return default


def a_numero(v):
    """Convierte '12,5%' / 'USD 20.000' / 20000 a float. Devuelve None si no
    hay número reconocible. Acepta formato español (1.234,56) e inglés."""
    if isinstance(v, (int, float)):
        return float(v)
    if v is None:
        return None
    s = str(v).strip()
    s = re.sub(r"[^\d,.\-]", "", s)
    if not s or s in ("-", ".", ","):
        return None
    # Si tiene ambos separadores, el último que aparece es el decimal.
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        # Coma sola: decimal si deja <=2 dígitos a la derecha, si no, de miles.
        ent, _, dec = s.rpartition(",")
        s = f"{ent.replace(',', '')}.{dec}" if len(dec) <= 2 else s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def clase_riesgo(v):
    """Mapea un nivel de riesgo a la pill correspondiente.

    Acepta las dos familias de vocabulario que conviven en el material del
    equipo: "Bajo / Medio / Alto" en las propuestas y "Conservador / Moderado /
    Agresivo" en los fact sheets. Sin esto, un fondo etiquetado "Moderado"
    salía como texto pelado, sin pastilla.
    """
    s = (str(v or "")).strip().lower()
    if s.startswith(("baj", "conserv")):
        return "bajo"
    if s.startswith(("med", "mod")):
        return "medio"
    if s.startswith(("alt", "agres")):
        return "alto"
    return ""


def pct_coma(pct):
    """Un porcentaje con un decimal y coma decimal: 52,3%.

    Existe para que la conversión toque sólo el número. Antes se hacía con un
    `.replace(".", ",")` sobre la cadena entera —etiqueta incluida— y cualquier
    punto del rótulo se convertía en coma: "EE.UU." salía impreso "EE,UU,"."""
    return f"{pct:.1f}%".replace(".", ",")


def clase_signo(v):
    """Colorea un valor según su signo, para que un resultado negativo se lea
    como negativo sin que nadie tenga que marcarlo."""
    s = str(v or "").strip()
    if s.startswith("-") or s.startswith("−"):
        return "neg"
    if s.startswith("+"):
        return "pos"
    return ""


MESES_ABREV = ["ene", "feb", "mar", "abr", "may", "jun",
               "jul", "ago", "sep", "oct", "nov", "dic"]


def mes_anio(fecha):
    """Convierte '27/08/2026' en 'ago/2026'.

    Una propuesta se fecha por mes: el día exacto en que se armó no le dice nada
    al cliente y envejece el documento más rápido de lo que corresponde. Si el
    valor no tiene formato de fecha se devuelve tal cual, así el asesor puede
    escribir directamente 'ago/2026' o un período propio.
    """
    if not fecha:
        return ""
    m = re.match(r"^\s*(\d{1,2})[/-](\d{1,2})[/-](\d{4})\s*$", str(fecha))
    if m:
        _, mes, anio = m.groups()
        if 1 <= int(mes) <= 12:
            return f"{MESES_ABREV[int(mes) - 1]}/{anio}"
    return str(fecha)


def asesores_de(p):
    """Los contactos de la propuesta, siempre como lista.

    Acepta `asesores` (lista) o `asesor` (uno solo). En Max Capital lo habitual
    es trabajar en dupla, así que el cliente tiene que poder escribirle a los
    dos: preguntá siempre quiénes van, no lo deduzcas de quién te habla.
    """
    lst = get(p, "asesores", "contactos", default=None)
    if lst:
        return lst if isinstance(lst, list) else [lst]
    uno = get(p, "asesor", default=None)
    return [uno] if uno else []


def trozos(lista, n):
    """Parte una lista en bloques de n. Base de la paginación automática."""
    return [lista[i:i + n] for i in range(0, len(lista), n)] or [[]]


# ============================ Gráficos (SVG) =============================== #

def donut(items, tamano=118, grosor=22):
    """Donut de distribución. `items` es [(label, valor)] donde valor puede ser
    número o texto con %. Los valores se normalizan sobre el total, así que
    funciona igual si vienen en % (suman 100) o en montos absolutos."""
    vals, labels = [], []
    for it in items:
        labels.append(get(it, "label", "etiqueta", "categoria", "nombre", default=""))
        vals.append(a_numero(get(it, "valor", "value", "pct", "peso", "monto")) or 0.0)
    total = sum(vals) or 1.0

    r = 70.0

    # Cada gajo es un arco <path> propio. Antes se dibujaban como circles con
    # stroke-dasharray, pero el último gajo terminaba justo sobre la costura
    # donde el path abre y cierra: el navegador lo trazaba cruzando ese punto y
    # le aplicaba un join, que salía como una punta hacia afuera del anillo.
    # Con arcos explícitos no hay costura que cruzar. Ver criterio 54.
    def punto(frac):
        ang = frac * 2 * math.pi - math.pi / 2     # 0 = las 12 en punto
        return f"{r * math.cos(ang):.4f} {r * math.sin(ang):.4f}"

    anillos = [f'<circle r="{r}" cx="0" cy="0" fill="none" stroke="#F4F4F5" '
               f'stroke-width="{grosor}"/>']
    acc = 0.0
    for i, v in enumerate(vals):
        f = (v / total) if total else 0.0
        color = COLORES[i % len(COLORES)]
        if f <= 0:
            continue
        if f >= 0.9999:
            # Un único gajo del 100%: un arco de 360° no dibuja nada porque
            # empieza y termina en el mismo punto. Va el círculo entero.
            anillos.append(f'<circle r="{r}" cx="0" cy="0" fill="none" '
                           f'stroke="{color}" stroke-width="{grosor}"/>')
        else:
            anillos.append(
                f'<path d="M {punto(acc)} A {r} {r} 0 {1 if f > 0.5 else 0} 1 '
                f'{punto(acc + f)}" fill="none" stroke="{color}" '
                f'stroke-width="{grosor}"/>')
        acc += f

    svg = (f'<svg viewBox="0 0 180 180" width="{tamano}" height="{tamano}" '
           f'xmlns="http://www.w3.org/2000/svg">'
           f'<g transform="translate(90,90)">{"".join(anillos)}</g></svg>')

    # Si los valores ya vienen en porcentaje —suman ~100— la leyenda muestra el
    # que escribió el asesor, no uno recalculado. Recalcular sobre el total
    # reintroduce el redondeo y hace que la leyenda contradiga al KPI de la
    # misma slide: 52,3% arriba y 52,2% abajo. Ver criterio 57.
    ya_es_pct = 99.0 <= total <= 101.0
    filas = []
    for i, (lb, v) in enumerate(zip(labels, vals)):
        pct = v if ya_es_pct else v / total * 100
        filas.append(
            f'<div class="donut-legend-row"><span>'
            f'<span class="dot" style="background:{COLORES[i % len(COLORES)]};"></span>'
            # El decimal se pasa a coma SÓLO sobre el número: aplicarlo a toda la
            # cadena se comía los puntos de la etiqueta y "EE.UU." salía "EE,UU,".
            f'{esc(lb)}</span><span>{pct_coma(pct)}</span></div>')
    return svg, "".join(filas)


def barras(items, normalizar=True):
    """Barras horizontales.

    `normalizar=True` (default) trata los valores como partes de un todo y los
    reparte sobre el total: es lo correcto para una distribución.

    `normalizar=False` los muestra tal cual, con la barra medida sobre 100. Hace
    falta cuando las barras comparan magnitudes INDEPENDIENTES —un antes contra
    un después, dos carteras distintas— donde sumarlas no significa nada.
    Normalizar ahí deforma los números: 63,9% y 38,8% se convertirían en 62,2% y
    37,8% sólo porque suman 102,7.
    """
    vals, labels = [], []
    for it in items:
        labels.append(get(it, "label", "etiqueta", "categoria", "nombre", default=""))
        vals.append(a_numero(get(it, "valor", "value", "pct", "peso", "monto")) or 0.0)
    total = sum(vals) or 1.0
    out = []
    for i, (lb, v) in enumerate(zip(labels, vals)):
        pct = (v / total * 100) if normalizar else v
        ancho = min(max(pct, 0), 100)
        out.append(
            f'<div class="bar-row"><div class="bar-head"><span>{esc(lb)}</span>'
            f'<b>{pct_coma(pct)}'
            f'</b></div><div class="bar-track"><div class="bar-fill" '
            f'style="width:{ancho:.2f}%;background:{COLORES[i % len(COLORES)]};">'
            f'</div></div></div>')
    return f'<div class="bars">{"".join(out)}</div>'


def grafico(g, tamano=118):
    """Elige donut o barras según lo que pidió el capítulo y cuántas categorías
    hay. Un donut de 12 gajos no se lee; en ese caso caen a barras solas."""
    titulo = get(g, "titulo", "title", default="")
    items = get(g, "items", "datos", default=[]) or []
    tipo = (get(g, "tipo", "type", default="") or "").lower()
    if not tipo:
        tipo = "barras" if len(items) > CONFIG["DONUT_MAX_CATEGORIAS"] else "donut"
    # `normalizar: false` en el gráfico -> los valores se muestran tal cual.
    normalizar = get(g, "normalizar", default=None)
    normalizar = True if normalizar is None else bool(normalizar)
    cuerpo = (barras(items, normalizar) if tipo.startswith("barra")
              else '<div class="donut-row">%s<div class="donut-legend">%s</div></div>'
                   % donut(items, tamano=tamano))
    return f'<div class="donut-card"><h4>{esc(titulo)}</h4>{cuerpo}</div>'


# ============================ Bloques reusables ============================ #

def kpi(item):
    label = get(item, "label", "etiqueta", "titulo", default="")
    valor = get(item, "valor", "value", default="")
    nota = get(item, "nota", "note", "detalle", default="")
    # Valor secundario: sirve para dar el equivalente nominal cuando la cifra
    # principal está en moneda constante. Sin él, un rendimiento real se lee
    # como flojo y nadie sabe que ya tiene la inflación descontada.
    secundario = get(item, "valor_nominal", "valor_secundario", default="")
    cls = " accent" if get(item, "accent", "destacado", default=False) else ""
    h = f'<div class="kpi{cls}"><span class="k-label">{esc(label)}</span>' \
        f'<span class="k-value">{esc(valor)}</span>'
    if secundario:
        h += f'<span class="k-alt">{esc(secundario)}</span>'
    if nota:
        h += f'<span class="k-note">{esc(nota)}</span>'
    return h + "</div>"


# Columnas por defecto del detalle de cartera. Sale del modelo "Propuesta de
# Inversión PH": son las que el equipo ya usa y el cliente ya sabe leer.
COLUMNAS_CARTERA = [
    ("clase", "Clase de Activo", "l"),
    ("descripcion", "Descripción", "l"),
    ("riesgo", "Nivel de Riesgo", "c"),
    ("rendimiento", "Rendimiento esperado", "r"),
    ("plazo", "Plazo de inversión", "c"),
    ("monto", "Monto a invertir", "r"),
]

# Encabezados y alineación de las columnas que el equipo usa además de las de
# arriba. Tenerlos acá evita títulos auto-generados sin tilde ("Ponderacion")
# y que una columna numérica salga alineada a la izquierda.
COLUMNAS_EXTRA = {
    "ponderacion": ("Ponderación", "r"),
    "geografia": ("Geografía", "c"),
    "custodia": ("Custodia", "c"),
    "duration": ("Duration", "r"),
    "vencimiento": ("Vencimiento", "c"),
    "tir": ("TIR", "r"),
    "moneda": ("Moneda", "c"),
    "precio": ("Precio", "r"),
    "nominal": ("Nominal", "r"),
    "trailer": ("Trailer", "r"),
}

SINONIMOS = {
    "clase": ("clase", "clase_activo", "asset_class", "tipo"),
    "descripcion": ("descripcion", "instrumento", "nombre", "detalle", "descripción"),
    "riesgo": ("riesgo", "nivel_riesgo", "nivel_de_riesgo"),
    "rendimiento": ("rendimiento", "rendimiento_esperado", "tir", "ytm", "retorno"),
    "plazo": ("plazo", "plazo_inversion", "horizonte", "vencimiento"),
    "monto": ("monto", "monto_a_invertir", "importe", "nominal"),
    "ponderacion": ("ponderacion", "peso", "ponderación", "participacion", "%"),
    "geografia": ("geografia", "geografía", "region", "país", "pais"),
    "custodia": ("custodia", "custodio"),
}


def celda(item, clave):
    return get(item, *SINONIMOS.get(clave, (clave,)), default="")


def _pct(v):
    """Lee '18,1%' o 18.1 y devuelve float. None si no parece un porcentaje."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).strip().replace("%", "").replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def controlar_cierre(c, etiqueta, avisos):
    """Avisa cuando una tabla de cartera no cierra.

    El invariante no es "los porcentajes suman 100": es **que la tabla cierre
    con su propio total**. Una tabla de posiciones a vender es un subconjunto y
    sus pesos son sobre la cartera entera — ahí la suma correcta es 40,4%, no
    100%. Lo que nunca puede pasar es que las filas digan una cosa y la fila de
    total otra.

    No corrige solo. Rebasear sobre el total real o repartir la diferencia por
    resto mayor cambia números que el asesor eligió, y esa decisión es suya.
    Ver criterio 58."""
    items = get(c, "items", "posiciones", "instrumentos", default=[]) or []
    if not items:
        return
    total = get(c, "total", default=None)
    pcts = [_pct(get(it, "ponderacion", "peso", "pct", default=None)) for it in items]
    pcts = [x for x in pcts if x is not None]

    if len(pcts) >= 2:
        suma = round(sum(pcts), 1)
        esperado = _pct(get(total, "ponderacion", "peso", default=None)) if total else None
        if esperado is None:
            # Sin fila de total, el único cierre posible es el 100%.
            if abs(suma - 100.0) > 0.05:
                avisos.append(
                    f"{etiqueta}: los porcentajes suman {suma:.1f}% y la tabla no "
                    f"tiene fila de total. Agregá el total, o ajustá los pesos "
                    f"para que cierren en 100%.")
            else:
                avisos.append(f"{etiqueta}: la tabla no tiene fila de total. "
                              f"Una tabla con porcentajes siempre la lleva.")
        elif abs(suma - esperado) > 0.05:
            avisos.append(
                f"{etiqueta}: los porcentajes de las filas suman {suma:.1f}% pero "
                f"la fila de total dice {esperado:.1f}%. Preguntale al asesor si "
                f"ajusta —rebasear sobre el total real, o repartir la diferencia "
                f"por resto mayor—. No lo cambies por tu cuenta.")

    if total:
        montos = [_num(get(it, "monto", "valuacion", default=None)) for it in items]
        montos = [x for x in montos if x is not None]
        dec = _num(get(total, "monto", "valuacion", default=None))
        if montos and dec is not None and abs(sum(montos) - dec) > 0.5:
            avisos.append(
                f"{etiqueta}: la fila de total dice "
                f"{get(total, 'monto', default='')} pero las filas suman "
                f"{sum(montos):,.0f}".replace(",", ".") +
                ". Una tabla tiene que cerrar con su propio total.")


def _num(v):
    """Lee 'USD 1.300.056' y devuelve float. None si no hay número."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    t = "".join(ch for ch in str(v) if ch.isdigit() or ch in ",.-")
    t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def _fila_subtotal(cols, grupo, agrupar):
    """Fila de subtotal de un grupo. Suma monto y ponderación de sus filas.

    Un grupo de una sola línea no lleva subtotal: repetiría el mismo número dos
    veces seguidas. Lo decide quien llama."""
    if len(grupo) < 2:
        return ""
    monto = sum(_num(get(it, "monto", "valuacion", default=None)) or 0.0 for it in grupo)
    peso = sum(_pct(get(it, "ponderacion", "peso", "pct", default=None)) or 0.0 for it in grupo)
    tds = []
    for clave, _, al in cols:
        base = f"{al} col-{esc(clave)}"
        if clave == "descripcion":
            v = "Subtotal"
        elif clave == "monto":
            v = "USD " + f"{monto:,.0f}".replace(",", ".")
        elif clave == "ponderacion":
            v = f"{peso:.1f}%".replace(".", ",")
        else:
            v = ""
        tds.append(f'<td class="{base}">{esc(v)}</td>')
    return f'<tr class="subtotal">{"".join(tds)}</tr>'


def tabla_cartera(items, columnas=None, total=None, denso=False, agrupar=None,
                  subtotales=False):
    """Renderiza el detalle de la cartera. `columnas` permite al capítulo elegir
    qué mostrar (una propuesta de bonos quiere 'duration' y una de fondos
    'custodia'), pero por defecto usa el set que ya usa el equipo."""
    cols = []
    if columnas:
        for c in columnas:
            if isinstance(c, dict):
                cols.append((get(c, "clave", "key", default=""),
                             get(c, "titulo", "label", default=""),
                             get(c, "align", "alineacion", default="l")))
            else:
                match = next((x for x in COLUMNAS_CARTERA if x[0] == c), None)
                if match is None and c in COLUMNAS_EXTRA:
                    match = (c, COLUMNAS_EXTRA[c][0], COLUMNAS_EXTRA[c][1])
                cols.append(match or (c, c.replace("_", " ").capitalize(), "l"))
    else:
        cols = list(COLUMNAS_CARTERA)

    # La clave viaja como clase CSS (col-descripcion, col-monto…) para que la
    # hoja de estilos pueda dar ancho a la descripción y evitar que las columnas
    # numéricas cortas se partan en varias líneas.
    th = "".join(f'<th class="{al} col-{esc(k)}">{esc(tit)}</th>' for k, tit, al in cols)

    # La columna `barra` dibuja el peso de cada fila. Se escala contra la fila
    # más pesada y no contra 100%: con carteras de diez líneas ninguna pasa del
    # 20%, y contra 100% todas las barras quedarían igual de cortas y no se
    # compararían entre sí, que es justamente para lo que están.
    pesos = [_pct(get(it, "ponderacion", "peso", "pct", default=None)) or 0.0
             for it in items]
    tope = max(pesos) if pesos else 0.0

    filas = []
    grupo_acc = []           # filas del grupo en curso, para su subtotal
    previo = None            # último valor impreso de la columna agrupada
    for it in items:
        tds = []
        # `agrupar` escribe el valor sólo en la primera fila de cada corrida.
        # Diez filas que dicen "Renta fija" no informan diez veces: informan una
        # y ensucian nueve. Los ítems tienen que venir ya ordenados por esa
        # columna — la tabla no reordena, respeta el orden del asesor.
        arranca = agrupar and celda(it, agrupar) != previo
        if agrupar:
            previo = celda(it, agrupar)
        for clave, _, al in cols:
            v = celda(it, clave)
            base = f"{al} col-{esc(clave)}"
            if clave == agrupar:
                tds.append(f'<td class="{base} grupo">{esc(v) if arranca else ""}</td>')
                continue
            if clave == "barra":
                peso = _pct(get(it, "ponderacion", "peso", "pct", default=None)) or 0.0
                ancho = (peso / tope * 100) if tope else 0.0
                tds.append(f'<td class="{base}"><span class="tbar">'
                           f'<span style="width:{ancho:.1f}%"></span></span></td>')
                continue
            if clave == "riesgo" and clase_riesgo(v):
                tds.append(f'<td class="{base}"><span class="pill {clase_riesgo(v)}">'
                           f'{esc(v)}</span></td>')
            elif clave in ("clase", "descripcion"):
                tds.append(f'<td class="{base} strong">{esc(v)}</td>')
            else:
                tds.append(f'<td class="{base} {clase_signo(v)}">{esc(v)}</td>')
        # Un grupo de una sola línea no lleva subtotal: repetiría el mismo número
        # dos veces seguidas. El grupo que cierra la tabla ya lo controlaba abajo;
        # los del medio no, y sacaban subtotal aunque tuvieran una fila sola.
        if arranca and filas and subtotales and len(grupo_acc) > 1:
            filas.append(_fila_subtotal(cols, grupo_acc, agrupar))
        if arranca:
            grupo_acc = []
        filas.append(f'<tr class="{"g-ini" if arranca and filas else ""}">'
                     f"{''.join(tds)}</tr>")
        grupo_acc.append(it)

    if subtotales and len(grupo_acc) > 1:
        filas.append(_fila_subtotal(cols, grupo_acc, agrupar))

    if total:
        tds = []
        # El rótulo "Total" se inyecta en la primera columna SÓLO si ninguna
        # columna lo trae ya. Si no, aparece dos veces: una en la columna que el
        # JSON completó y otra puesta por acá.
        rotulado = any(celda(total, k) for k, _, _ in cols)
        for i, (clave, _, al) in enumerate(cols):
            v = celda(total, clave) or (
                "" if rotulado else (get(total, "label", default="Total") if i == 0 else ""))
            tds.append(f'<td class="{al} col-{esc(clave)}">{esc(v)}</td>')
        filas.append(f'<tr class="total">{"".join(tds)}</tr>')

    return (f'<table class="mc"><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(filas)}</tbody></table>')


def tabla_libre(headers, filas, alineacion=None, total_ultima=False):
    """Escotilla de escape: cualquier tabla que el catálogo de capítulos no
    cubra. Sale con el mismo estilo que las demás, así que no rompe la unidad
    visual aunque el contenido sea arbitrario."""
    al = list(alineacion or "")
    while len(al) < len(headers):
        al.append("r" if al else "l")
    th = "".join(f'<th class="{a}">{esc(h)}</th>' for h, a in zip(headers, al))
    out = []
    for i, fila in enumerate(filas):
        cls = ' class="total"' if (total_ultima and i == len(filas) - 1) else ""
        tds = "".join(f'<td class="{a} {clase_signo(c)}">{esc(c)}</td>'
                      for c, a in zip(fila, al))
        out.append(f"<tr{cls}>{tds}</tr>")
    return (f'<table class="mc"><thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(out)}</tbody></table>')


def ficha_instrumento(f):
    nombre = get(f, "nombre", "instrumento", "name", default="")
    tipo = get(f, "tipo", "clase", "kind", default="")
    texto = get(f, "que_hace", "descripcion", "texto", "rol", default="")
    datos = get(f, "datos", "metricas", default=[]) or []
    # Un dato puede venir como par (label + valor) o como texto suelto. El texto
    # suelto sale como etiqueta: sirve para clasificar la posición —"Largo
    # plazo", "Custodia USA"— donde no hay una cifra que mostrar.
    def _pill(d):
        if isinstance(d, str):
            return f'<span class="dato tag">{esc(d)}</span>'
        lb = get(d, "label", "etiqueta", default="")
        vl = get(d, "valor", "value", default="")
        if not lb:
            return f'<span class="dato tag">{esc(vl)}</span>'
        return f'<span class="dato">{esc(lb)} <b>{esc(vl)}</b></span>'
    pills = "".join(_pill(d) for d in datos)
    h = ['<div class="ficha"><div class="ficha-head"><div>'
         f'<span class="ficha-name">{esc(nombre)}</span>']
    if tipo:
        h.append(f'<span class="ficha-kind">{esc(tipo)}</span>')
    h.append("</div>")
    # La esquina de la ficha: el monto que se invierte y/o la pill de riesgo.
    # El monto va primero — es el número que el cliente busca en esta lámina.
    monto = get(f, "monto", "importe", default="")
    riesgo = get(f, "riesgo", "nivel_riesgo", default="")
    if monto or riesgo:
        h.append('<div class="ficha-esq">')
        if monto:
            h.append(f'<span class="ficha-monto">{esc(monto)}</span>')
        if riesgo:
            h.append(f'<span class="pill {clase_riesgo(riesgo)}">{esc(riesgo)}</span>')
        h.append("</div>")
    h.append("</div>")
    if texto:
        h.append(f"<p>{esc_md(texto)}</p>")
    if pills:
        h.append(f'<div class="ficha-datos">{pills}</div>')
    h.append("</div>")
    return "".join(h)


def bloque_acciones(acciones):
    """Qué comprar / qué vender / qué mantener. Es el capítulo que más valor
    tiene para un cliente con cartera vigente: convierte el análisis en algo
    accionable en vez de descriptivo."""
    cols = []
    # El orden por defecto es comprar → vender → mantener. `orden` lo cambia
    # cuando el relato de la slide pide otra secuencia: en un rebalanceo se
    # vende primero y recién después se coloca el producido, y leerlo al revés
    # obliga al cliente a reconstruir de dónde salió la plata.
    ROTULOS = {"comprar": "Comprar", "vender": "Vender", "mantener": "Mantener"}
    orden = get(acciones, "orden", "secuencia", default=None) \
        or ["comprar", "vender", "mantener"]
    for clave in orden:
        titulo = ROTULOS.get(clave)
        items = get(acciones, clave, default=[]) or []
        if titulo is None or not items:
            continue
        cuerpo = []
        for it in items:
            nombre = get(it, "nombre", "instrumento", "activo", default="")
            monto = get(it, "monto", "importe", "peso", default="")
            razon = get(it, "razon", "motivo", "por_que", "comentario", default="")
            cuerpo.append(
                f'<div class="accion-item"><div class="ai-top">'
                f'<span class="ai-name">{esc(nombre)}</span>'
                f'<span class="ai-amt">{esc(monto)}</span></div>'
                + (f'<div class="ai-why">{esc_md(razon)}</div>' if razon else "")
                + "</div>")
        cols.append(f'<div class="accion-col {clave}"><h4>{esc(titulo)}</h4>'
                    f'{"".join(cuerpo)}</div>')
    if not cols:
        return ""
    estilo = "" if len(cols) == 3 else f' style="grid-template-columns:repeat({len(cols)},1fr);"'
    return f'<div class="acciones"{estilo}>{"".join(cols)}</div>'


# ======================= Capítulos del DECK (16:9) ========================= #
# Cada función devuelve una LISTA de slides (HTML del cuerpo + metadatos), para
# que un capítulo largo pueda ocupar varias slides sin desbordar.

def esquina(destacado, riesgo):
    """La esquina superior derecha de una slide.

    Admite un dato destacado —típicamente el monto que se invierte— y/o la pill
    de nivel de riesgo. Si van los dos, el monto va primero: es el número que el
    cliente busca. Si no hay ninguno, la esquina no se dibuja."""
    piezas = []
    if destacado:
        if isinstance(destacado, str):
            destacado = {"valor": destacado}
        rotulo = get(destacado, "rotulo", "label", "titulo", default="")
        valor = get(destacado, "valor", "value", "monto", default="")
        if valor:
            piezas.append(
                (f'<span class="r-rotulo">{esc(rotulo)}</span>' if rotulo else "")
                + f'<span class="r-monto">{esc(valor)}</span>')
    if riesgo:
        piezas.append(f'<span class="r-rotulo">Nivel de riesgo</span>'
                      f'<span class="pill {clase_riesgo(riesgo)}">{esc(riesgo)}</span>')
    return f'<div class="slide-riesgo">{"".join(piezas)}</div>' if piezas else ""


def _slide(titulo, cuerpo, subtitulo=None, denso=False, nota=None, riesgo=None,
           destacado=None):
    return {"titulo": titulo, "subtitulo": subtitulo, "cuerpo": cuerpo,
            "denso": denso, "nota": nota, "clase": "", "riesgo": riesgo,
            "destacado": destacado}


def cap_texto(c):
    """Bloque de prosa en columnas. Es el capítulo de 'síntesis', 'contexto',
    'visión de mercado' — cualquier cosa que sea argumento y no tabla."""
    columnas = get(c, "columnas", "bloques", default=[]) or []
    if not columnas and get(c, "parrafos", "texto"):
        p = get(c, "parrafos", "texto")
        columnas = [{"parrafos": p if isinstance(p, list) else [p]}]
    n = min(max(len(columnas), 1), 4)
    partes = []
    for col in columnas:
        h = []
        t = get(col, "titulo", "title", default="")
        if t:
            h.append(f"<h5>{esc(t)}</h5>")
        ps = get(col, "parrafos", "texto", "parrafo", default=[]) or []
        if isinstance(ps, str):
            ps = [ps]
        h += [f"<p>{esc_md(p)}</p>" for p in ps]
        partes.append(f'<div class="col">{"".join(h)}</div>')
    cuerpo = f'<div class="cols c{n}">{"".join(partes)}</div>'
    largo = sum(len(str(p)) for col in columnas
                for p in (get(col, "parrafos", "texto", default=[]) or []))
    return [_slide(get(c, "titulo", default=""), cuerpo,
                   get(c, "subtitulo", default=None), denso=largo > 1600)]


def cap_forma_trabajo(c):
    """Cómo trabajamos con el cliente. Va temprano en el deck porque ordena la
    expectativa de la relación antes de hablar de plata."""
    pasos = get(c, "pasos", "items", default=[]) or []
    slides = []
    grupos = trozos(pasos, CONFIG["PASOS_POR_SLIDE"])
    for i, grupo in enumerate(grupos):
        n = 2 if len(grupo) <= 4 else 3
        items = []
        for j, p in enumerate(grupo):
            idx = i * CONFIG["PASOS_POR_SLIDE"] + j + 1
            items.append(
                f'<div class="paso"><div class="paso-num">{idx}</div>'
                f'<div class="paso-body"><h5>'
                f'{esc(get(p, "titulo", "title", default=""))}</h5>'
                f'<p>{esc(get(p, "texto", "descripcion", default=""))}</p>'
                f"</div></div>")
        cuerpo = f'<div class="pasos p{n}">{"".join(items)}</div>'
        intro = get(c, "intro", "subtitulo", default=None) if i == 0 else None
        titulo = get(c, "titulo", default="Cómo trabajamos")
        slides.append(_slide(titulo + (" (cont.)" if i else ""), cuerpo, intro,
                             denso=len(grupo) > 4))
    return slides


def cap_perfil(c):
    """Quién es el cliente — no su perfil de riesgo, sino la persona.

    Sirve para devolverle al cliente lo que el asesor entendió de la charla y
    que lo confirme o lo corrija antes de discutir instrumentos. Una propuesta
    construida sobre un malentendido se cae en la reunión, y este capítulo hace
    barato descubrirlo temprano.
    """
    rasgos = get(c, "rasgos", "items", "datos", default=[]) or []
    parrafos = get(c, "notas", "parrafos", "texto", default=[]) or []
    if isinstance(parrafos, str):
        parrafos = [parrafos]
    # `puntos` es una lista con viñetas: sirve cuando lo que cambia la propuesta
    # se enumera en vez de argumentarse en prosa.
    puntos = get(c, "puntos", "bullets", "lista", default=[]) or []
    if isinstance(puntos, str):
        puntos = [puntos]

    filas = "".join(
        f'<div class="rasgo"><span class="r-label">'
        f'{esc(get(r, "label", "etiqueta", "titulo", default=""))}</span>'
        f'<span class="r-valor">{esc(get(r, "valor", "value", default=""))}</span></div>'
        for r in rasgos)
    izq = f'<div class="rasgos">{filas}</div>' if filas else ""
    der = "".join(f"<p>{esc_md(p)}</p>" for p in parrafos)
    if puntos:
        der += "<ul>" + "".join(f"<li>{esc_md(x)}</li>" for x in puntos) + "</ul>"

    if izq and der:
        cuerpo = (f'<div class="split wide-right"><div>{izq}</div>'
                  f'<div class="perfil-texto">{der}</div></div>')
    else:
        cuerpo = izq or f'<div class="perfil-texto">{der}</div>'
    return [_slide(get(c, "titulo", default="Perfil del inversor"), cuerpo,
                   get(c, "subtitulo", default=None),
                   denso=len(rasgos) > 7, nota=get(c, "nota", default=None))]


def cap_proyeccion(c):
    """Proyección de capital al retiro.

    Los números grandes arriba y los supuestos a la vista: una proyección sin
    sus supuestos visibles es una promesa, y acá lo que se muestra es el
    resultado de un modelo con parámetros discutibles.
    """
    items = get(c, "kpis", "items", default=[]) or []
    supuestos = get(c, "supuestos", default=[]) or []
    n = min(max(len(items), 1), 5)
    # En qué base están las cifras. Va arriba de los números y no en la bajada:
    # si la proyección es en moneda constante hay que decirlo donde se lee, no
    # en una línea que se saltea.
    base = get(c, "base", "aclaracion", "moneda", default=None)
    cuerpo = (f'<div class="proy-base">{esc(base)}</div>' if base else "")
    cuerpo += (f'<div class="kpi-grid hero k{n}" style="grid-template-columns:repeat({n},1fr);">'
              + "".join(kpi(i) for i in items) + "</div>")
    if supuestos:
        pills = "".join(
            f'<span class="dato">{esc(get(s, "label", "etiqueta", default=""))} '
            f'<b>{esc(get(s, "valor", "value", default=""))}</b></span>'
            for s in supuestos)
        cuerpo += ('<div class="supuestos"><span class="s-titulo">Supuestos</span>'
                   f'<div class="ficha-datos">{pills}</div></div>')
    return [_slide(get(c, "titulo", default="Proyección al retiro"), cuerpo,
                   get(c, "subtitulo", default=None), nota=get(c, "nota", default=None))]


def cap_glidepath(c):
    """Trayectoria de la asignación a lo largo del horizonte.

    Hace visible algo que el cliente no puede deducir de una tabla: cómo se va a
    mover su cartera con los años. Sirve tanto para mostrar un desarme gradual de
    riesgo como para mostrar que la asignación NO cambia — que también es una
    decisión, y conviene que esté dicha.

    Los tramos marcados `tentativo` se dibujan atenuados y punteados: son los que
    todavía no están decididos, y pintarlos igual que el resto los haría pasar
    por compromiso.
    """
    tramos = get(c, "tramos", "items", default=[]) or []
    et_rv = get(c, "etiqueta_variable", default="Renta variable")
    et_rf = get(c, "etiqueta_fija", default="Renta fija")

    cols = []
    for t in tramos:
        eq = a_numero(get(t, "acciones", "variable", "equity", default=0)) or 0.0
        eq = min(max(eq, 0), 100)
        lb = get(t, "label", "edad", "anio", default="")
        sub = get(t, "nota", "detalle", default="")
        cls = " tentativo" if get(t, "tentativo", default=False) else ""
        cols.append(
            f'<div class="gp-col{cls}"><div class="gp-bar">'
            f'<div class="gp-rv" style="height:{eq:.0f}%"><span>{eq:.0f}%</span></div>'
            f'<div class="gp-rf"><span>{100 - eq:.0f}%</span></div></div>'
            f'<div class="gp-foot"><div class="gp-label">{esc(lb)}</div>'
            + (f'<div class="gp-sub">{esc(sub)}</div>' if sub else "")
            + "</div></div>")

    leyenda = (f'<div class="gp-leyenda">'
               f'<span><i style="background:var(--blue)"></i>{esc(et_rv)}</span>'
               f'<span><i style="background:var(--navy)"></i>{esc(et_rf)}</span></div>')
    cuerpo = (f'<div class="glidepath"><div class="gp-chart">{"".join(cols)}</div>'
              f'{leyenda}</div>')
    return [_slide(get(c, "titulo", default="Trayectoria de la cartera"), cuerpo,
                   get(c, "subtitulo", default=None),
                   denso=len(tramos) > 9, nota=get(c, "nota", default=None))]


def cap_kpis(c):
    """Los números que resumen la propuesta. Se renderizan en modo 'hero'
    (tarjetas grandes) porque acá el número ES el contenido de la slide."""
    items = get(c, "items", "kpis", default=[]) or []
    n = min(max(len(items), 1), 5)
    cuerpo = (f'<div class="kpi-grid hero k{n}" style="grid-template-columns:repeat({n},1fr);">'
              + "".join(kpi(i) for i in items) + "</div>")
    extra = get(c, "texto", "nota_texto", default=None)
    if extra:
        cuerpo += f'<p class="lede" style="margin-top:18px;">{esc(extra)}</p>'
    return [_slide(get(c, "titulo", default=""), cuerpo,
                   get(c, "subtitulo", default=None), nota=get(c, "nota", default=None))]


def cap_cartera(c):
    """Cartera sugerida: KPIs de encabezado + tabla de detalle. Es el capítulo
    central de la propuesta y el que replica el modelo que el equipo ya usa."""
    items = get(c, "items", "posiciones", "instrumentos", default=[]) or []
    columnas = get(c, "columnas", default=None)
    total = get(c, "total", default=None)
    kpis = get(c, "kpis", default=[]) or []
    agrupar = get(c, "agrupar_por", "agrupar", default=None)
    graf = get(c, "grafico", default=None)

    cabecera = ""
    if kpis:
        n = min(max(len(kpis), 1), 5)
        cabecera = (f'<div class="kpi-grid" style="grid-template-columns:repeat({n},1fr);'
                    f'margin-bottom:14px;">' + "".join(kpi(k) for k in kpis) + "</div>")

    # La primera slide lleva los KPIs, así que le entran menos filas.
    denso = len(items) > CONFIG["UMBRAL_DENSO"]
    cupo = CONFIG["FILAS_POR_SLIDE_DENSA"] if denso else CONFIG["FILAS_POR_SLIDE"]
    cupo_primera = max(cupo - (3 if kpis else 0), 4)

    grupos = [items[:cupo_primera]]
    resto = items[cupo_primera:]
    while resto:
        grupos.append(resto[:cupo])
        resto = resto[cupo:]

    slides = []
    for i, grupo in enumerate(grupos):
        es_ultima = (i == len(grupos) - 1)
        tab = tabla_cartera(grupo, columnas, total if es_ultima else None,
                            denso, agrupar,
                            subtotales=bool(get(c, "subtotales", default=False)))
        # El gráfico acompaña a la tabla sólo si la cartera entra en una slide:
        # partido en dos no dice nada, y repetido en cada una miente sobre a qué
        # tramo corresponde.
        if graf and len(grupos) == 1:
            cuerpo = (cabecera + '<div class="cart-wrap">' + tab
                      + grafico(graf, tamano=150) + "</div>")
        else:
            cuerpo = (cabecera if i == 0 else "") + tab
        titulo = get(c, "titulo", default="Cartera sugerida")
        slides.append(_slide(titulo + (" (cont.)" if i else ""), cuerpo,
                             get(c, "subtitulo", default=None) if i == 0 else None,
                             denso=denso,
                             nota=get(c, "nota", default=None) if es_ultima else None))
    return slides


def cap_cartera_actual(c):
    """Cartera vigente + qué hacer con ella. Puede traer la foto de posiciones,
    el bloque de acciones, o ambos: se arma con lo que el asesor haya aportado."""
    slides = []
    posiciones = get(c, "posiciones", "items", default=[]) or []
    acciones = get(c, "acciones", "recomendaciones", default=None)
    titulo = get(c, "titulo", default="Cartera actual")

    if posiciones:
        columnas = get(c, "columnas", default=None)
        denso = len(posiciones) > CONFIG["UMBRAL_DENSO"]
        cupo = CONFIG["FILAS_POR_SLIDE_DENSA"] if denso else CONFIG["FILAS_POR_SLIDE"]
        for i, grupo in enumerate(trozos(posiciones, cupo)):
            es_ultima = (i == len(trozos(posiciones, cupo)) - 1)
            slides.append(_slide(
                titulo + (" (cont.)" if i else ""),
                tabla_cartera(grupo, columnas,
                              get(c, "total", default=None) if es_ultima else None, denso),
                get(c, "subtitulo", default=None) if i == 0 else None, denso=denso))

    if acciones:
        cuerpo = bloque_acciones(acciones)
        intro = get(c, "intro_acciones", default=None)
        slides.append(_slide(get(c, "titulo_acciones", default="Qué comprar y qué vender"),
                             cuerpo, intro, denso=True, nota=get(c, "nota", default=None)))
    return slides


def cap_trades(c):
    """Movimientos emparejados: qué sale y qué entra en cada uno.

    Es el hermano de `cartera_actual` y resuelve el caso contrario. En un
    rebalanceo por estrategia cada posición se justifica sola contra el mandato
    —esto se vende porque X, esto se compra porque Y— y las tres columnas de
    comprar / vender / mantener alcanzan. En un trade el argumento es la
    comparación entre dos instrumentos del mismo segmento: por qué el que entra
    es mejor que el que sale. Ahí la venta y la compra no se pueden leer por
    separado sin que el cliente tenga que adivinar qué va con qué.

    Salen dos slides: la tabla de movimientos y, si hay razones, una lámina con
    una columna por movimiento. La razón nunca va como quinta columna de la
    tabla: el texto largo parte las filas en dos y rompe el criterio 59."""
    items = get(c, "items", "movimientos", "trades", default=[]) or []
    if not items:
        return []
    slides = []

    filas = []
    for i, it in enumerate(items, 1):
        filas.append([
            get(it, "etiqueta", "label", default=f"Movimiento {i}"),
            get(it, "sale", "vender", "desde", default=""),
            get(it, "entra", "comprar", "hacia", default=""),
            get(it, "monto", "importe", default=""),
        ])
    slides.append(_slide(
        get(c, "titulo", default="Los movimientos"),
        tabla_libre(["", "Sale", "Entra", "Monto"], filas, "lllr", False),
        get(c, "subtitulo", default=None),
        denso=len(filas) > CONFIG["UMBRAL_DENSO"],
        nota=get(c, "nota", default=None)))

    # Las razones sólo si las hay: un trade sin porqué es una orden, pero a veces
    # el asesor quiere la tabla sola y desarrolla el argumento hablando.
    con_razon = [it for it in items
                 if get(it, "razon", "motivo", "por_que", default=None)]
    if con_razon:
        for j, grupo in enumerate(trozos(con_razon, 4)):
            partes = []
            for k, it in enumerate(grupo, 1):
                h = []
                t = get(it, "etiqueta", "label", default="")
                if t:
                    h.append(f"<h5>{esc(t)}</h5>")
                ps = get(it, "razon", "motivo", "por_que", default=[]) or []
                if isinstance(ps, str):
                    ps = [ps]
                h += [f"<p>{esc_md(p)}</p>" for p in ps]
                partes.append(f'<div class="col">{"".join(h)}</div>')
            n = min(max(len(grupo), 1), 4)
            titulo_r = get(c, "titulo_razones", default="Por qué cada movimiento")
            slides.append(_slide(
                titulo_r + (" (cont.)" if j else ""),
                f'<div class="cols c{n}">{"".join(partes)}</div>',
                get(c, "subtitulo_razones", default=None) if j == 0 else None))
    return slides


def cap_distribuciones(c):
    graficos = get(c, "graficos", "items", "distribuciones", default=[]) or []
    # Los deltas: lo que cambia entre el antes y el después, en una franja al
    # pie. Un par de donuts lado a lado obliga a restar de memoria; el número
    # que importa es cuánto se movió cada cosa, así que se escribe.
    deltas = get(c, "deltas", "cambios", default=[]) or []
    tira = ""
    if deltas:
        cajas = []
        for d_ in deltas:
            cls = " destacado" if get(d_, "destacado", "accent", default=False) else ""
            cajas.append(
                f'<div class="delta{cls}">'
                f'<span class="d-label">{esc(get(d_, "label", "etiqueta", default=""))}</span>'
                f'<span class="d-valor">{esc(get(d_, "valor", "value", default=""))}</span>'
                + (f'<span class="d-nota">{esc(get(d_, "nota", default=""))}</span>'
                   if get(d_, "nota", default="") else "")
                + "</div>")
        # Con menos de tres tarjetas no se reparte el ancho: cada caja mide lo
        # que mide su contenido y el sobrante queda vacío a la derecha. Con tres
        # o más se reparten la fila en partes iguales, como siempre.
        if len(cajas) < 3:
            tira = ('<div class="deltas pocas" style="grid-template-columns:'
                    f'repeat({len(cajas)},max-content);">' + "".join(cajas) + "</div>")
        else:
            tira = (f'<div class="deltas" style="grid-template-columns:repeat({len(cajas)},1fr);">'
                    + "".join(cajas) + "</div>")

    # Métricas de encabezado, opcionales: sirven para una slide de ficha de
    # portfolio, donde la distribución se lee mejor con el rendimiento y el
    # riesgo a la vista.
    kpis = get(c, "kpis", default=[]) or []
    cabecera = ""
    if kpis:
        nk = min(max(len(kpis), 1), 5)
        cabecera = (f'<div class="kpi-grid" style="grid-template-columns:repeat({nk},1fr);'
                    f'margin-bottom:16px;">' + "".join(kpi(k) for k in kpis) + "</div>")

    slides = []
    grupos = trozos(graficos, 3)
    for i, grupo in enumerate(grupos):
        n = len(grupo) if grupo else 1
        # Las tarjetas van ARRIBA de los gráficos: son la conclusión y es lo que
        # el lector tiene que ver primero. Debajo, el detalle que las sostiene.
        cuerpo = (cabecera if i == 0 else "")
        cuerpo += tira if i == 0 else ""
        cuerpo += (f'<div class="dist-wrap" style="grid-template-columns:repeat({n},1fr);">'
                  + "".join(grafico(g) for g in grupo) + "</div>")
        slides.append(_slide(get(c, "titulo", default="Distribución de la cartera"),
                             cuerpo, get(c, "subtitulo", default=None),
                             denso=(bool(deltas) or bool(kpis)) and n >= 3,
                             riesgo=get(c, "riesgo", "nivel_riesgo", default=None),
                             destacado=get(c, "destacado", "monto", default=None),
                             # La nota va en la última slide del capítulo: si se
                             # repitiera en cada una parecería aplicar a cada
                             # gráfico por separado.
                             nota=(get(c, "nota", default=None)
                                   if i == len(grupos) - 1 else None)))
    return slides


def cap_instrumentos(c):
    """Qué hace cada componente de la cartera. Acá es donde entra el contenido
    de los fact sheets que aportó el asesor: una línea por instrumento sobre el
    rol que cumple, no una repetición de la ficha técnica."""
    fichas = get(c, "fichas", "items", "instrumentos", default=[]) or []
    slides = []
    grupos = trozos(fichas, CONFIG["FICHAS_POR_SLIDE"])
    for i, grupo in enumerate(grupos):
        n = 2 if len(grupo) <= 4 else 3
        cuerpo = (f'<div class="g{n}" style="grid-template-columns:repeat({n},1fr);">'
                  + "".join(ficha_instrumento(f) for f in grupo) + "</div>")
        titulo = get(c, "titulo", default="Los instrumentos de la cartera")
        slides.append(_slide(titulo + (" (cont.)" if i else ""), cuerpo,
                             get(c, "subtitulo", default=None) if i == 0 else None,
                             denso=len(grupo) > 4,
                             # La nota va en la última slide del capítulo. Antes no
                             # se pasaba: el campo validaba, se aceptaba y no se
                             # dibujaba, así que una aclaración desaparecía sin aviso.
                             nota=(get(c, "nota", default=None)
                                   if i == len(grupos) - 1 else None)))
    return slides


def cap_tabla(c):
    headers = get(c, "headers", "columnas", default=[]) or []
    filas = get(c, "filas", "rows", "datos", default=[]) or []
    denso = len(filas) > CONFIG["UMBRAL_DENSO"]
    cupo = CONFIG["FILAS_POR_SLIDE_DENSA"] if denso else CONFIG["FILAS_POR_SLIDE"]
    slides = []
    grupos = trozos(filas, cupo)
    for i, grupo in enumerate(grupos):
        es_ultima = (i == len(grupos) - 1)
        cuerpo = tabla_libre(headers, grupo, get(c, "alineacion", default=None),
                             get(c, "total_ultima_fila", default=False) and es_ultima)
        slides.append(_slide(get(c, "titulo", default="") + (" (cont.)" if i else ""),
                             cuerpo, get(c, "subtitulo", default=None) if i == 0 else None,
                             denso=denso,
                             nota=get(c, "nota", default=None) if es_ultima else None))
    return slides


CAPITULOS_DECK = {
    "perfil": cap_perfil,
    "perfil_inversor": cap_perfil,
    "proyeccion": cap_proyeccion,
    "glidepath": cap_glidepath,
    "trayectoria": cap_glidepath,
    "proyeccion_retiro": cap_proyeccion,
    "texto": cap_texto,
    "sintesis": cap_texto,
    "vision_mercado": cap_texto,
    "forma_de_trabajo": cap_forma_trabajo,
    "kpis": cap_kpis,
    "resumen": cap_kpis,
    "cartera_sugerida": cap_cartera,
    "cartera": cap_cartera,
    "cartera_actual": cap_cartera_actual,
    "trades": cap_trades,
    "movimientos": cap_trades,
    "distribuciones": cap_distribuciones,
    "instrumentos": cap_instrumentos,
    "tabla": cap_tabla,
}


# ============================ Armado del DECK ============================== #

def slide_portada(p, logo_svg):
    cli = get(p, "cliente", default={}) or {}
    nombre_cli = get(cli, "nombre", "name", default="") if isinstance(cli, dict) else str(cli)
    portada = get(p, "portada", default={}) or {}
    asesor = get(p, "asesor", default={}) or {}
    imagen = get(portada, "imagen", "image", default=None)

    art_cls, art_style = "cover-art", ""
    veil = ""
    if imagen and os.path.exists(imagen):
        ext = os.path.splitext(imagen)[1].lstrip(".").lower() or "jpeg"
        b64 = base64.b64encode(open(imagen, "rb").read()).decode()
        art_cls += " has-image"
        art_style = f' style="background-image:url(data:image/{ext};base64,{b64});"'
        veil = '<div class="cover-veil"></div>'

    anio = get(p, "anio", default=None) or (get(p, "fecha", default="") or "")[-4:]
    sub = get(p, "subtitulo", "subtitle", default="")
    fecha = get(p, "fecha", default="")

    ases = asesores_de(p)
    contacto = ""
    if ases:
        nombres = "".join(
            f'<span class="k-value">{esc(get(a, "nombre", default=""))}</span>' for a in ases)
        cargo = get(ases[0], "cargo", default=CONFIG["AREA"])
        contacto = (
            '<div class="cover-by"><span class="k-label">Presentado por</span>'
            + nombres
            + (f'<span class="k-note">{esc(cargo)}</span>' if cargo else "")
            + "</div>")

    return f'''<div class="slide cover">
<div class="{art_cls}"{art_style}></div>{veil}
<div class="cover-inner with-logo">
  <div class="cover-top">
    <div class="cover-top-left"><span class="cover-client">{esc(nombre_cli)}</span>
    {f'<span class="cover-year">{esc(anio)}</span>' if anio else ''}</div>
    <div class="cover-logo">{logo_svg}</div>
  </div>
  <h1 class="cover-title">{esc(get(p, "titulo", default="Propuesta de Inversión"))}</h1>
  {f'<p class="cover-sub">{esc(sub)}</p>' if sub else ''}
  <div class="cover-foot">{contacto}
    {f'<div class="cover-date">Datos al {esc(fecha)}</div>' if fecha else ''}
  </div>
</div>
</div>'''


def slide_divisor(c, nombre_cli, numero, logo=""):
    sub = get(c, "subtitulo", default="")
    return f'''<div class="slide divider">
<div class="divider-art"></div>
<div class="slide-logo">{logo}</div>
<div class="divider-inner">
  <div class="divider-num">{numero:02d}</div>
  <h2 class="divider-title">{esc(get(c, "titulo", default=""))}</h2>
  {f'<p class="divider-sub">{esc(sub)}</p>' if sub else ''}
</div>
<div class="divider-client">{esc(nombre_cli)}</div>
</div>'''


def slide_cierre(p, c, logo=""):
    contacto = []
    for a in asesores_de(p):
        lineas = []
        for clave in ("email", "telefono"):
            v = get(a, clave, default="")
            if v:
                lineas.append(f'<span class="k-dato">{esc(v)}</span>')
        contacto.append(
            '<div><span class="k-label">'
            f'{esc(get(a, "cargo", default=CONFIG["AREA"]))}</span>'
            f'<span class="k-value">{esc(get(a, "nombre", default=""))}</span>'
            + "".join(lineas) + "</div>")
    disc = get(c, "disclaimer", default=None) or CONFIG["DISCLAIMER"]
    # Sin URL por defecto: si el capítulo no la trae, la slide no la muestra.
    u = get(c, "url", default=None)
    url_cierre = f'<div class="closing-url">{esc(u)}</div>' if u else ""
    return f'''<div class="slide closing">
<div class="slide-logo">{logo}</div>
<div class="closing-inner">
  <h2 class="closing-title">{esc(get(c, "titulo", default="¡Muchas gracias!"))}</h2>
  {url_cierre}
  <div class="closing-contact">{"".join(contacto)}</div>
  <div class="disclaimer"><b>Información importante</b>{esc(disc)}
    <span class="matriculas">{esc(CONFIG["LEYENDA_REGULATORIA"])}</span></div>
</div>
</div>'''


def slide_contenido(s, nombre_cli, numero):
    cls = "slide dense" if s["denso"] else "slide"
    sub = s.get("subtitulo")
    pie = []
    if s.get("nota"):
        pie.append(f'<div class="fnote">{esc(s["nota"])}</div>')
    else:
        pie.append("<div></div>")
    pie.append(f'<div class="fbrand">{esc(CONFIG["FOOTER_BRAND"])}</div>')
    badge = esquina(s.get("destacado"), s.get("riesgo"))
    return f'''<div class="{cls}">{badge}
<div class="slide-top"><span class="slide-badge">{numero}</span>
<span class="slide-client">{esc(nombre_cli)}</span></div>
<h2 class="slide-title">{esc(s["titulo"])}</h2>
{f'<p class="slide-sub">{esc(sub)}</p>' if sub else ''}
<div class="slide-body">{s["cuerpo"]}</div>
<div class="slide-foot">{"".join(pie)}</div>
</div>'''


def construir_deck(p, assets):
    cli = get(p, "cliente", default={}) or {}
    nombre_cli = get(cli, "nombre", default="") if isinstance(cli, dict) else str(cli)
    logo = leer_logo(assets, "negativo", 150)   # portada: arriba a la derecha, protagonista
    logo_chico = leer_logo(assets, "negativo", 84)  # divisores y cierre

    out = [slide_portada(p, logo)]
    numero = 1          # numeración visible (la portada no cuenta)
    n_divisor = 0

    for c in get(p, "capitulos", "chapters", default=[]) or []:
        tipo = (get(c, "tipo", "type", default="texto") or "texto").lower()
        if tipo == "portada":
            continue
        if tipo == "divisor":
            n_divisor += 1
            out.append(slide_divisor(c, nombre_cli, n_divisor, logo_chico))
            continue
        if tipo == "cierre":
            out.append(slide_cierre(p, c, logo_chico))
            continue
        fn = CAPITULOS_DECK.get(tipo)
        if fn is None:
            # Un tipo desconocido no debe romper el render: se avisa por stderr
            # y se intenta como bloque de texto, que es el más permisivo.
            print(f"  aviso: capítulo de tipo '{tipo}' desconocido; "
                  f"se renderiza como texto.", file=sys.stderr)
            fn = cap_texto
        for s in fn(c):
            numero += 1
            out.append(slide_contenido(s, nombre_cli, numero))

    if not any('class="slide closing"' in s for s in out):
        out.append(slide_cierre(p, {}, logo_chico))
    return "\n".join(out)


# ========================== Armado del ONE-PAGER =========================== #

def buscar_capitulo(p, *tipos):
    for c in get(p, "capitulos", default=[]) or []:
        if (get(c, "tipo", "type", default="") or "").lower() in tipos:
            return c
    return None


def construir_onepager(p, assets):
    """El one-pager no compone capítulos libremente: es una hoja de estructura
    fija (KPIs · detalle · distribuciones) que toma lo esencial de la propuesta.
    Si el asesor cargó capítulos que no entran acá, se avisa cuáles se omiten
    para que la decisión de recortar sea explícita y no una sorpresa."""
    cli = get(p, "cliente", default={}) or {}
    nombre_cli = get(cli, "nombre", default="") if isinstance(cli, dict) else str(cli)
    logo = leer_logo(assets, "negativo", 96)    # banda negra del encabezado

    cap_cart = buscar_capitulo(p, "cartera_sugerida", "cartera")
    cap_dist = buscar_capitulo(p, "distribuciones")
    cap_k = buscar_capitulo(p, "kpis", "resumen")
    cap_inst = buscar_capitulo(p, "instrumentos")

    items = get(cap_cart, "items", "posiciones", default=[]) or [] if cap_cart else []
    kpis = (get(cap_k, "items", default=[]) if cap_k else None) or \
           (get(cap_cart, "kpis", default=[]) if cap_cart else []) or []

    if len(items) > CONFIG["OP_FILAS_MAXIMO"]:
        print(f"  aviso: la cartera tiene {len(items)} líneas; el one-pager rinde bien "
              f"hasta {CONFIG['OP_FILAS_MAXIMO']}. Se renderizan todas, pero revisá "
              f"la legibilidad o usá --formato deck.", file=sys.stderr)

    # La compresión mira el contenido total de la hoja, no sólo las filas: desde
    # que las distribuciones y la nota de instrumentos se apilan debajo de la
    # tabla, seis posiciones con seis fichas ocupan más que doce posiciones
    # peladas. Cada ficha pesa ~0,8 de una fila.
    n_fichas = len(get(cap_inst, "fichas", "items", default=[]) or []) if cap_inst else 0
    peso = len(items) + 0.8 * n_fichas
    cls = ""
    if peso > CONFIG["OP_FILAS_TIGHTER"]:
        cls = " tighter"
    elif peso > CONFIG["OP_FILAS_TIGHT"]:
        cls = " tight"

    n_k = min(max(len(kpis), 1), 6)
    bloque_kpis = (f'<div class="op-kpis k{n_k}" '
                   f'style="grid-template-columns:repeat({n_k},1fr);">'
                   + "".join(kpi(k) for k in kpis) + "</div>") if kpis else ""

    tabla = ""
    if items:
        tabla = ('<div class="section-heading">Detalle de la propuesta</div>'
                 + tabla_cartera(items, get(cap_cart, "columnas", default=None),
                                 get(cap_cart, "total", default=None)))
        nota = get(cap_cart, "nota", default=None)
        if nota:
            tabla += f'<div class="table-footnote">{esc(nota)}</div>'

    graficos = get(cap_dist, "graficos", "items", default=[]) or [] if cap_dist else []
    dist = ""
    if graficos:
        n_g = min(len(graficos), 3)
        dist = (f'<div class="op-dist g{n_g}" style="grid-template-columns:repeat({n_g},1fr);">'
                + "".join(grafico(g) for g in graficos[:3]) + "</div>")

    # Instrumentos al pie, como NOTA y no como tarjetas. En una hoja sola el
    # espacio se lo tienen que quedar la cartera y las distribuciones: qué hace
    # cada vehículo es contexto de apoyo, no un bloque protagonista. Si la ficha
    # trae `resumen` se usa eso (una cláusula); si no, se recorta `que_hace`.
    fichas = get(cap_inst, "fichas", "items", default=[]) or [] if cap_inst else []
    tira = ""
    if fichas:
        lineas = []
        for f in fichas:
            nombre = get(f, "nombre", "instrumento", default="")
            txt = get(f, "resumen", "que_hace", "descripcion", default="")
            # Si la ficha no trae `resumen`, `que_hace` viene con el texto largo
            # del deck. En una nota al pie eso desborda la hoja, así que se corta
            # en el límite de palabra. Lo correcto es cargar `resumen`; esto es
            # la red para que una propuesta no salga rota por no haberlo hecho.
            if txt and len(txt) > CONFIG["OP_NOTA_MAX_CARACTERES"]:
                corte = txt[:CONFIG["OP_NOTA_MAX_CARACTERES"]].rsplit(" ", 1)[0]
                txt = corte.rstrip(" .,;:") + "…"
            if txt:
                lineas.append(f'<span class="op-nota-item"><b>{esc(nombre)}</b> — '
                              f'{esc_md(txt)}</span>')
        if lineas:
            tira = f'<div class="op-nota-inst">{"".join(lineas)}</div>'

    # Las distribuciones van DEBAJO de la tabla, no en una columna al costado:
    # así la cartera ocupa el ancho completo (que es lo que el cliente lee) y no
    # queda media hoja vacía cuando hay un solo gráfico. La nota de instrumentos
    # cierra la hoja, apoyada contra el disclaimer (ver `margin-top:auto` en el
    # CSS): es contexto de lectura final, no parte del cuerpo de la propuesta.
    partes = []
    if dist:
        partes.append(f'<div class="op-bottom">{dist}</div>')
    if tira:
        partes.append(tira)
    bloque_inferior = "".join(partes)
    fecha_corta = get(p, "fecha_corta", default=None) or mes_anio(get(p, "fecha", default=""))
    objetivo = get(p, "objetivo", default=None) or \
        (get(cap_cart, "subtitulo", default=None) if cap_cart else None)

    meta = []
    for a in asesores_de(p):
        if get(a, "nombre", default=""):
            meta.append(f'<b>{esc(get(a, "nombre"))}</b>')
        for k in ("email", "telefono"):
            if get(a, k, default=""):
                meta.append(esc(get(a, k)))

    return f'''<div class="sheet{cls}">
<div class="op-header">
  <div class="op-header-left">
    <span class="op-eyebrow">{esc(nombre_cli)}{f'<span class="op-fecha">&nbsp;·&nbsp;{esc(fecha_corta)}</span>' if fecha_corta else ''}</span>
    <h1 class="op-title">{esc(get(p, "titulo", default="Propuesta de Inversión"))}</h1>
  </div>
  <div class="op-logo">{logo}</div>
</div>
{f'<div class="op-objetivo"><span class="lbl">Objetivo</span><span class="val">{esc(objetivo)}</span></div>' if objetivo else ''}
<div class="op-body">
  {bloque_kpis}
  {tabla}
  {bloque_inferior}
</div>
<div class="op-foot">
  <div class="disclaimer"><b>Información importante</b>{esc(CONFIG["DISCLAIMER"])}
    <span class="matriculas">{esc(CONFIG["LEYENDA_REGULATORIA"])}</span></div>
  <div class="op-meta">{"<br>".join(meta)}</div>
</div>
</div>'''


# ========================== Armado del DOCUMENTO =========================== #

def seccion_documento(c):
    """Traduce un capítulo al registro del documento largo: prosa primero,
    tablas y figuras como apoyo. El mismo dato que en el deck era una slide acá
    es una sección numerada."""
    tipo = (get(c, "tipo", "type", default="texto") or "texto").lower()
    titulo = get(c, "titulo", default="")
    h = [f'<div class="doc-sec"><h2>{esc(titulo)}</h2>']

    intro = get(c, "subtitulo", "intro", default=None)
    if intro:
        h.append(f'<div class="doc-callout">{esc(intro)}</div>')

    if tipo in ("texto", "sintesis", "vision_mercado"):
        for col in get(c, "columnas", "bloques", default=[]) or []:
            t = get(col, "titulo", default="")
            if t:
                h.append(f"<h3>{esc(t)}</h3>")
            ps = get(col, "parrafos", "texto", default=[]) or []
            h += [f"<p>{esc_md(x)}</p>" for x in ([ps] if isinstance(ps, str) else ps)]
        ps = get(c, "parrafos", "texto", default=[]) or []
        h += [f"<p>{esc_md(x)}</p>" for x in ([ps] if isinstance(ps, str) else ps)]

    elif tipo == "forma_de_trabajo":
        for p_ in get(c, "pasos", "items", default=[]) or []:
            h.append(f'<h3>{esc(get(p_, "titulo", default=""))}</h3>'
                     f'<p>{esc(get(p_, "texto", "descripcion", default=""))}</p>')

    elif tipo in ("kpis", "resumen"):
        items = get(c, "items", default=[]) or []
        n = min(max(len(items), 1), 4)
        h.append(f'<div class="kpi-grid" style="grid-template-columns:repeat({n},1fr);">'
                 + "".join(kpi(i) for i in items) + "</div>")
        if get(c, "texto", default=None):
            h.append(f'<p>{esc(get(c, "texto"))}</p>')

    elif tipo in ("cartera_sugerida", "cartera", "cartera_actual"):
        items = get(c, "items", "posiciones", default=[]) or []
        if items:
            h.append(tabla_cartera(items, get(c, "columnas", default=None),
                                   get(c, "total", default=None)))
        acciones = get(c, "acciones", default=None)
        if acciones:
            for clave, tit in (("comprar", "Comprar"), ("vender", "Vender"),
                               ("mantener", "Mantener")):
                lst = get(acciones, clave, default=[]) or []
                if not lst:
                    continue
                h.append(f"<h3>{tit}</h3><ul>")
                for it in lst:
                    razon = get(it, "razon", "motivo", default="")
                    h.append(f'<li><b>{esc(get(it, "nombre", default=""))}</b>'
                             f'{" — " + esc(razon) if razon else ""}</li>')
                h.append("</ul>")

    elif tipo == "distribuciones":
        gs = get(c, "graficos", "items", default=[]) or []
        h.append('<div class="dist-wrap">' + "".join(grafico(g) for g in gs) + "</div>")

    elif tipo == "instrumentos":
        fichas = get(c, "fichas", "items", default=[]) or []
        h.append('<div class="fichas-grid">'
                 + "".join(ficha_instrumento(f) for f in fichas) + "</div>")

    elif tipo == "tabla":
        h.append(tabla_libre(get(c, "headers", default=[]) or [],
                             get(c, "filas", "rows", default=[]) or [],
                             get(c, "alineacion", default=None),
                             get(c, "total_ultima_fila", default=False)))

    elif tipo in ("trades", "movimientos"):
        # En prosa el movimiento se lee mejor emparejado en una línea que como
        # tabla de cuatro columnas, y la razón va justo debajo de su movimiento.
        movs = get(c, "items", "movimientos", "trades", default=[]) or []
        for i, m in enumerate(movs, 1):
            et = get(m, "etiqueta", "label", default=f"Movimiento {i}")
            sale = get(m, "sale", "vender", "desde", default="")
            entra = get(m, "entra", "comprar", "hacia", default="")
            monto = get(m, "monto", "importe", default="")
            h.append(f"<h3>{esc(et)}</h3>")
            h.append(f"<p><b>{esc(sale)}</b> → <b>{esc(entra)}</b>"
                     + (f" · {esc(monto)}" if monto else "") + "</p>")
            ps = get(m, "razon", "motivo", "por_que", default=[]) or []
            if isinstance(ps, str):
                ps = [ps]
            h += [f"<p>{esc_md(x)}</p>" for x in ps]

    nota = get(c, "nota", default=None)
    if nota:
        h.append(f'<div class="doc-figcap">{esc(nota)}</div>')
    h.append("</div>")
    return "".join(h)


def construir_documento(p, assets):
    cli = get(p, "cliente", default={}) or {}
    nombre_cli = get(cli, "nombre", default="") if isinstance(cli, dict) else str(cli)
    asesor = get(p, "asesor", default={}) or {}
    logo = leer_logo(assets, "positivo", 132)  # portada sobre fondo blanco

    caps = [c for c in (get(p, "capitulos", default=[]) or [])
            if (get(c, "tipo", default="texto") or "").lower()
            not in ("portada", "divisor", "cierre")]

    meta = []
    for lbl, val in (("Preparado para", nombre_cli),
                     ("Preparado por", " · ".join(
                         get(a, "nombre", default="") for a in asesores_de(p))),
                     ("Fecha", get(p, "fecha", default="")),
                     ("Mandato", get(p, "mandato", default=""))):
        if val:
            meta.append(f'<div><span class="lbl">{lbl}</span>'
                        f'<span class="val">{esc(val)}</span></div>')

    toc = "".join(f'<li>{esc(get(c, "titulo", default=""))}</li>' for c in caps)
    sub = get(p, "subtitulo", default="")

    firma = []
    for a in asesores_de(p):
        datos = " · ".join(x for x in (get(a, "email", default=""),
                                       get(a, "telefono", default="")) if x)
        firma.append(f'<div><span class="lbl">{esc(get(a, "cargo", default=CONFIG["AREA"]))}</span>'
                     f'<span class="val">{esc(get(a, "nombre", default=""))}</span>'
                     + (f'<span class="lbl" style="margin-top:4px">{esc(datos)}</span>'
                        if datos else "") + "</div>")

    return f'''<div class="doc-wrap">
<div class="doc-cover">
  <div class="dc-logo">{logo}</div>
  <div class="dc-eyebrow">Wealth Management</div>
  <h1>{esc(get(p, "titulo", default="Propuesta de Administración de Cartera"))}</h1>
  <div class="dc-client">{esc(nombre_cli)}</div>
  <div class="dc-rule"></div>
  {f'<p style="margin-top:20px;max-width:480px;font-size:12px;line-height:1.6;">{esc(sub)}</p>' if sub else ''}
  <div class="dc-meta">{"".join(meta)}</div>
</div>
<div class="doc-toc"><h2>Contenido</h2><ol>{toc}</ol></div>
{"".join(seccion_documento(c) for c in caps)}
<div class="doc-legal">
  <h2>Información importante</h2>
  <div class="disclaimer"><b>Aviso legal</b>{esc(CONFIG["DISCLAIMER"])}
    <span class="matriculas">{esc(CONFIG["LEYENDA_REGULATORIA"])}</span></div>
  <div class="doc-firma">{"".join(firma)}</div>
  <p style="margin-top:18px;font-size:7.4px;color:#A1A1AA;">
    {esc(CONFIG["FOOTER_BRAND"])}</p>
</div>
</div>'''


# ============================ HTML + PDF =================================== #

def css_fuentes(assets):
    """Inter embebida en base64. Va inline para que el PDF sea autocontenido y
    se vea igual en cualquier máquina, sin depender de la red ni de fuentes
    instaladas."""
    pesos = {400: "inter-latin-400-normal.woff2", 500: "inter-latin-500-normal.woff2",
             600: "inter-latin-600-normal.woff2", 700: "inter-latin-700-normal.woff2"}
    out = []
    for peso, archivo in pesos.items():
        ruta = os.path.join(assets, "fonts", archivo)
        if not os.path.exists(ruta):
            continue
        b64 = base64.b64encode(open(ruta, "rb").read()).decode()
        out.append(f"@font-face{{font-family:'Inter';font-style:normal;"
                   f"font-weight:{peso};font-display:block;"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")
    return "\n".join(out)


# Proporción del logotipo dentro del archivo oficial: el PNG trae incorporado el
# área de resguardo de la marca (el aire mínimo alrededor). Se usa tal cual viene
# —no se recorta— y el ancho se compensa con este factor para que el logotipo
# visible quede del tamaño buscado.
LOGO_PROPORCION = 0.648


def leer_logo(assets, variante="negativo", ancho=104):
    """Logotipo oficial de Max Capital, embebido en base64.

    `variante`: "negativo" (blanco, para fondos oscuros) o "positivo" (negro,
    para fondos claros). Son los archivos que provee marketing y se usan sin
    modificar: no se recolorean, no se les cambia la opacidad y no se recortan
    sus márgenes. Tintar el logotipo o bajarle la opacidad es una violación de
    marca, aunque quede lindo.
    """
    ruta = os.path.join(assets, f"logo_{variante}.png")
    if not os.path.exists(ruta):
        print(f"  aviso: falta el logotipo oficial {ruta}", file=sys.stderr)
        return ""
    b64 = base64.b64encode(open(ruta, "rb").read()).decode()
    w = round(ancho / LOGO_PROPORCION)
    return (f'<img class="logo-img" alt="Max Capital" style="width:{w}px" '
            f'src="data:image/png;base64,{b64}">')


def leer_css(assets, *nombres):
    out = []
    for n in nombres:
        ruta = os.path.join(assets, n)
        if os.path.exists(ruta):
            out.append(open(ruta, encoding="utf-8").read())
        else:
            print(f"  aviso: falta {n} en {assets}", file=sys.stderr)
    return "\n".join(out)


CONSTRUCTORES = {
    "deck": (construir_deck, "deck.css", ""),
    "onepager": (construir_onepager, "onepager.css", ""),
    "documento": (construir_documento, "documento.css", "doc"),
}


def construir_html(propuesta, formato, assets):
    if formato not in CONSTRUCTORES:
        raise SystemExit(f"Formato desconocido: {formato}. "
                         f"Opciones: {', '.join(CONSTRUCTORES)}")
    fn, css_formato, body_cls = CONSTRUCTORES[formato]
    cuerpo = fn(propuesta, assets)
    css = css_fuentes(assets) + "\n" + leer_css(assets, "base.css", css_formato)
    titulo = get(propuesta, "titulo", default="Propuesta de Inversión")
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<title>{esc(titulo)}</title><style>\n{css}\n</style></head>'
            f'<body class="{body_cls}">{cuerpo}</body></html>')


# Medidas de página por formato. El deck usa 10 x 5.625 in, que es exactamente
# el tamaño del deck de referencia (720 x 405 pt) y mapea 1:1 con los 960x540px
# del CSS.
PAGINA = {
    "deck": dict(width="10in", height="5.625in",
                 margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}),
    "onepager": dict(width="297mm", height="210mm",
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}),
    "documento": dict(format="A4",
                      margin={"top": "20mm", "bottom": "18mm",
                              "left": "20mm", "right": "20mm"}),
}


# JS que corre en el navegador, con el documento ya maquetado. Es la única
# forma honesta de saber si algo desborda: depende de la fuente, del texto real
# y de cómo envolvió cada línea. Estimarlo desde el JSON siempre se equivoca.
_JS_DESBORDE = """
() => {
  const reportes = [];
  document.querySelectorAll('.slide').forEach((s, i) => {
    const sr = s.getBoundingClientRect();
    const cs = getComputedStyle(s);
    const pie = s.querySelector('.slide-foot');
    // El límite es el pie si existe —encimarse con él ya es un defecto— y si no
    // el borde interior de la slide.
    const limite = pie ? pie.getBoundingClientRect().top
                       : sr.bottom - parseFloat(cs.paddingBottom);
    let peor = 0, culpable = '';
    s.querySelectorAll('*').forEach(el => {
      if (pie && (el === pie || pie.contains(el))) return;
      const r = el.getBoundingClientRect();
      if (r.height === 0 || r.width === 0) return;
      const exceso = r.bottom - limite;
      if (exceso > peor) {
        peor = exceso;
        culpable = (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 46);
      }
    });
    if (peor > 1) {
      const t = s.querySelector('.slide-title');
      reportes.push({n: i + 1, titulo: t ? t.textContent.trim() : '',
                     exceso: Math.round(peor), culpable});
    }
  });
  return reportes;
}
"""


def render_pdf(html_str, out_path, formato, cliente=""):
    from playwright.sync_api import sync_playwright
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     encoding="utf-8") as f:
        f.write(html_str)
        ruta = f.name
    opts = dict(PAGINA[formato])
    if formato == "documento":
        # El documento fluye y pagina solo, así que necesita pie corrido con
        # numeración. El deck y el one-pager tienen el pie dibujado en el CSS.
        opts.update(display_header_footer=True,
                    header_template="<div></div>",
                    footer_template=(
                        '<div style="width:100%;font-size:7px;color:#A1A1AA;'
                        'font-family:Arial,sans-serif;padding:0 20mm;'
                        'display:flex;justify-content:space-between;">'
                        f'<span>{html.escape(cliente)}</span>'
                        '<span class="pageNumber"></span></div>'))
    try:
        with sync_playwright() as pw:
            navegador = pw.chromium.launch()
            pagina = navegador.new_page()
            pagina.goto(f"file://{ruta}")
            pagina.wait_for_timeout(400)
            if formato == "deck":
                for r in pagina.evaluate(_JS_DESBORDE):
                    print(f"  DESBORDE: slide {r['n']} ('{r['titulo']}') se pasa "
                          f"{r['exceso']}px del pie. Empieza a encimarse en: "
                          f"\"{r['culpable']}\". Sacá contenido o partí la slide "
                          f"— no lo dejes recortado. Ver criterio 62.",
                          file=sys.stderr)
            pagina.pdf(path=out_path, print_background=True, **opts)
            navegador.close()
    finally:
        os.unlink(ruta)


# ============================== Validación ================================= #

def controlar_distribucion(g, etiqueta, avisos):
    """Un gráfico de distribución tiene que cerrar en 100%.

    Se salta los que declaran `normalizar: false` —magnitudes independientes,
    como un antes/después de riesgo argentino, que no son partes de un todo— y
    los que vienen en montos absolutos, donde la suma no significa nada. El
    aviso salta sólo cuando los valores claramente quisieron ser porcentajes:
    suman cerca de 100 pero no 100. Ver criterio 58."""
    if get(g, "normalizar", default=True) is False:
        return
    vals = [_pct(get(it, "valor", "value", "pct", default=None))
            for it in (get(g, "items", "datos", default=[]) or [])]
    vals = [v for v in vals if v is not None]
    if len(vals) < 2:
        return
    suma = round(sum(vals), 1)
    if 95.0 <= suma <= 105.0 and abs(suma - 100.0) > 0.05:
        avisos.append(
            f"{etiqueta}: el gráfico '{get(g, 'titulo', default='sin título')}' "
            f"suma {suma:.1f}%, no 100%. Si es una distribución tiene que cerrar; "
            f"si son magnitudes independientes marcalo con \"normalizar\": false.")


def validar(p):
    """Revisa la propuesta antes de renderizar. La intención no es rechazar
    trabajo sino avisar temprano de lo que va a salir vacío o raro en el PDF,
    que es mucho más barato que descubrirlo mirando la hoja final."""
    problemas, avisos = [], []
    cli = get(p, "cliente", default=None)
    if not cli:
        problemas.append("Falta 'cliente'. La portada y el pie de cada slide lo usan.")
    if not get(p, "capitulos", default=None):
        problemas.append("Falta 'capitulos': la propuesta no tiene contenido.")

    for i, c in enumerate(get(p, "capitulos", default=[]) or []):
        tipo = (get(c, "tipo", "type", default="") or "").lower()
        et = f"capítulo {i + 1} ('{tipo or 'sin tipo'}')"
        if not tipo:
            problemas.append(f"{et}: falta 'tipo'.")
            continue
        if tipo not in CAPITULOS_DECK and tipo not in ("portada", "divisor", "cierre"):
            avisos.append(f"{et}: tipo desconocido, se renderiza como texto. "
                          f"Tipos válidos: {', '.join(sorted(CAPITULOS_DECK))}.")
        if tipo in ("cartera_sugerida", "cartera") and not get(c, "items", "posiciones"):
            problemas.append(f"{et}: no tiene 'items'; la tabla saldría vacía.")
        if tipo in ("cartera_sugerida", "cartera", "cartera_actual"):
            controlar_cierre(c, et, avisos)
        if tipo == "distribuciones":
            for g in get(c, "graficos", "items", default=[]) or []:
                if not (get(g, "items", "datos", default=[]) or []):
                    problemas.append(f"{et}: un gráfico no tiene 'items'.")
                controlar_distribucion(g, et, avisos)
        if tipo == "instrumentos" and not get(c, "fichas", "items"):
            problemas.append(f"{et}: no tiene 'fichas'.")
        if tipo in ("trades", "movimientos"):
            movs = get(c, "items", "movimientos", "trades", default=[]) or []
            if not movs:
                problemas.append(f"{et}: no tiene 'items'; la tabla saldría vacía.")
            for j, m in enumerate(movs, 1):
                if not (get(m, "sale", "vender", "desde", default="")
                        and get(m, "entra", "comprar", "hacia", default="")):
                    avisos.append(f"{et}: el movimiento {j} no tiene los dos lados. "
                                  "Un trade se lee emparejado; si es una compra o una "
                                  "venta suelta, va en 'cartera_actual'.")
        if tipo == "tabla":
            headers = get(c, "headers", "columnas", default=[]) or []
            for j, fila in enumerate(get(c, "filas", "rows", default=[]) or []):
                if len(fila) != len(headers):
                    problemas.append(f"{et}: la fila {j + 1} tiene {len(fila)} celdas "
                                     f"y hay {len(headers)} columnas.")
                    break
    return problemas, avisos


# ================================= CLI ===================================== #

def main():
    ap = argparse.ArgumentParser(
        description="Genera el PDF de una propuesta de inversión de Max Capital.")
    ap.add_argument("--json", required=True, help="Ruta al JSON de la propuesta")
    ap.add_argument("--formato", default="deck",
                    choices=sorted(CONSTRUCTORES), help="deck | onepager | documento")
    ap.add_argument("--out", help="Ruta del PDF de salida")
    ap.add_argument("--design-html", dest="design_html",
                    help="Exporta el HTML con datos reales (para editar en Claude Design)")
    ap.add_argument("--validar", action="store_true",
                    help="Solo revisa el JSON y reporta problemas")
    ap.add_argument("--assets",
                    default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                         "..", "assets"))
    args = ap.parse_args()

    with open(args.json, encoding="utf-8") as f:
        propuesta = json.load(f)

    problemas, avisos = validar(propuesta)
    for a in avisos:
        print(f"  aviso: {a}", file=sys.stderr)
    if problemas:
        print("Problemas en la propuesta:", file=sys.stderr)
        for pr in problemas:
            print(f"  - {pr}", file=sys.stderr)
        if args.validar:
            raise SystemExit(1)
        raise SystemExit("Corregí el JSON y volvé a correr (o usá --validar "
                         "para ver el detalle).")
    if args.validar:
        print("OK: la propuesta es válida.")
        return

    if not args.out and not args.design_html:
        ap.error("Indicá --out (PDF) y/o --design-html (HTML para Claude Design)")

    assets = os.path.abspath(args.assets)
    html_str = construir_html(propuesta, args.formato, assets)

    if args.design_html:
        open(args.design_html, "w", encoding="utf-8").write(html_str)
        print(f"OK (design HTML) -> {args.design_html}")
    if args.out:
        cli = get(propuesta, "cliente", default={}) or {}
        nombre = get(cli, "nombre", default="") if isinstance(cli, dict) else str(cli)
        render_pdf(html_str, args.out, args.formato, nombre)
        print(f"OK (PDF {args.formato}) -> {args.out}")


if __name__ == "__main__":
    main()
