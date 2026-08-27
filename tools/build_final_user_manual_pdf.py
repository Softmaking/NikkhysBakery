from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "manuales"
SCREEN_DIR = OUT_DIR / "capturas-manual-final"
PDF_PATH = OUT_DIR / "manual-final-operativo-usuario-nikkhysbakery.pdf"
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
    base.add(ParagraphStyle("CoverTitle", parent=base["Title"], fontName="Helvetica-Bold", fontSize=23, leading=27, textColor=BRAND, alignment=TA_CENTER, spaceAfter=4))
    base.add(ParagraphStyle("CoverSubtitle", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, textColor=BRAND_DARK, alignment=TA_CENTER, spaceAfter=8))
    base.add(ParagraphStyle("CoverMeta", parent=base["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=10))
    base.add(ParagraphStyle("H1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=BRAND, spaceBefore=8, spaceAfter=6))
    base.add(ParagraphStyle("H2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=11.3, leading=14, textColor=BRAND, spaceBefore=6, spaceAfter=4))
    base.add(ParagraphStyle("Body", parent=base["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.1, textColor=BRAND_DARK, spaceAfter=5))
    base.add(ParagraphStyle("Small", parent=base["BodyText"], fontName="Helvetica", fontSize=8.05, leading=10.4, textColor=BRAND_DARK))
    base.add(ParagraphStyle("SmallBold", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.05, leading=10.4, textColor=BRAND_DARK))
    base.add(ParagraphStyle("TableHead", parent=base["BodyText"], fontName="Helvetica-Bold", fontSize=8.05, leading=10, textColor=BRAND))
    return base


S = make_styles()


def p(text, style="Body"):
    return Paragraph(text, S[style])


def h1(text):
    return Paragraph(text, S["H1"])


def h2(text):
    return Paragraph(text, S["H2"])


def callout(title, body, fill=LIGHT):
    data = [[p(f"<b>{title}</b>", "Small")], [p(body, "Small")]]
    t = Table(data, colWidths=[6.45 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fill),
        ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([t, Spacer(1, 6)])


def table(headers, rows, widths, keep=True):
    data = [[p(head, "TableHead") for head in headers]]
    for row in rows:
        data.append([p(str(cell), "Small") for cell in row])
    t = Table(data, colWidths=[w * inch for w in widths], hAlign="LEFT", repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER),
        ("BACKGROUND", (0, 1), (-1, -1), LIGHT_2),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return KeepTogether([t, Spacer(1, 7)]) if keep else t


def steps(rows):
    return [table(["Paso", "Qué hacer", "Resultado esperado"], rows, [0.7, 3.15, 2.6], keep=False), Spacer(1, 7)]


def shot(name, max_width=6.45 * inch, max_height=3.9 * inch):
    path = SCREEN_DIR / f"{name}.png"
    with PILImage.open(path) as img:
        width, height = img.size
    scale = min(max_width / width, max_height / height)
    image = Image(str(path), width=width * scale, height=height * scale)
    image.hAlign = "CENTER"
    return image


def screenshot_page(story, title, image_name, intro, zones, actions, note=None, fill=LIGHT):
    story.extend([h1(title), p(intro), shot(image_name), Spacer(1, 7)])
    story.append(table(["Zona visible", "Para qué sirve", "Qué debe revisar el usuario"], zones, [1.55, 2.45, 2.45]))
    story.extend(steps(actions))
    if note:
        story.append(callout("Importante", note, fill))
    story.append(PageBreak())


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(0.85 * inch, 0.55 * inch, 7.65 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 7.8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(4.25 * inch, 0.35 * inch, f"Manual operativo NikkhysBakery · Página {doc.page}")
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
        title="Manual operativo final de usuario NikkhysBakery",
        author="NikkhysBakery",
    )

    story = []
    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=0.55 * inch, height=0.68 * inch)
        logo.hAlign = "CENTER"
        story.extend([logo, Spacer(1, 8)])

    story.extend([
        p("NikkhysBakery", "CoverTitle"),
        p("Manual operativo para usuario final", "CoverSubtitle"),
        p("Guía con capturas reales para usar stock, recetas, producción y ventas", "CoverMeta"),
        callout(
            "Cómo leer este manual",
            "Este documento está pensado para una persona que usará el sistema sin asistencia. Cada módulo incluye: dónde entrar, qué mirar, qué completar, qué resultado esperar y qué hacer si aparece un problema.",
            LIGHT,
        ),
        table(["Módulo", "Qué aprenderás", "Ejemplo real usado"], [
            ("Inventario", "Revisar stock, registrar ingresos, ajustes, mermas y buscar movimientos.", "Aceite de oliva, Agua, Azúcar, Stock general."),
            ("Recetas", "Crear o revisar fichas técnicas, versiones activas y producto asociado.", "Pan amasado, Focaccia, Trampa falso."),
            ("Producción", "Planificar, calcular requerimientos, crear y completar órdenes.", "Órdenes terminadas y alerta de Pan amasado."),
            ("Ventas / POS", "Armar una orden, elegir canal, agregar productos y cerrar venta.", "Americano, Capuchino, Chocolate caliente."),
            ("Reportes", "Consultar stock, movimientos y resumen de producción.", "Reportes de inventario y producción."),
        ], [1.2, 3.2, 2.05]),
        callout("Regla general", "No mezcles módulos: las compras se registran en Inventario, las fórmulas en Recetas, la transformación en Producción y el cobro en POS.", GREEN),
        PageBreak(),
    ])

    story.extend([
        h1("1. Conceptos mínimos antes de operar"),
        p("Antes de tocar una pantalla, el usuario debe entender cuatro conceptos. Si esto queda claro, el flujo completo se vuelve mucho más simple."),
        table(["Concepto", "Significado", "Ejemplo en NikkhysBakery"], [
            ("Materia prima", "Insumo que se compra y se consume.", "Agua, Azúcar, Aceite de oliva."),
            ("Producto de venta", "Producto que aparece en POS para vender al cliente.", "Americano simple, Capuchino, Pan amasado."),
            ("Receta", "Ficha técnica que dice qué insumos consume y cuánto rinde.", "Pan amasado con versión vigente."),
            ("Producción", "Proceso que consume materia prima y deja stock o disponibilidad.", "Completar una orden de producción."),
            ("Venta", "Orden POS cerrada con productos y pago.", "Mesa con Americano y Capuchino."),
        ], [1.35, 2.9, 2.2]),
        h2("Orden recomendado de trabajo"),
        *steps([
            ("1", "Revisar stock de materias primas.", "Sabes si puedes producir o vender."),
            ("2", "Revisar receta activa.", "Sabes qué insumos se consumirán."),
            ("3", "Planificar y completar producción.", "El sistema habilita stock o disponibilidad."),
            ("4", "Vender en POS.", "El sistema registra la venta y descuenta stock cuando corresponde."),
            ("5", "Revisar reportes.", "Puedes detectar errores o diferencias."),
        ]),
        callout("Sucursal", "Cuando la pantalla muestre Casa Matriz o Global, confirma el alcance antes de operar. Las ventas y movimientos deben quedar en la sucursal correcta.", WARN),
        PageBreak(),
    ])

    screenshot_page(
        story,
        "2. Entrar y ubicarse en el sistema",
        "02-dashboard-menu",
        "Después de iniciar sesión se ve el panel administrativo. El usuario debe usar el menú lateral para entrar al módulo de trabajo.",
        [
            ("Menú lateral", "Permite cambiar entre módulos.", "Usar inventario, recetas, producción, POS y reportes."),
            ("Buscador superior", "Ayuda a encontrar información en pantallas grandes.", "Campo Buscar en la parte superior."),
            ("Usuario activo", "Muestra quién está operando.", "Capacitacion con rol ADMIN en la captura."),
        ],
        [
            ("1", "Mirar el menú lateral.", "Identificas el módulo al que debes entrar."),
            ("2", "Entrar al módulo según la tarea.", "Inventario para stock, Recetas para fórmulas, POS para ventas."),
            ("3", "Confirmar usuario y sucursal cuando aplique.", "Evitas registrar datos en un contexto incorrecto."),
        ],
        "Si no ves un módulo, probablemente tu usuario no tiene permisos para usarlo. Debes pedir acceso al administrador.",
        WARN,
    )

    screenshot_page(
        story,
        "3. Revisar stock actual",
        "03-inventario-stock",
        "La pestaña Stock muestra existencias reales por ubicación. Es la primera pantalla que se revisa antes de producir o investigar diferencias.",
        [
            ("Alcance", "Define si miras Casa Matriz o Global.", "Casa Matriz está seleccionada."),
            ("Filtros", "Permiten buscar por ubicación, tipo, bajo mínimo o negativo.", "Ubicación Todas y Tipo Todos."),
            ("Lista de stock", "Muestra item, ubicación, cantidad, valor y estado.", "Aceite de oliva, Agua, Azúcar y Azúcar flor."),
        ],
        [
            ("1", "Entrar a Inventario y dejar seleccionada la pestaña Stock.", "Ves el stock actual."),
            ("2", "Filtrar por ubicación o tipo si hay muchos items.", "Encuentras más rápido el insumo."),
            ("3", "Revisar cantidad y estado.", "Detectas si hay suficiente stock, bajo mínimo o negativo."),
            ("4", "Si algo no coincide, no ajustes todavía.", "Primero revisa movimientos o Kardex."),
        ],
        "El stock muestra una foto actual. Para saber por qué cambió una cantidad, usa Movimientos o Kardex.",
        LIGHT,
    )

    screenshot_page(
        story,
        "4. Registrar compra o ingreso",
        "04-inventario-ingresos",
        "Usa Ingresos cuando llegó una compra o reposición de materia prima. En la pantalla se ve Aceite de oliva como ejemplo real.",
        [
            ("Insumo", "Item que entra al inventario.", "Aceite de oliva."),
            ("Ubicación", "Dónde queda guardado el stock.", "Stock general."),
            ("Cantidad y unidad", "Cuánto entró y en qué unidad.", "1 Litro (l) en la captura."),
            ("Costo total", "Costo de la compra completa.", "El sistema lo usa para costo promedio."),
        ],
        [
            ("1", "Seleccionar pestaña Ingresos.", "Aparece Registrar compra o ingreso."),
            ("2", "Elegir ubicación e insumo.", "Ej.: Stock general y Aceite de oliva."),
            ("3", "Ingresar cantidad, unidad y costo total.", "El sistema puede calcular costo unitario."),
            ("4", "Completar proveedor/documento si corresponde.", "Queda trazabilidad de la compra."),
            ("5", "Presionar Registrar ingreso.", "Aumenta el stock del item."),
        ],
        "Verifica unidad antes de guardar. Un error entre ml, litro, gramo o kilo puede alterar stock y costos.",
        RED,
    )

    screenshot_page(
        story,
        "5. Ajustes de inventario",
        "05-inventario-ajustes",
        "Usa Ajustes cuando el conteo físico no coincide con el sistema. No reemplaza compras, ventas ni producción.",
        [
            ("Tipo de ajuste", "Indica si sube o baja stock.", "Ajuste positivo o negativo según pantalla."),
            ("Item y ubicación", "Define qué stock se corrige.", "Debe corresponder a la sucursal activa."),
            ("Motivo", "Explica por qué se corrige.", "Conteo físico, diferencia detectada, error anterior."),
        ],
        [
            ("1", "Contar físicamente antes de ajustar.", "Tienes un número real."),
            ("2", "Elegir item, ubicación y cantidad.", "Solo corriges el stock afectado."),
            ("3", "Escribir motivo claro.", "Cualquier supervisor puede entender el ajuste."),
            ("4", "Guardar ajuste.", "El stock cambia y queda movimiento registrado."),
        ],
        "No uses ajustes para registrar ventas o producción. Si se vendió, debe pasar por POS. Si se produjo, debe pasar por Producción.",
        WARN,
    )

    screenshot_page(
        story,
        "6. Registrar mermas",
        "06-inventario-mermas",
        "Usa Mermas cuando se perdió, venció, dañó o descartó materia prima o producto controlado.",
        [
            ("Item", "Qué se perdió o descartó.", "Puede ser materia prima o producto controlado."),
            ("Cantidad", "Cuánto se descuenta.", "Debe coincidir con lo realmente perdido."),
            ("Motivo", "Explica la pérdida.", "Vencimiento, daño, mala preparación, descarte."),
        ],
        [
            ("1", "Entrar a pestaña Mermas.", "Aparece formulario de registro."),
            ("2", "Elegir item y ubicación.", "Seleccionas el stock afectado."),
            ("3", "Ingresar cantidad y motivo.", "Queda explicación de la pérdida."),
            ("4", "Guardar merma.", "El stock baja y queda trazabilidad."),
        ],
        "Registrar mermas ayuda a entender pérdidas reales. Si no se registran, los reportes parecerán incorrectos.",
        LIGHT,
    )

    screenshot_page(
        story,
        "7. Revisar Kardex o movimientos",
        "07-inventario-kardex",
        "Kardex y movimientos ayudan a responder la pregunta: ¿por qué cambió este stock?",
        [
            ("Filtros", "Permiten buscar por item, ubicación o fechas.", "Útiles cuando hay muchos movimientos."),
            ("Historial", "Muestra ingresos, ajustes, mermas, producción y consumo.", "Ayuda a auditar stock."),
            ("Resultado", "Permite detectar errores antes de corregir.", "Evita duplicar ajustes."),
        ],
        [
            ("1", "Entrar a Kardex o Movimientos.", "Ves el historial."),
            ("2", "Filtrar por item y fecha.", "Encuentras el movimiento relevante."),
            ("3", "Revisar origen del cambio.", "Sabes si fue ingreso, merma, producción o venta."),
            ("4", "Solo si corresponde, hacer ajuste.", "Corriges con respaldo."),
        ],
        "Antes de tocar stock, revisa historial. Es la diferencia entre corregir bien y tapar un error.",
        GREEN,
    )

    screenshot_page(
        story,
        "8. Reposición sugerida",
        "08-inventario-reposicion",
        "Reposición ayuda a ver qué insumos necesitan compra o reposición según mínimos e ideales configurados.",
        [
            ("Listado", "Muestra sugerencias de reposición.", "Depende del stock actual y mínimos."),
            ("Stock mínimo", "Umbral bajo que requiere atención.", "Si está bajo, conviene comprar."),
            ("Stock ideal", "Cantidad objetivo para operar cómodo.", "Sirve para planificación."),
        ],
        [
            ("1", "Entrar a Reposición.", "Ves sugerencias disponibles."),
            ("2", "Revisar items bajo mínimo.", "Priorizas compra."),
            ("3", "Confirmar con stock físico si hay dudas.", "Evitas compras duplicadas."),
            ("4", "Registrar ingreso cuando llegue compra.", "Actualizas stock real."),
        ],
        "La reposición sugiere, pero no compra sola. El usuario debe confirmar operación real.",
        LIGHT,
    )

    screenshot_page(
        story,
        "9. Crear o revisar recetas",
        "09-recetas-listado-crear",
        "Recetas permite crear fichas técnicas y revisar cuáles están activas. En la captura aparecen recetas reales como Focaccia, Pan amasado y Trampa falso.",
        [
            ("Crear receta", "Formulario para nueva ficha técnica.", "Nombre, tipo, producto que genera y estado activa."),
            ("Producto asociado", "Producto POS que quedará con stock o disponible.", "No es materia prima."),
            ("Listado recetas", "Recetas existentes y estado.", "Pan amasado aparece activa con costo vigente."),
        ],
        [
            ("1", "Entrar a Recetas.", "Ves formulario y listado."),
            ("2", "Completar nombre y tipo si crearás una nueva receta.", "Ej.: Pan amasado, Producción."),
            ("3", "Seleccionar producto de venta que genera.", "Debe existir como producto POS."),
            ("4", "Guardar receta.", "Luego podrás crear versión e insumos."),
            ("5", "Abrir receta existente para revisar.", "Compruebas si está activa y con costo."),
        ],
        "Una receta de producción debe apuntar a un producto de venta o disponibilidad. Si no, puede no aparecer correctamente en Producción.",
        WARN,
    )

    screenshot_page(
        story,
        "10. Revisar receta Pan amasado",
        "10-recetas-pan-amasado",
        "Pan amasado aparece como receta real activa. Es un buen ejemplo para explicar la diferencia entre receta, producto de venta y producción.",
        [
            ("Receta activa", "Indica que puede operar.", "Pan amasado aparece Activa."),
            ("Costo vigente", "Costo calculado desde insumos.", "$147.062 y $4.902/unit en la captura."),
            ("Producto asociado", "Debe ser producto POS.", "La alerta en producción ayuda a detectar si falta configuración."),
        ],
        [
            ("1", "Buscar Pan amasado en la lista.", "Ubicas la receta real."),
            ("2", "Revisar si está activa.", "Si no está activa, no debe usarse para producción."),
            ("3", "Validar producto asociado.", "Debe estar configurado para venta o disponibilidad."),
            ("4", "Revisar costo vigente.", "Sirve para entender margen y producción."),
        ],
        "Si el pan se vende por monto y no por unidad, lo recomendado es trabajar con disponibilidad: disponible mientras hay pan y agotado cuando se acaba.",
        GREEN,
    )

    screenshot_page(
        story,
        "11. Producción: vista general",
        "11-produccion-general",
        "Producción muestra métricas, alertas, creación de órdenes, planificación y órdenes existentes.",
        [
            ("Alerta roja", "Indica recetas activas incompletas para producción.", "Pan amasado aparece en alerta."),
            ("Crear orden", "Crea producción desde una receta activa.", "Selecciona receta, ubicación y cantidad."),
            ("Planificar producción", "Calcula requerimientos antes de crear o completar.", "Botón Calcular requerimientos."),
            ("Órdenes", "Lista órdenes históricas o actuales.", "Trampa falso terminada."),
        ],
        [
            ("1", "Leer alertas antes de producir.", "Sabes si hay recetas con configuración pendiente."),
            ("2", "Planificar producción.", "Ves faltantes y requerimientos."),
            ("3", "Crear orden solo si corresponde.", "Queda orden registrada."),
            ("4", "Completar cuando realmente se produjo.", "Ahí se consume inventario y se habilita producto."),
        ],
        "Crear orden no consume stock. El consumo ocurre al completar producción.",
        RED,
    )

    screenshot_page(
        story,
        "12. Planificar producción",
        "12-produccion-planificar",
        "La planificación permite validar si tienes insumos suficientes antes de comprometer producción.",
        [
            ("Receta activa", "Receta que se evaluará.", "Selector de receta."),
            ("Ubicación", "Desde dónde se consumirán insumos.", "Stock general."),
            ("Cantidad a producir", "Cantidad planificada.", "1 en la captura."),
            ("Calcular requerimientos", "Muestra insumos requeridos, disponibles y faltantes.", "Debe usarse antes de producir."),
        ],
        [
            ("1", "Elegir receta activa.", "El sistema sabe qué insumos usar."),
            ("2", "Elegir ubicación.", "Se evalúa stock del lugar correcto."),
            ("3", "Ingresar cantidad a producir.", "Define cuánto se necesita."),
            ("4", "Presionar Calcular requerimientos.", "Ves si puedes producir o falta inventario."),
            ("5", "Corregir faltantes antes de crear orden.", "Evitas errores al completar."),
        ],
        "Si hay faltantes, primero registra ingreso de stock o baja la cantidad a producir.",
        WARN,
    )

    screenshot_page(
        story,
        "13. Ordenes / POS: pantalla de venta",
        "13-pos-general",
        "POS es la pantalla del cajero. Permite elegir canal, buscar productos, agregar items y cerrar venta.",
        [
            ("Canal", "Define Mesa, Retiro o Despacho.", "Mesa está seleccionado."),
            ("Referencia", "Identifica mesa o pedido.", "Campo Mesa."),
            ("Categorías", "Filtran productos.", "Cafetería, Panadería, Pastelería."),
            ("Productos", "Items vendibles con precio.", "Americano doble, Capuchino simple, Chocolate caliente."),
        ],
        [
            ("1", "Elegir canal de atención.", "Mesa, Retiro o Despacho."),
            ("2", "Ingresar referencia si corresponde.", "Número de mesa o nombre del pedido."),
            ("3", "Seleccionar categoría.", "Encuentras productos más rápido."),
            ("4", "Agregar productos a la orden.", "La orden se arma en Caja/POS."),
            ("5", "Cerrar venta cuando el cliente pague.", "Queda venta registrada."),
        ],
        "Si un producto no se puede agregar, revisa si está activo y si tiene stock o disponibilidad en la sucursal.",
        GREEN,
    )

    screenshot_page(
        story,
        "14. Ejemplo de venta con productos reales",
        "14-pos-producto-agregado",
        "En el POS se ven productos reales de cafetería y sus precios. Úsalo como referencia para entrenar al cajero.",
        [
            ("Cafetería", "Categoría activa para bebidas.", "Americano, Capuchino, Chocolate caliente."),
            ("Precio", "Valor de venta visible.", "Americano simple $2.500, Capuchino simple $2.700."),
            ("Orden", "Zona donde se arma el pedido.", "Si está vacía, aún no hay items agregados."),
        ],
        [
            ("1", "Elegir producto desde la lista.", "Ej.: Americano simple."),
            ("2", "Verificar que aparezca en la orden.", "El pedido queda armado."),
            ("3", "Agregar otros productos si corresponde.", "Ej.: Capuchino simple."),
            ("4", "Revisar total antes de cobrar.", "Evitas errores de caja."),
            ("5", "Cerrar venta.", "El sistema registra venta y consumo si aplica."),
        ],
        "Para productos con receta directa, el consumo de insumos ocurre al cerrar la venta.",
        LIGHT,
    )

    screenshot_page(
        story,
        "15. Reporte de stock",
        "15-reporte-stock",
        "El reporte de stock sirve para consultar existencias sin modificar datos. Es ideal para supervisar.",
        [
            ("Filtros", "Permiten acotar por sucursal, ubicación o item.", "Usar cuando hay muchos registros."),
            ("Resultados", "Muestran stock y estado.", "Ayuda a detectar bajo mínimo o negativo."),
            ("Uso", "Solo consulta, no modifica.", "Para corregir, volver a inventario."),
        ],
        [
            ("1", "Entrar a Reporte de stock.", "Ves existencias."),
            ("2", "Aplicar filtros si es necesario.", "Encuentras el item."),
            ("3", "Comparar con conteo físico si hay dudas.", "Validas diferencia."),
            ("4", "Ir a movimientos antes de ajustar.", "Entiendes origen del problema."),
        ],
        "No corrijas desde memoria. Primero revisa reportes y movimientos.",
        GREEN,
    )

    screenshot_page(
        story,
        "16. Reporte de movimientos",
        "16-reporte-movimientos",
        "Movimientos muestra el historial de entradas y salidas de inventario. Es la herramienta principal para investigar diferencias.",
        [
            ("Filtros", "Permiten buscar por fecha, item o tipo.", "Útil para auditoría."),
            ("Tipo de movimiento", "Indica ingreso, ajuste, merma, consumo o producción.", "Ayuda a explicar stock."),
            ("Fechas", "Permiten revisar periodo específico.", "Día de operación o cierre."),
        ],
        [
            ("1", "Seleccionar rango de fechas.", "Acotas la investigación."),
            ("2", "Filtrar por item si sabes cuál falló.", "Ves solo movimientos relevantes."),
            ("3", "Revisar tipo y cantidad.", "Encuentras el origen del cambio."),
            ("4", "Documentar si se requiere ajuste.", "La corrección queda justificada."),
        ],
        "Este reporte evita ajustes innecesarios. Úsalo antes de modificar stock.",
        LIGHT,
    )

    screenshot_page(
        story,
        "17. Resumen de producción",
        "17-reporte-produccion",
        "El resumen de producción permite revisar órdenes completadas, estados y costos. Sirve para supervisión diaria.",
        [
            ("Filtros", "Permiten buscar por fecha, estado o receta.", "Ayuda a revisar un turno o día."),
            ("Órdenes", "Muestran producción creada, completada o cancelada.", "Sirve para seguimiento."),
            ("Costo", "Ayuda a entender impacto de producción.", "Usar junto con recetas y stock."),
        ],
        [
            ("1", "Entrar al reporte de producción.", "Ves resumen histórico."),
            ("2", "Filtrar por fecha o estado.", "Revisas producción del día."),
            ("3", "Comparar con stock y ventas.", "Detectas inconsistencias."),
            ("4", "Si falta producción, revisar módulo Producción.", "Ves si quedó pendiente o no completada."),
        ],
        "Una producción creada pero no completada no debe considerarse stock disponible.",
        WARN,
    )

    story.extend([
        h1("18. Flujos guiados con ejemplos reales"),
        h2("Flujo A: compra de materia prima"),
        *steps([
            ("1", "Entrar a Inventario > Ingresos.", "Se abre formulario de compra."),
            ("2", "Elegir Stock general y Aceite de oliva.", "Usas item real visible en pantalla."),
            ("3", "Ingresar cantidad, unidad y costo total.", "El sistema actualiza stock y costo promedio."),
            ("4", "Revisar Stock actual.", "Aceite de oliva aumenta en la ubicación correcta."),
        ]),
        h2("Flujo B: revisar si Pan amasado puede producirse"),
        *steps([
            ("1", "Entrar a Recetas y buscar Pan amasado.", "Confirmas que la receta está activa."),
            ("2", "Revisar producto asociado.", "Debe ser producto POS o disponibilidad."),
            ("3", "Entrar a Producción.", "Leer alerta superior si aparece."),
            ("4", "Si aparece en alerta, corregir receta/producto antes de producir.", "Evitas órdenes fallidas."),
        ]),
        h2("Flujo C: venta de cafetería"),
        *steps([
            ("1", "Entrar a Órdenes / POS.", "Se abre caja."),
            ("2", "Elegir Mesa, Retiro o Despacho.", "Define el canal."),
            ("3", "Seleccionar Cafetería.", "Ves Americano, Capuchino y Chocolate caliente."),
            ("4", "Agregar productos y revisar total.", "La orden queda lista para pago."),
            ("5", "Cerrar venta.", "La venta queda registrada y descuenta stock si corresponde."),
        ]),
        PageBreak(),
        h1("19. Qué hacer si algo falla"),
        table(["Problema", "Qué revisar primero", "Acción recomendada"], [
            ("No veo un módulo", "Permisos del usuario.", "Pedir acceso al administrador."),
            ("No encuentro un insumo", "Inventario > Catálogo.", "Crear o activar item si corresponde."),
            ("Stock no coincide", "Kardex o reporte de movimientos.", "Investigar antes de ajustar."),
            ("No aparece receta en producción", "Versión activa y producto asociado.", "Corregir receta/producto."),
            ("No deja producir", "Stock suficiente, receta activa, sucursal.", "Planificar y corregir faltantes."),
            ("No deja vender", "Producto activo, stock o disponibilidad.", "Producir, marcar disponible o revisar configuración."),
            ("Venta cerrada con error", "Detalle de orden y reportes.", "Consultar con supervisor antes de ajustar stock."),
        ], [1.7, 2.3, 2.45], keep=False),
        callout("Regla de cierre", "Si no sabes qué pasó, no corrijas directo. Primero revisa reportes, movimientos y estado de receta/producción. El sistema está pensado para dejar trazabilidad.", RED),
        h1("20. Checklist diario para el usuario"),
        table(["Momento", "Checklist"], [
            ("Inicio del día", "Confirmar sucursal, revisar stock bajo, revisar productos agotados y producciones pendientes."),
            ("Antes de producir", "Validar receta activa, calcular requerimientos y revisar faltantes."),
            ("Durante ventas", "Usar POS, revisar productos disponibles y marcar agotado cuando corresponda."),
            ("Después de producir", "Completar la orden y revisar que el stock/disponibilidad cambió."),
            ("Cierre", "Revisar ventas, movimientos, producción y diferencias de stock."),
        ], [1.45, 5.0]),
        callout("Mensaje final para capacitación", "El usuario no necesita memorizar todo. Debe recordar el flujo: Stock -> Recetas -> Producción -> POS -> Reportes. Si sigue ese orden, la operación queda clara y trazable.", GREEN),
    ])

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
