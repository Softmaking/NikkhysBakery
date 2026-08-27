# Flujos End-to-End

## Login y Sesion

1. Usuario entra a `/admin/login`.
2. Frontend envia credenciales a `POST /auth/login`.
3. Backend devuelve access token y setea refresh token en cookie `HttpOnly`.
4. Frontend obtiene usuario actual con `GET /auth/me`.
5. Se cargan roles, permisos y sucursales.
6. El panel muestra rutas segun permisos disponibles.

## POS y Cierre de Orden

1. Cajero crea la venta con `POST /orders/pos`, que registra orden, items y envio a KDS dentro de una transaccion.
2. Puede agregar items con `POST /orders/:id/items`.
3. Puede editar item con `PATCH /orders/:id/items/:itemId`.
4. Puede anular item con `PATCH /orders/:id/items/:itemId/void`.
5. Cierra orden con `PATCH /orders/:id/close`.
6. Backend calcula totales, propina, snapshots y consumo de inventario.

## KDS

1. Producto se asigna a estaciones con endpoints de estaciones/productos.
2. Orden enviada genera tickets e items para cocina.
3. Cocina consulta tickets por estacion con `GET /kds/stations/:stationId/tickets`.
4. Cocina actualiza ticket con `PATCH /tickets/:id/status`.
5. Cocina actualiza item con `PATCH /ticket-items/:id/status`.

## Inventario

1. Usuario crea ubicaciones e items.
2. Registra ingresos con `POST /inventory/receipts` usando costos netos, sin IVA.
3. Registra ajustes con `POST /inventory/adjustments`.
4. Registra mermas con `POST /inventory/waste`.
5. Backend mantiene stock, promedio ponderado, movimientos y lotes con costo neto;
   el IVA de compras queda fuera del flujo operativo actual.
6. Frontend consulta stock, movimientos, lotes, alertas y sugerencias.

## Recetas, Costeo y Produccion

1. Usuario crea receta y versiones.
2. Activa version operacional.
3. Consulta costo vigente basado en promedio de inventario.
4. Crea orden de produccion.
5. Confirma y completa produccion.
6. Backend consume insumos y recibe producto terminado.
7. Si aplica, registra lote de salida y vencimiento.

## Reporteria

1. Frontend consulta reportes por dominio.
2. Backend filtra por sucursal activa.
3. Reportes historicos usan snapshots.
4. Reportes operativos pueden usar estado vigente de stock/costos.

## Usuarios, Roles y Permisos

1. Administrador consulta usuarios, roles y catalogo IAM.
2. Asigna roles a usuario.
3. Asigna permisos a roles.
4. Cambios de permisos deben reflejarse en la sesion efectiva del usuario.
