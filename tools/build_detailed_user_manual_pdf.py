from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "manuales"
PDF_PATH = OUT_DIR / "manual-detallado-usuario-nikkhysbakery.pdf"
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
BLUE = colors.HexColor("#EEF4FA")
BORDER = colors.HexColor("#E3D5CE")


def make_styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=BRAND,
            alignment=TA_CENTER,
            spaceAfter=3,
        )
    )
    base.add(
        ParagraphStyle(
            "CoverSubtitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=BRAND_DARK,
            alignment=TA_CENTER,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "CoverMeta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    base.add(
        ParagraphStyle(
            "H1",
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
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=BRAND,
            spaceBefore=8,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=12.5,
            textColor=BRAND_DARK,
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=10.8,
            textColor=BRAND_DARK,
        )
    )
    base.add(
        ParagraphStyle(
            "SmallBold",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.4,
            leading=10.8,
            textColor=BRAND_DARK,
        )
    )
    base.add(
        ParagraphStyle(
            "TableHead",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            textColor=BRAND,
        )
    )
    base.add(
        ParagraphStyle(
            "Footer",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    return base


S = make_styles()


def p(text, style="Body"):
    return Paragraph(text, S[style])


def h1(text):
    return Paragraph(text, S["H1"])


def h2(text):
    return Paragraph(text, S["H2"])


def callout(title, body, fill=LIGHT):
    table = Table(
        [[p(f"<b>{title}</b>", "Small")], [p(body, "Small")]],
        colWidths=[6.45 * inch],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fill),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return KeepTogether([table, Spacer(1, 7)])


def table(headers, rows, widths, keep=True):
    data = [[p(head, "TableHead") for head in headers]]
    for row in rows:
        data.append([p(str(value), "Small") for value in row])
    t = Table(data, colWidths=[w * inch for w in widths], hAlign="LEFT", repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEADER),
                ("BACKGROUND", (0, 1), (-1, -1), LIGHT_2),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return KeepTogether([t, Spacer(1, 8)]) if keep else t


def steps(rows):
    return [table(["Paso", "Accion en el sistema", "Ejemplo / resultado esperado"], rows, [0.7, 3.2, 2.55], keep=False), Spacer(1, 8)]


def example(title, rows):
    return KeepTogether(
        [
            callout(title, "Ejemplo practico para entrenar al usuario antes de operar con datos reales.", BLUE),
            table(["Dato", "Valor de ejemplo", "Para que sirve"], rows, [1.35, 2.35, 2.75], keep=False),
        ]
    )


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(0.85 * inch, 0.55 * inch, 7.65 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 7.8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(4.25 * inch, 0.35 * inch, f"Manual detallado NikkhysBakery · Pagina {doc.page}")
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
        title="Manual detallado de uso NikkhysBakery",
        author="NikkhysBakery",
        subject="Guia detallada para stock, recetas, produccion y ventas",
    )

    story = []
    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=0.55 * inch, height=0.68 * inch)
        logo.hAlign = "CENTER"
        story.extend([logo, Spacer(1, 8)])

    story.extend(
        [
            p("NikkhysBakery", "CoverTitle"),
            p("Manual detallado de uso", "CoverSubtitle"),
            p("Stock, recetas, produccion y ventas · Version mayo 2026", "CoverMeta"),
            callout(
                "Como usar este manual",
                "Primero lee el flujo general. Luego usa los ejemplos para practicar: ingreso de stock, receta, produccion y venta. El objetivo es que el equipo opere sin depender de memoria o instrucciones informales.",
                LIGHT,
            ),
            table(
                ["Capitulo", "Que aprenderas"],
                [
                    ("1. Mapa del sistema", "Como se relacionan inventario, recetas, produccion y POS."),
                    ("2. Stock", "Como ingresar, ajustar, revisar movimientos y evitar confusiones por sucursal."),
                    ("3. Recetas", "Como crear receta, versiones, insumos, rendimiento y producto asociado."),
                    ("4. Produccion", "Como planificar, crear, confirmar y completar ordenes."),
                    ("5. Ventas / POS", "Como vender productos con stock, disponibilidad o receta directa."),
                    ("6. Ejemplos completos", "Casos de pan amasado, cheesecake y cafe preparado."),
                ],
                [1.8, 4.65],
            ),
            PageBreak(),
            h1("1. Mapa del sistema"),
            p(
                "NikkhysBakery separa lo que compras, lo que produces y lo que vendes. Esta es la idea mas importante para evitar errores: inventario no es lo mismo que producto de venta."
            ),
            table(
                ["Elemento", "Que representa", "Donde impacta"],
                [
                    ("Inventario / materia prima", "Insumos fisicos que entran y salen.", "Stock, movimientos, costo promedio, produccion."),
                    ("Producto de venta", "Producto visible para el cajero en POS.", "Catalogo, precio, stock vendible o disponibilidad."),
                    ("Receta", "Formula que consume insumos y genera resultado.", "Costeo, produccion, receta directa."),
                    ("Produccion", "Orden que transforma insumos en producto o disponibilidad.", "Stock vendible, disponibilidad, movimientos."),
                    ("Venta", "Orden POS cerrada con productos y pagos.", "Ingresos, reportes, consumo de inventario."),
                ],
                [1.55, 2.75, 2.15],
            ),
            callout(
                "Regla simple",
                "Si el problema es 'no tengo harina', se revisa Inventario. Si el problema es 'no puedo vender pan', se revisa Producto, Produccion y disponibilidad.",
                GREEN,
            ),
            h2("Estados que debes reconocer"),
            table(
                ["Estado", "Significado", "Que hacer"],
                [
                    ("Borrador", "La receta o version aun no opera.", "Completar datos y activar cuando este lista."),
                    ("Activa", "La version o producto puede operar.", "Usarla para producir o vender."),
                    ("Agotado", "Producto por disponibilidad no se puede vender.", "Marcar disponible tras nueva produccion."),
                    ("Cerrada", "Venta finalizada.", "Ya impacta reportes y stock si corresponde."),
                ],
                [1.45, 3.0, 2.0],
            ),
            PageBreak(),
            h1("2. Stock e inventario"),
            p(
                "El modulo de inventario se usa para controlar materias primas y, cuando corresponde, productos terminados. Siempre revisa la sucursal antes de ingresar o consultar stock."
            ),
            h2("2.1 Revisar stock"),
            *steps(
                [
                    ("1", "Entrar a Inventario / Stock.", "Veras items, ubicaciones y cantidades."),
                    ("2", "Seleccionar sucursal o validar que la sucursal activa sea correcta.", "Casa Matriz, local u otra sucursal."),
                    ("3", "Buscar el insumo o producto terminado.", "Ej.: Harina, leche, cheesecake."),
                    ("4", "Revisar cantidad disponible, minimo e ideal.", "Si esta bajo minimo, planificar compra o produccion."),
                ]
            ),
            h2("2.2 Registrar ingreso de materia prima"),
            *steps(
                [
                    ("1", "Entrar a Inventario / Ingresos.", "Usar cuando llega una compra."),
                    ("2", "Elegir item, ubicacion, cantidad y unidad.", "Ej.: Harina, bodega, 25 kg."),
                    ("3", "Ingresar costo total.", "Ej.: $18.000 por el saco completo."),
                    ("4", "Guardar ingreso.", "El sistema actualiza stock y costo promedio."),
                ]
            ),
            example(
                "Ejemplo: ingreso de harina",
                [
                    ("Item", "Harina", "Materia prima que se consume en recetas."),
                    ("Cantidad", "25 kg", "Aumenta stock disponible."),
                    ("Costo total", "$18.000", "Permite calcular costo promedio."),
                    ("Sucursal", "Casa Matriz", "Evita mezclar stock entre locales."),
                ],
            ),
            PageBreak(),
            h2("2.3 Ajustes y mermas"),
            table(
                ["Operacion", "Cuando usar", "Ejemplo"],
                [
                    ("Ajuste positivo", "El conteo real es mayor que el sistema.", "Aparecieron 2 kg adicionales de azucar."),
                    ("Ajuste negativo", "El conteo real es menor sin ser venta.", "Conteo detecta 1 kg menos de harina."),
                    ("Merma", "Hubo perdida, vencimiento o producto inutilizable.", "Leche vencida o masa quemada."),
                    ("Movimiento", "Necesitas auditar que paso con el stock.", "Ver compras, consumos, mermas y producciones."),
                ],
                [1.45, 3.05, 1.95],
            ),
            callout(
                "Cuidado",
                "No uses ajustes para esconder ventas o producciones. Los ajustes explican diferencias de conteo; las ventas y producciones deben pasar por su flujo real.",
                WARN,
            ),
            h2("2.4 Buenas practicas de stock"),
            table(
                ["Practica", "Por que importa"],
                [
                    ("Registrar compras el mismo dia", "Evita producir con stock desactualizado."),
                    ("Usar unidades correctas", "Un error entre gramos, kilos o unidades altera costos."),
                    ("Separar sucursales", "Una sucursal no debe consumir stock de otra sin movimiento real."),
                    ("Registrar merma", "Permite entender perdidas y ajustar decisiones."),
                    ("Revisar movimientos antes de corregir", "Evita duplicar ingresos o ajustes."),
                ],
                [2.25, 4.2],
            ),
            PageBreak(),
            h1("3. Recetas"),
            p(
                "Una receta define que insumos se usan, cuanto rinde y que producto queda asociado. La receta puede tener varias versiones, pero solo una version activa opera para costos, produccion o receta directa."
            ),
            h2("3.1 Crear receta"),
            *steps(
                [
                    ("1", "Entrar a Recetas y seleccionar crear.", "Se abre formulario de nueva receta."),
                    ("2", "Indicar nombre y tipo.", "Ej.: Pan amasado, tipo Produccion."),
                    ("3", "Seleccionar producto asociado si la receta alimenta una venta.", "Ej.: producto POS Pan amasado."),
                    ("4", "Guardar receta.", "Luego se agregan versiones e insumos."),
                ]
            ),
            h2("3.2 Crear version de receta"),
            *steps(
                [
                    ("1", "Abrir la receta y crear version.", "La version queda en borrador."),
                    ("2", "Agregar insumos con cantidades.", "Ej.: harina, levadura, sal, agua."),
                    ("3", "Definir rendimiento teorico.", "Ej.: 30 unidades teoricas o 1 preparacion."),
                    ("4", "Revisar costo de receta.", "Usa costo promedio vigente del inventario."),
                    ("5", "Activar version.", "Solo cuando la receta este completa y lista."),
                ]
            ),
            callout(
                "Importante",
                "Si una receta no tiene version activa, no debe aparecer como opcion operativa en produccion. Si no tiene producto asociado cuando corresponde, no podra alimentar stock o disponibilidad de venta.",
                RED,
            ),
            PageBreak(),
            h2("3.3 Tipos de receta y producto asociado"),
            table(
                ["Caso", "Configuracion recomendada", "Ejemplo"],
                [
                    ("Producto terminado contado", "Producto de venta con stock vendible.", "Cheesecake individual: produce unidades y luego se descuentan al vender."),
                    ("Producto por disponibilidad", "Producto de venta con disponibilidad.", "Pan vendido por monto: se habilita disponible y se marca agotado."),
                    ("Preparacion al momento", "Producto con receta directa.", "Cafe preparado consume cafe molido y leche al cerrar venta."),
                    ("Producto sin inventario", "No consume ni produce stock.", "Servicio o producto externo sin control."),
                ],
                [1.75, 3.0, 1.7],
            ),
            example(
                "Ejemplo: receta de pan amasado",
                [
                    ("Producto asociado", "Pan amasado", "Producto que se vende en POS."),
                    ("Modo", "Disponibilidad", "No descuenta panes por unidad."),
                    ("Rendimiento", "30 unidades teoricas", "Sirve para costo y planificacion."),
                    ("Insumos", "Harina, agua, sal, levadura", "Se consumen al completar produccion."),
                ],
            ),
            example(
                "Ejemplo: receta de cheesecake",
                [
                    ("Producto asociado", "Cheesecake Frambuesa", "Producto de venta contado."),
                    ("Modo", "Stock vendible", "Baja unidades al vender."),
                    ("Rendimiento", "12 porciones", "Cada produccion aumenta stock vendible."),
                    ("Insumos", "Queso crema, galleta, mantequilla", "Se consumen al completar produccion."),
                ],
            ),
            PageBreak(),
            h1("4. Produccion"),
            p(
                "Produccion es el paso donde el sistema consume materias primas y deja producto disponible para venta. Crear una orden no mueve stock; completar la orden si mueve stock."
            ),
            h2("4.1 Planificar antes de producir"),
            *steps(
                [
                    ("1", "Entrar a Produccion / Planificar.", "Seleccionar receta activa."),
                    ("2", "Elegir sucursal y cantidad a producir.", "Ej.: 1 tanda de pan amasado."),
                    ("3", "Calcular requerimientos.", "El sistema muestra insumos requeridos, disponibles y faltantes."),
                    ("4", "Corregir faltantes antes de crear orden.", "Ingresar stock o bajar cantidad planificada."),
                ]
            ),
            h2("4.2 Crear y completar orden"),
            *steps(
                [
                    ("1", "Crear orden de produccion.", "Queda registrada con receta, sucursal y cantidad."),
                    ("2", "Confirmar orden.", "Indica que la produccion se ejecutara."),
                    ("3", "Completar orden.", "Aqui se consumen insumos y se habilita producto o disponibilidad."),
                    ("4", "Revisar resultado.", "Ver stock vendible, disponibilidad o movimientos."),
                ]
            ),
            callout(
                "Si no deja crear o completar",
                "Revisa sucursal activa, receta con version activa, insumos configurados, producto asociado y stock suficiente. Si el producto es por disponibilidad, confirma que la venta se controle por disponible/agotado.",
                RED,
            ),
            PageBreak(),
            h2("4.3 Que pasa al completar"),
            table(
                ["Producto asociado", "Efecto de completar", "Efecto al vender"],
                [
                    ("Stock vendible", "Aumenta stock terminado en sucursal.", "Baja unidades al cerrar venta."),
                    ("Disponibilidad", "Marca producto disponible en sucursal.", "No baja unidades; se marca agotado manualmente."),
                    ("Receta directa", "Normalmente no se produce por lote.", "Consume insumos al cerrar venta."),
                ],
                [1.7, 2.65, 2.1],
            ),
            example(
                "Ejemplo: producir pan amasado",
                [
                    ("Receta", "Pan amasado v1 activa", "Fuente de insumos y costo."),
                    ("Cantidad", "1 tanda", "Planificacion del dia."),
                    ("Resultado", "Pan disponible", "El cajero puede vender mientras haya pan."),
                    ("Agotado", "Marcar cuando no quede", "Bloquea ventas futuras hasta nueva produccion."),
                ],
            ),
            PageBreak(),
            h1("5. Ventas / POS"),
            p(
                "POS es el flujo de caja y atencion. El cajero agrega productos, envia a cocina si corresponde y cierra la orden. El impacto en inventario ocurre segun el modo de inventario del producto."
            ),
            h2("5.1 Crear venta"),
            *steps(
                [
                    ("1", "Entrar a Ordenes / POS.", "Seleccionar mesa/canal si aplica."),
                    ("2", "Agregar productos.", "El sistema valida stock o disponibilidad."),
                    ("3", "Enviar a cocina si corresponde.", "Productos con estaciones generan tickets."),
                    ("4", "Confirmar pago y cerrar orden.", "La venta queda registrada y mueve stock cuando corresponde."),
                ]
            ),
            h2("5.2 Que validar antes de vender"),
            table(
                ["Caso", "Validacion", "Accion del cajero"],
                [
                    ("Producto con stock vendible", "Debe existir stock suficiente en la sucursal.", "Si no hay stock, no vender o producir primero."),
                    ("Producto por disponibilidad", "Debe estar disponible.", "Si se acabo, marcar agotado."),
                    ("Producto receta directa", "Debe tener receta activa e insumos.", "Cerrar venta consume insumos."),
                    ("Producto con precio abierto", "Debe ingresar monto correcto.", "Usar segun politica de caja."),
                ],
                [1.75, 2.65, 2.05],
            ),
            callout(
                "Pan por monto",
                "Si el pan se vende por monto y no se cuentan unidades, la regla operativa es disponibilidad: vender mientras haya pan y marcar agotado cuando ya no quede.",
                WARN,
            ),
            PageBreak(),
            h2("5.3 Cerrar, cancelar y revisar"),
            table(
                ["Accion", "Cuando usar", "Resultado"],
                [
                    ("Cerrar orden", "Cliente paga.", "Registra venta, pago, propina y consumo de stock si aplica."),
                    ("Cancelar orden", "La venta no se realizara.", "Cancela la orden y tickets asociados si corresponde."),
                    ("Anular item", "Un producto se retiro antes de cierre.", "Quita el item sin cerrar toda la orden."),
                    ("Revisar orden", "Hay duda de cobro o productos.", "Ver detalle, estado, canal, pago y total."),
                ],
                [1.5, 2.55, 2.4],
            ),
            example(
                "Ejemplo: venta de cheesecake",
                [
                    ("Producto", "Cheesecake Frambuesa", "Producto contado."),
                    ("Stock inicial", "12 unidades", "Viene de produccion completada."),
                    ("Venta", "2 unidades", "Al cerrar, stock baja a 10."),
                    ("Reporte", "Venta queda con costo historico", "Permite margen correcto."),
                ],
            ),
            example(
                "Ejemplo: venta de cafe preparado",
                [
                    ("Producto", "Capuchino simple", "Producto POS."),
                    ("Receta directa", "Cafe molido + leche", "Consume insumos al cerrar."),
                    ("Stock requerido", "Cafe y leche disponibles", "Si falta insumo, corregir antes."),
                    ("Cierre", "Venta cerrada", "Registra consumo e ingreso."),
                ],
            ),
            PageBreak(),
            h1("6. Flujo completo con ejemplos"),
            h2("6.1 Flujo pan amasado por disponibilidad"),
            *steps(
                [
                    ("1", "Ingresar materia prima.", "Harina, sal, levadura y otros insumos tienen stock."),
                    ("2", "Configurar producto Pan amasado.", "Producto de venta con modo disponibilidad."),
                    ("3", "Crear receta Pan amasado.", "Insumos + rendimiento teorico."),
                    ("4", "Activar version.", "La receta queda operativa."),
                    ("5", "Planificar produccion.", "Ver faltantes antes de producir."),
                    ("6", "Completar produccion.", "Producto queda disponible para venta."),
                    ("7", "Vender en POS.", "El cajero vende por monto mientras haya pan."),
                    ("8", "Marcar agotado.", "Cuando no queda pan, se bloquean ventas futuras."),
                ]
            ),
            h2("6.2 Flujo cheesecake con stock vendible"),
            *steps(
                [
                    ("1", "Ingresar insumos.", "Queso crema, galleta, mantequilla, fruta."),
                    ("2", "Configurar producto de venta.", "Cheesecake con stock vendible."),
                    ("3", "Crear receta y rendimiento.", "Ej.: 12 porciones."),
                    ("4", "Completar produccion.", "Stock vendible aumenta en 12."),
                    ("5", "Vender porciones.", "Cada cierre descuenta unidades."),
                    ("6", "Revisar stock.", "Si queda bajo, producir nuevamente."),
                ]
            ),
            PageBreak(),
            h1("7. Errores comunes y solucion"),
            table(
                ["Problema", "Causa probable", "Como resolver"],
                [
                    ("No aparece receta en produccion", "No tiene version activa o producto asociado.", "Abrir receta, completar version, asociar producto y activar."),
                    ("No deja activar receta", "Faltan insumos, cantidades o rendimiento.", "Revisar version en borrador y completar datos."),
                    ("No deja vender producto", "Sin stock, agotado, inactivo o sin receta activa.", "Revisar producto, stock/disponibilidad y sucursal."),
                    ("Produccion no consume stock", "La orden solo fue creada, no completada.", "Completar produccion y revisar movimientos."),
                    ("Stock no coincide", "Sucursal, ubicacion o ajuste mal registrado.", "Revisar movimientos antes de corregir."),
                    ("Costo de receta parece raro", "Costo promedio del insumo esta incorrecto.", "Revisar ultimos ingresos y costos totales."),
                ],
                [1.75, 2.35, 2.35],
                keep=False,
            ),
            h1("8. Checklist de capacitacion"),
            table(
                ["El usuario sabe...", "Como comprobarlo"],
                [
                    ("Diferenciar materia prima y producto de venta", "Puede explicar harina vs pan amasado."),
                    ("Registrar ingreso de stock", "Crea un ingreso con cantidad, unidad, costo y sucursal."),
                    ("Crear o revisar receta", "Identifica insumos, rendimiento y version activa."),
                    ("Planificar produccion", "Calcula requerimientos y entiende faltantes."),
                    ("Completar produccion", "Reconoce que ahi se consume inventario."),
                    ("Vender en POS", "Agrega productos, cierra venta y entiende impacto en stock."),
                    ("Marcar agotado", "Sabe bloquear productos por disponibilidad."),
                    ("Buscar errores", "Revisa movimientos, sucursal, receta y producto."),
                ],
                [2.95, 3.5],
                keep=False,
            ),
            callout(
                "Cierre",
                "El sistema funciona bien cuando cada accion se registra en su modulo correcto: compras en inventario, formulas en recetas, transformacion en produccion y cobros en POS.",
                GREEN,
            ),
        ]
    )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
