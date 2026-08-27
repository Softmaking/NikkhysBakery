# Contexto de Negocio

## Proposito

NikkhysBakery es un sistema para administrar una pasteleria/cafeteria con
operacion de venta, cocina, inventario, produccion y reporteria.

El objetivo es reducir trabajo manual, mantener trazabilidad operativa y permitir
decisiones basadas en datos de ventas, costos, stock y produccion.

## Usuarios Principales

- Administrador: configura usuarios, permisos, productos, sucursales y reglas.
- Supervisor: opera y revisa ventas, inventario, cocina y reportes.
- Cajero: crea y cierra ordenes en POS.
- Cocina: gestiona tickets KDS y estados de preparacion.
- Operacion/produccion: administra insumos, recetas, costeo y produccion.

## Dominios del Negocio

- Publico: sitio de marca para NikkhysBakery.
- Autenticacion e IAM: usuarios, roles, permisos y sesiones.
- Sucursales: contexto operativo por branch.
- Catalogo: productos, categorias, precios y modos de inventario.
- POS: ordenes, items, precios abiertos, propinas, cierre y cancelacion.
- KDS: estaciones, tickets de cocina y estados.
- Inventario: insumos, unidades, ubicaciones, stock, movimientos y lotes.
- Recetas y costeo: versiones, costos vigentes, perfiles y cotizaciones.
- Produccion: ordenes, consumo de insumos y entrada de producto terminado.
- Reporteria: ventas, productos, tickets, stock, movimientos, produccion y margenes.

## Principios de Producto

- La informacion visible en UI debe venir de contratos backend claros.
- Los reportes historicos deben respetar snapshots y no recalcular ventas pasadas
  con costos nuevos.
- Las acciones criticas deben tener permisos explicitos.
- La sucursal activa debe estar resuelta antes de operar datos sensibles.
- El sistema debe favorecer trazabilidad sobre edicion silenciosa.

## Decisiones Tomadas

- Los permisos del frontend deben alinearse con permisos backend existentes.
  Reportes usan permisos de dominio como `ORDERS_READ`, `INVENTORY_READ`,
  `PRODUCTION_READ` y `KDS_READ`.
- KDS usa `KDS_READ`, `KDS_SEND` y `KDS_UPDATE`; no se agregan permisos
  granulares por estaciones por ahora.
- `API_VERSION` se mantiene como version informativa; las rutas reales no usan
  prefijo global `/v1`.
