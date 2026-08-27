from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from PIL import Image as PILImage


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "manuales"
SCREEN_DIR = OUT_DIR / "capturas-sistema"
PDF_PATH = OUT_DIR / "manual-visual-usuario-nikkhysbakery.pdf"
LOGO_PATH = ROOT / "NikkhysBakery-Front" / "public" / "assets" / "brand" / "logo-public-header.png"

BRAND = colors.HexColor("#7E4D4E")
BRAND_DARK = colors.HexColor("#3E2D2B")
MUTED = colors.HexColor("#746360")
LIGHT = colors.HexColor("#F7F1EC")
HEADER = colors.HexColor("#EDE2DC")
GREEN = colors.HexColor("#EAF4EE")
WARN = colors.HexColor("#FFF4E6")
RED = colors.HexColor("#FCEEEE")
BORDER = colors.HexColor("#E3D5CE")


def make_styles():
    base = getSampleStyleSheet()
    base.add(ParagraphStyle("TitleNikkhys", parent=base["Title"], fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=BRAND, alignment=TA_CENTER, spaceAfter=3))
    base.add(ParagraphStyle("SubNikkhys", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=BRAND_DARK, alignment=TA_CENTER, spaceAfter=8))
    base.add(ParagraphStyle("MetaNikkhys", parent=base["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=10))
    base.add(ParagraphStyle("H1Nikkhys", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=BRAND, spaceBefore=8, spaceAfter=6))
    base.add(ParagraphStyle("H2Nikkhys", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=BRAND, spaceBefore=6, spaceAfter=4))
    base.add(ParagraphStyle("BodyNikkhys", parent=base["BodyText"], fontName="Helvetica", fontSize=9.3, leading=12.2, textColor=BRAND_DARK, spaceAfter=5))
    base.add(ParagraphStyle("SmallNikkhys", parent=base["BodyText"], fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=BRAND_DARK))
    base.add(ParagraphStyle("HeadNikkhys", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.2, leading=10, textColor=BRAND))
    return base


S = make_styles()


def p(text, style="BodyNikkhys"):
    return Paragraph(text, S[style])


def h1(text):
    return Paragraph(text, S["H1Nikkhys"])


def h2(text):
    return Paragraph(text, S["H2Nikkhys"])


def callout(title, body, fill=LIGHT):
    t = Table([[p(f"<b>{title}</b>", "SmallNikkhys")], [p(body, "SmallNikkhys")]], colWidths=[6.45 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([t, Spacer(1, 6)])


def data_table(headers, rows, widths):
    data = [[p(head, "HeadNikkhys") for head in headers]]
    for row in rows:
        data.append([p(str(cell), "SmallNikkhys") for cell in row])
    t = Table(data, colWidths=[w * inch for w in widths], hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FBF8F5")),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return KeepTogether([t, Spacer(1, 7)])


def screenshot(name, max_width=6.45 * inch, max_height=4.15 * inch):
    path = SCREEN_DIR / f"{name}.png"
    with PILImage.open(path) as img:
        width, height = img.size
    scale = min(max_width / width, max_height / height)
    image = Image(str(path), width=width * scale, height=height * scale)
    image.hAlign = "CENTER"
    return image


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(0.85 * inch, 0.55 * inch, 7.65 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 7.8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(4.25 * inch, 0.35 * inch, f"Manual visual NikkhysBakery · Pagina {doc.page}")
    canvas.restoreState()


def page_with_screenshot(story, title, image_name, intro, rows, note=None, note_fill=LIGHT):
    story.append(h1(title))
    story.append(p(intro))
    story.append(screenshot(image_name))
    story.append(Spacer(1, 8))
    story.append(data_table(["Zona de la pantalla", "Que hacer", "Ejemplo real visible"], rows, [1.75, 2.7, 2.0]))
    if note:
        story.append(callout("Nota operativa", note, note_fill))
    story.append(PageBreak())


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(PDF_PATH), pagesize=letter, rightMargin=0.85 * inch, leftMargin=0.85 * inch, topMargin=0.72 * inch, bottomMargin=0.72 * inch, title="Manual visual de usuario NikkhysBakery", author="NikkhysBakery")

    story = []
    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=0.55 * inch, height=0.68 * inch)
        logo.hAlign = "CENTER"
        story.extend([logo, Spacer(1, 8)])
    story.extend([
        p("NikkhysBakery", "TitleNikkhys"),
        p("Manual visual con ejemplos reales del sistema", "SubNikkhys"),
        p("Stock, recetas, produccion y ventas · Capturas reales del panel local", "MetaNikkhys"),
        callout("Objetivo", "Mostrar donde entrar, que mirar y que accion realizar usando pantallas reales del sistema. Este manual sirve para capacitar al equipo operativo sin depender de explicaciones largas.", LIGHT),
        data_table(["Flujo", "Pantalla real usada", "Ejemplo del sitio"], [
            ("Stock", "Inventario operativo", "Aceite de oliva, Agua, Azucar y Azucar flor."),
            ("Recetas", "Fichas tecnicas y costos base", "Pan amasado, Focaccia, Receta y Trampa falso."),
            ("Produccion", "Ordenes de produccion", "Trampa falso completada y alerta real de Pan amasado."),
            ("Ventas", "Ordenes / POS", "Americano, Capuchino, Chocolate caliente, Cortado y Espresso."),
        ], [1.25, 2.65, 2.55]),
        PageBreak(),
    ])

    page_with_screenshot(
        story,
        "1. Entrar al panel y ubicarse",
        "01-dashboard",
        "Al iniciar sesion, el usuario llega al panel administrativo. Desde aqui debe usar el menu lateral para entrar al modulo correcto.",
        [
            ("Menu lateral", "Elegir el modulo de trabajo.", "Iconos de dashboard, POS, inventario, recetas y produccion."),
            ("Buscador superior", "Buscar rapido si el modulo tiene mucha informacion.", "Campo Buscar en la barra superior."),
            ("Usuario activo", "Confirmar que estas operando con la cuenta correcta.", "Usuario Capacitacion con rol ADMIN."),
        ],
        "Antes de operar stock o ventas, confirma que estas en la sucursal correcta cuando la pantalla lo solicite.",
        GREEN,
    )

    page_with_screenshot(
        story,
        "2. Revisar stock real",
        "03-stock-inventario",
        "Inventario operativo muestra el stock disponible por sucursal. En esta captura se ve el alcance Casa Matriz y una lista real de materias primas.",
        [
            ("Alcance", "Trabajar por sucursal o vista global si eres administrador.", "Casa Matriz y Global."),
            ("Pestanas", "Cambiar entre Stock, Catalogo, Ubicaciones, Ingresos, Ajustes y Mermas.", "Stock esta seleccionado."),
            ("Stock actual", "Revisar item, ubicacion, cantidad, valor y estado.", "Aceite de oliva 5.005 ml, Agua 1.002 ml, Azucar 2.650 g."),
        ],
        "Usa Ingresos para compras reales, Ajustes para diferencias de conteo y Mermas para perdidas o vencimientos.",
        LIGHT,
    )

    page_with_screenshot(
        story,
        "3. Crear o revisar recetas reales",
        "04-recetas",
        "Recetas concentra las fichas tecnicas. Aqui se define que insumos consume una preparacion y que producto de venta queda asociado.",
        [
            ("Crear receta", "Completar nombre, tipo y producto de venta que genera la receta.", "Campo con ejemplo Pan amasado."),
            ("Producto de venta", "Seleccionar el producto POS que quedara con stock o disponibilidad.", "Selector de producto terminado."),
            ("Listado", "Abrir recetas existentes y revisar si estan activas.", "Focaccia, Pan amasado, Receta, Trampa falso."),
        ],
        "La materia prima no se selecciona como producto de venta. La receta consume materia prima y alimenta un producto POS.",
        WARN,
    )

    page_with_screenshot(
        story,
        "4. Produccion con alerta real",
        "05-produccion",
        "Produccion permite planificar, crear y completar ordenes. La captura muestra una alerta real: Pan amasado no aparecera si no tiene producto producido o disponibilidad configurada.",
        [
            ("Alerta superior", "Leer antes de producir: indica que receta no esta lista para produccion.", "Pan amasado aparece en la alerta."),
            ("Crear orden", "Seleccionar receta activa, ubicacion y cantidad planificada.", "Receta v1 y Stock general."),
            ("Planificar produccion", "Calcular insumos requeridos y faltantes antes de confirmar.", "Boton Calcular requerimientos."),
            ("Ordenes", "Revisar ordenes existentes y estado.", "Trampa falso terminada."),
        ],
        "Si ves una alerta como la de Pan amasado, corrige la receta/producto antes de intentar producir. La orden se completa solo cuando realmente se produjo.",
        RED,
    )

    page_with_screenshot(
        story,
        "5. Vender en Ordenes / POS",
        "06-pos-ordenes",
        "POS es la pantalla de caja. Desde aqui se agregan productos reales, se arma la orden y se cierra la venta.",
        [
            ("Canal", "Elegir Mesa, Retiro o Despacho segun corresponda.", "Mesa esta seleccionada."),
            ("Categorias", "Filtrar productos por cafeteria, panaderia o pasteleria.", "Cafeteria, Panaderia, Pasteleria."),
            ("Productos", "Agregar productos disponibles a la orden.", "Americano doble $2.900, Capuchino simple $2.700, Chocolate caliente $3.500."),
            ("Ordenes", "Ver ordenes recientes del sistema.", "La pantalla indica 0 registros en la vista actual."),
        ],
        "Si un producto no aparece o no deja agregarlo, revisa que este activo y que tenga stock o disponibilidad en la sucursal.",
        GREEN,
    )

    page_with_screenshot(
        story,
        "6. Reporte de stock",
        "07-reporte-stock",
        "El reporte de stock sirve para revisar existencias sin modificar datos. Es ideal para supervisores y administradores.",
        [
            ("Filtros", "Elegir sucursal, ubicacion o tipo si necesitas acotar.", "Reporte de inventario stock."),
            ("Resultados", "Comparar item, cantidad, ubicacion y estado.", "Usar para detectar bajo minimo o negativo."),
            ("Accion", "Si encuentras diferencia, ir a movimientos antes de ajustar.", "Evita corregir sin entender el origen."),
        ],
        "El reporte no reemplaza el Kardex ni los movimientos: si hay dudas, revisa el historial antes de registrar ajustes.",
        LIGHT,
    )

    story.extend([
        h1("7. Flujo real recomendado para capacitar"),
        data_table(["Paso", "Pantalla", "Ejemplo real"], [
            ("1", "Inventario", "Revisar stock de Agua, Azucar o Aceite de oliva en Casa Matriz."),
            ("2", "Recetas", "Abrir Pan amasado y validar producto de venta asociado."),
            ("3", "Produccion", "Planificar con receta activa y corregir alertas antes de crear orden."),
            ("4", "POS", "Vender Americano simple, Capuchino simple o productos de pasteleria disponibles."),
            ("5", "Reportes", "Revisar stock y movimientos si algo no coincide."),
        ], [0.7, 1.6, 4.15]),
        callout("Regla final", "Cada cosa tiene su lugar: compras e inventario en Stock, formulas en Recetas, transformacion en Produccion y cobro en POS. Si se respeta ese orden, los reportes quedan confiables.", GREEN),
    ])

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
