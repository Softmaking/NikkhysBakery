from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "manuales"
PDF_PATH = OUT_DIR / "manual-rapido-usuario-nikkhysbakery.pdf"
LOGO_PATH = ROOT / "NikkhysBakery-Front" / "public" / "assets" / "brand" / "logo-public-header.png"

BRAND = colors.HexColor("#7E4D4E")
BRAND_DARK = colors.HexColor("#3E2D2B")
MUTED = colors.HexColor("#746360")
LIGHT = colors.HexColor("#F7F1EC")
LIGHT_2 = colors.HexColor("#FBF8F5")
HEADER = colors.HexColor("#EDE2DC")
GREEN = colors.HexColor("#EAF4EE")
WARN = colors.HexColor("#FFF4E6")
RED = colors.HexColor("#FCEEEE")
BORDER = colors.HexColor("#E3D5CE")


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            "ManualTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=29,
            textColor=BRAND,
            alignment=TA_CENTER,
            spaceAfter=2,
        )
    )
    base.add(
        ParagraphStyle(
            "ManualSubtitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=BRAND_DARK,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "ManualMeta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "H1Manual",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=BRAND,
            spaceBefore=10,
            spaceAfter=7,
        )
    )
    base.add(
        ParagraphStyle(
            "H2Manual",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.2,
            leading=15,
            textColor=BRAND,
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            "BodyManual",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10,
            leading=13.2,
            textColor=BRAND_DARK,
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            "SmallManual",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=11.5,
            textColor=BRAND_DARK,
        )
    )
    base.add(
        ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=10.5,
            textColor=BRAND,
        )
    )
    base.add(
        ParagraphStyle(
            "Footer",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    return base


S = styles()


def p(text, style="BodyManual"):
    return Paragraph(text, S[style])


def section(title):
    return Paragraph(title, S["H1Manual"])


def subsection(title):
    return Paragraph(title, S["H2Manual"])


def callout(title, body, fill=LIGHT):
    data = [[p(f"<b>{title}</b>", "SmallManual")], [p(body, "SmallManual")]]
    table = Table(data, colWidths=[6.45 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return KeepTogether([table, Spacer(1, 7)])


def data_table(headers, rows, widths):
    data = [[p(h, "TableHeader") for h in headers]]
    for row in rows:
        data.append([p(str(v), "SmallManual") for v in row])
    table = Table(data, colWidths=[w * inch for w in widths], hAlign="LEFT", repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT_2),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return KeepTogether([table, Spacer(1, 8)])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(0.85 * inch, 0.55 * inch, 7.65 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(4.25 * inch, 0.35 * inch, f"Manual rapido de uso NikkhysBakery · Pagina {doc.page}")
    canvas.restoreState()


def build():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=0.85 * inch,
        leftMargin=0.85 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.72 * inch,
        title="Manual rapido de uso NikkhysBakery",
        author="NikkhysBakery",
        subject="Stock, recetas, produccion y ventas",
    )

    story = []
    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=0.55 * inch, height=0.68 * inch)
        logo.hAlign = "CENTER"
        story.extend([logo, Spacer(1, 8)])
    story.extend(
        [
            p("NikkhysBakery", "ManualTitle"),
            p("Manual rapido de uso", "ManualSubtitle"),
            p("Stock, recetas, produccion y ventas · Version mayo 2026", "ManualMeta"),
            callout(
                "Objetivo",
                "Explicar el flujo operativo diario en pocas paginas: revisar stock, mantener recetas, producir y vender sin perder trazabilidad.",
                LIGHT,
            ),
            data_table(
                ["Tema", "Que resuelve"],
                [
                    ("Stock", "Saber que materia prima y producto vendible hay por sucursal."),
                    ("Recetas", "Definir que insumos consume cada preparacion y que resultado genera."),
                    ("Produccion", "Transformar insumos en producto disponible o stock vendible."),
                    ("Ventas", "Vender en POS respetando stock, disponibilidad y cierre de caja."),
                ],
                [1.35, 5.1],
            ),
            section("1. Antes de operar: idea clave"),
            p(
                "El sistema separa inventario de materia prima, recetas, produccion y productos de venta. "
                "Esa separacion evita confundir harina, leche o cafe con los productos que el cliente compra en el POS."
            ),
            data_table(
                ["Concepto", "Uso correcto", "Ejemplo"],
                [
                    ("Materia prima", "Insumos que se compran, reciben y consumen.", "Harina, mantequilla, cafe molido, leche."),
                    ("Producto de venta", "Producto visible en POS para vender al cliente.", "Pan amasado, capuchino, cheesecake."),
                    ("Receta", "Define insumos, rendimiento teorico y producto asociado.", "Pan amasado consume harina, agua, sal y levadura."),
                    ("Produccion", "Consume materia prima y habilita stock o disponibilidad.", "Completar produccion de pan para venderlo."),
                ],
                [1.25, 3.1, 2.1],
            ),
            callout(
                "Regla practica",
                "Si quieres producir, revisa receta e inventario. Si quieres vender, revisa producto de venta y disponibilidad por sucursal.",
                GREEN,
            ),
            PageBreak(),
            section("2. Rutina diaria recomendada"),
            data_table(
                ["Momento", "Accion", "Resultado esperado"],
                [
                    ("Inicio", "Elegir sucursal activa y revisar stock bajo o productos agotados.", "El equipo sabe que puede producir y vender."),
                    ("Antes de producir", "Planificar produccion desde una receta activa.", "Se ven insumos requeridos, disponibles y faltantes."),
                    ("Durante el dia", "Vender en POS y marcar agotado cuando corresponda.", "No se venden productos sin stock o sin disponibilidad."),
                    ("Cierre", "Revisar ventas, movimientos y producciones completadas.", "Queda trazabilidad para reportes y reposicion."),
                ],
                [1.15, 3.35, 1.95],
            ),
            section("3. Stock e inventario"),
            subsection("Que revisar"),
            p(
                "En inventario se administran materias primas, ubicaciones, ingresos, ajustes, mermas y stock por sucursal. "
                "Para operacion diaria, lo mas importante es confirmar que la sucursal tenga stock suficiente antes de producir."
            ),
            data_table(
                ["Operacion", "Cuando usarla", "Cuidado"],
                [
                    ("Ingreso", "Cuando entra compra o reposicion de insumos.", "Registrar costo total y unidad correcta."),
                    ("Ajuste", "Cuando el conteo real no coincide con el sistema.", "Usarlo con motivo claro; no reemplaza una venta."),
                    ("Merma", "Cuando se pierde producto o insumo.", "Registrar para no ocultar diferencias de stock."),
                    ("Movimientos", "Cuando necesitas investigar cambios.", "Filtrar por sucursal, fecha e item."),
                ],
                [1.25, 3.05, 2.15],
            ),
            callout(
                "Sucursal",
                "El stock operativo se trabaja por sucursal. Un administrador puede ver stock global, pero las entradas, mermas y producciones deben quedar asociadas a una sucursal concreta.",
                LIGHT,
            ),
            PageBreak(),
            section("4. Recetas"),
            p(
                "Una receta sirve para saber que insumos se consumen, cuanto cuesta producir y que producto queda disponible para vender. "
                "Las recetas se trabajan por versiones: una version puede estar en borrador y solo una version queda activa para operar."
            ),
            data_table(
                ["Paso", "Que hacer", "Verificacion"],
                [
                    ("Crear receta", "Indicar nombre, tipo y producto asociado para venta cuando corresponda.", "El producto asociado debe existir en Productos."),
                    ("Agregar insumos", "Registrar materias primas y cantidades de la preparacion.", "Las unidades deben coincidir o tener conversion."),
                    ("Definir rendimiento", "Indicar cuanto produce la receta para costeo y planificacion.", "Ej.: 30 unidades teoricas o una preparacion."),
                    ("Crear version", "Guardar la version de receta.", "Queda como borrador hasta activarla."),
                    ("Activar version", "Activar cuando este completa y validada.", "Produccion y costos usaran esa version."),
                ],
                [1.15, 3.35, 1.95],
            ),
            callout(
                "Producto por disponibilidad",
                "Para productos como pan vendido por monto, el rendimiento se usa para costeo. La venta no descuenta unidades; el equipo marca el producto como agotado cuando ya no queda.",
                WARN,
            ),
            PageBreak(),
            section("5. Produccion"),
            p(
                "Produccion transforma materia prima en producto terminado o en disponibilidad para vender. Crear una orden no consume stock; el consumo ocurre al completar la produccion."
            ),
            data_table(
                ["Accion", "Que revisar", "Que pasa en sistema"],
                [
                    ("Planificar", "Receta activa, sucursal y cantidad a producir.", "Muestra requeridos, disponibles y faltantes."),
                    ("Crear orden", "Notas, sucursal y cantidad planificada.", "La orden queda registrada para seguimiento."),
                    ("Confirmar", "Que se ejecutara la produccion.", "La orden avanza de estado."),
                    ("Completar", "Que se produjo realmente.", "Consume insumos y aumenta stock vendible o disponibilidad."),
                    ("Cancelar", "Solo si la produccion no seguira.", "La orden queda cerrada sin completar consumo."),
                ],
                [1.2, 3.05, 2.2],
            ),
            callout(
                "Si no deja producir",
                "Revisa que exista sucursal activa, receta con version activa, insumos configurados, producto asociado y stock suficiente de materias primas.",
                RED,
            ),
            PageBreak(),
            section("6. Ventas / POS"),
            p(
                "El POS se usa para crear ordenes, agregar productos, enviar a cocina cuando corresponda y cerrar la venta. "
                "El sistema valida el stock o disponibilidad antes de vender y guarda el costo historico al cerrar."
            ),
            data_table(
                ["Tipo de producto", "Como se vende", "Efecto en stock"],
                [
                    ("Stock vendible", "Se agrega al POS con cantidad.", "Descuenta producto terminado al cerrar la orden."),
                    ("Disponibilidad", "Se vende mientras este disponible.", "No descuenta unidades; se marca agotado manualmente."),
                    ("Receta directa", "Se prepara al momento.", "Consume insumos de la receta activa al cerrar."),
                    ("Sin inventario", "Se vende sin control de stock.", "No mueve inventario."),
                ],
                [1.65, 2.45, 2.35],
            ),
            callout(
                "Cierre de venta",
                "El inventario se descuenta al cerrar la orden, no solo al agregar productos. Si el producto no tiene stock o esta agotado, no debe venderse.",
                GREEN,
            ),
            section("7. Flujo completo recomendado"),
            data_table(
                ["Orden", "Modulo", "Accion breve"],
                [
                    ("1", "Inventario", "Registrar ingresos de materia prima con costo y sucursal correctos."),
                    ("2", "Productos", "Configurar productos de venta y su modo de inventario."),
                    ("3", "Recetas", "Crear receta, asociar producto, agregar insumos y activar version."),
                    ("4", "Produccion", "Planificar, crear, confirmar y completar la orden."),
                    ("5", "POS", "Vender productos disponibles y cerrar ordenes."),
                    ("6", "Reportes", "Revisar ventas, stock, movimientos y produccion para corregir desviaciones."),
                ],
                [0.7, 1.35, 4.4],
            ),
            PageBreak(),
            section("8. Problemas comunes"),
            data_table(
                ["Situacion", "Que revisar primero"],
                [
                    ("No aparece una receta en produccion", "Debe tener version activa y producto asociado/resultado valido."),
                    ("No deja activar una receta", "Faltan insumos, rendimiento o datos requeridos de la version."),
                    ("No deja vender un producto", "Puede estar sin stock vendible, agotado, inactivo o sin sucursal correcta."),
                    ("El stock no coincide", "Revisar movimientos, ubicacion, sucursal, ajustes y mermas."),
                    ("Produccion no descuenta insumos", "Verificar que la orden se completo; crear la orden no consume stock."),
                ],
                [2.6, 3.85],
            ),
            section("9. Reglas de oro"),
            data_table(
                ["Regla", "Aplicacion diaria"],
                [
                    ("No mezclar inventario y POS", "Inventario es materia prima; POS vende productos."),
                    ("Siempre operar con sucursal correcta", "Evita stock duplicado, ventas bloqueadas y reportes incorrectos."),
                    ("No producir sin receta activa", "La receta activa es la fuente para consumo y costo."),
                    ("Registrar mermas y ajustes con motivo", "Permite explicar diferencias reales."),
                    ("Cerrar ventas al final del flujo", "El cierre deja trazabilidad y mueve stock cuando corresponde."),
                ],
                [2.15, 4.3],
            ),
            p(
                "Este manual es una guia rapida. Para dudas de permisos, configuracion avanzada o reportes, consultar al administrador del sistema.",
                "SmallManual",
            ),
        ]
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
