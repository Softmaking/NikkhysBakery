# Contratos Front-Back

Este archivo es la matriz viva de integracion. Si un endpoint cambia, actualizar
este documento junto con backend docs y frontend docs.

## Convenciones

- Backend base URL local: `http://localhost:3000`.
- No existe prefijo global `/v1` aplicado actualmente.
- Auth: `Authorization: Bearer <accessToken>`.
- Refresh: cookie `HttpOnly`; backend busca por digest indexado y valida con bcrypt.
- Sucursal: `x-branch-id` cuando el usuario opera multiples sucursales.
- Content type: `application/json`.

## Estado de Contratos

| Dominio | Frontend | Backend | Estado |
| --- | --- | --- | --- |
| Auth | `auth.service.ts`, `auth-refresh.service.ts` | `auth.controller.ts` | OK |
| Dashboard | `dashboard-api.service.ts` | `dashboard.controller.ts` | OK |
| Categorias admin | `categories-api.service.ts` | `product-categories.controller.ts` | OK |
| Categorias catalogo | lectura liviana | `catalog.controller.ts` | OK, documentar uso exacto por pantalla |
| Productos | `products-api.service.ts` | `products.controller.ts` | OK |
| Ordenes | `orders-api.service.ts` | `orders.controller.ts` | OK |
| KDS tickets | `kds-api.service.ts` | `kds.controller.ts` | OK |
| KDS configuracion | `kds-config-api.service.ts` | `kds-config.controller.ts` | OK |
| Inventario | `inventory-api.service.ts` | `inventory.controller.ts` | OK |
| Recetas | `recipes-api.service.ts` | `recipes.controller.ts` | OK |
| Costeo | `costing-api.service.ts` | `costing.controller.ts` | OK |
| Produccion | `production-api.service.ts` | `production.controller.ts` | OK |
| Reportes | `reports-api.service.ts` | `reports.controller.ts` | OK |
| IAM | `iam-api.service.ts`, `users-api.service.ts` | `iam.controller.ts`, `user.controller.ts`, `role.controller.ts` | OK |
| Horarios por sucursal | `business-hours-api.service.ts` | `business-hours.controller.ts` | Implementado |
| Permisos de reportes y KDS config | rutas/menu Angular | migraciones/backend | Resuelto: frontend usa permisos backend existentes |

## Endpoints Principales

### Auth

- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `GET /auth/me`

### Diagnostico

- `GET /`
- `GET /version`
- `GET /docs`

### Dashboard

- `GET /dashboard/summary`

### Sucursales, Usuarios e IAM

- `GET /branches`
- `POST /branches`
- `POST /branches/assign`
- `GET /branches/user/:userId`
- `GET /users`
- `GET /users/:id`
- `POST /users`
- `PATCH /users/:id`
- `DELETE /users/:id`
- `GET /roles`
- `GET /iam/catalog`
- `GET /iam/users/:userId/access`
- `POST /iam/users/:userId/roles`
- `POST /iam/roles/:roleCode/permissions`

### Horarios públicos y configuración

- `GET /public/branches` (público): devuelve sucursales activas, dirección y horarios.
- `GET /branches/:branchId/business-hours` (`BRANCHES_READ`).
- `PATCH /branches/:branchId/business-hours` (`BRANCHES_UPDATE`).

El payload de actualización contiene exactamente siete días (`dayOfWeek` de 0 a 6),
`isClosed` y horarios `HH:mm`. Los horarios abiertos requieren apertura menor que
cierre. La sucursal se selecciona automáticamente cuando solo existe una; con varias,
frontend muestra tabs Material.

### Catalogo y Productos

- `GET /categories`
- `POST /categories`
- `GET /product-categories`
- `POST /product-categories`
- `PATCH /product-categories/:id/active`
- `GET /products`
- `GET /products/:id`
- `POST /products`
- `PATCH /products/:id`
- `PATCH /products/:id/active`
- `GET /products/:id/price-history`
- `PUT /products/:id/categories`
- `PATCH /products/:id/categories/add`
- `PATCH /products/:id/categories/remove`
- `PATCH /products/:id/categories/toggle`

### Ordenes y KDS

- `POST /orders`
- `POST /orders/pos`
- `GET /orders`
- `GET /orders/:id`
- `POST /orders/:id/items`
- `PATCH /orders/:id/items/:itemId`
- `PATCH /orders/:id/items/:itemId/void`
- `POST /orders/:id/send`
- `PATCH /orders/:id/close`
- `PATCH /orders/:id/cancel`
- `GET /kds/stations/:stationId/tickets`
- `PATCH /tickets/:id/status`
- `PATCH /ticket-items/:id/status`
- `GET /stations`
- `POST /stations`
- `PATCH /stations/:id`
- `DELETE /stations/:id`
- `GET /products/:id/stations`
- `POST /products/:id/stations`
- `DELETE /products/:id/stations/:stationId`

### Inventario

- `GET /inventory/units`
- `GET /inventory/locations`
- `POST /inventory/locations`
- `GET /inventory/items`
- `GET /inventory/items/:id`
- `POST /inventory/items`
- `PATCH /inventory/items/:id`
- `POST /inventory/receipts`
- `POST /inventory/adjustments`
- `POST /inventory/waste`
- `GET /inventory/stocks`
- `GET /inventory/movements`
- `GET /inventory/lots`
- `GET /inventory/lots/alerts`
- `GET /inventory/reorder-suggestions`

Regla de alcance:

- Inventario opera estrictamente por sucursal mediante `x-branch-id`.
- Si el usuario tiene una sola sucursal activa, backend puede resolverla.
- Usuarios `ADMIN` pueden consultar inventario global cuando no envían `x-branch-id`.
- Frontend expone selector de alcance en inventario para alternar sucursal activa
  y vista global cuando el usuario tiene rol `ADMIN`.
- `GET /inventory/items/:id` incluye `configurationLocks` para informar cambios
  estructurales no permitidos. `PATCH /inventory/items/:id` valida estas mismas
  restricciones en backend.
- `POST /inventory/receipts` recibe `totalCost` o `unitCost` netos, sin IVA. El IVA de
  compras no forma parte del contrato actual ni del costo operativo.

### Recetas, Costeo y Produccion

- `GET /recipes`
- `GET /recipes/:id`
- `POST /recipes`
- `POST /recipes/:id/versions`
- `POST /recipes/:id/versions/:versionId/activate`
- `GET /recipes/:id/cost`
- `GET /costing/profiles`
- `POST /costing/profiles`
- `POST /costing/quotes`
- `GET /costing/quotes/:id`
- `POST /costing/quotes/analyze-price`
- `GET /production/orders`
- `GET /production/orders/:id`
- `POST /production/orders`
- `POST /production/orders/:id/confirm`
- `POST /production/orders/:id/complete`
- `POST /production/orders/:id/cancel`
- `POST /production/planning/requirements`

### Reportes

- `GET /reports/sales/summary`
- `GET /reports/orders`
- `GET /reports/orders/:id`
- `GET /reports/products`
- `GET /reports/tickets`
- `GET /reports/tickets/:id`
- `GET /reports/inventory/stock`
- `GET /reports/inventory/movements`
- `GET /reports/production/summary`
- `GET /reports/costing/product-margins`

## Decisiones de Contrato

### Permisos de reportes

Decision tomada: no crear permisos nuevos de reporteria por ahora. Frontend y
backend usan permisos de dominio:

- ventas/ordenes/productos/margenes: `ORDERS_READ`
- inventario: `INVENTORY_READ`
- produccion: `PRODUCTION_READ`
- tickets: `KDS_READ`

### Permisos KDS configuracion

Decision tomada: no crear permisos granulares nuevos por estaciones por ahora.
Frontend y backend usan:

- lectura KDS y estaciones: `KDS_READ`
- envio de ordenes a cocina: `KDS_SEND`
- cambios de estado/configuracion KDS: `KDS_UPDATE`

### Versionado `/v1`

`API_VERSION` existe en configuracion y README, pero las rutas reales actuales no
usan prefijo global `/v1`.

Decision tomada: mantener `API_VERSION` como version informativa hasta planificar
un cambio coordinado de URLs.

### POS transaccional

Decision tomada: el flujo principal de venta usa `POST /orders/pos` para crear
orden, agregar items y enviar a KDS dentro de una transaccion backend.

Esto reemplaza en frontend el flujo secuencial `POST /orders` + multiples
`POST /orders/:id/items` + `POST /orders/:id/send` para nuevas ventas POS.

El permiso requerido para este flujo es `ORDERS_CREATE`. El backend valida stock
vendible por sucursal al crear/actualizar items y consume `FINISHED_GOOD` desde
ubicaciones activas de la sucursal al cerrar la venta.

### Producción por sucursal

Decision tomada: producción opera estrictamente dentro de la sucursal activa.
El frontend debe enviar `x-branch-id` en `GET/POST /production/*` cuando el
usuario tenga más de una sucursal.

### Cancelacion de orden y KDS

Decision tomada: `PATCH /orders/:id/cancel` cancela la orden y sus tickets KDS
asociados en backend. El frontend no debe cancelar tickets manualmente.

### Acciones granulares en detalle de orden

Decision tomada: el frontend debe mostrar/habilitar acciones de detalle usando
los mismos permisos del backend:

- cerrar: `ORDERS_CLOSE`
- cancelar: `ORDERS_CANCEL`
- agregar item: `ORDERITEM_ADD`
- editar item: `ORDERITEM_UPDATE`
- anular item: `ORDERITEM_VOID`
