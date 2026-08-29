# Current Task

## Foco Actual

Consolidar la estructura spec-driven fullstack manteniendo los nombres actuales:

   - `NikkhysBakery-Front`
   - `NikkhysBakery-Back`

## En Curso

- Crear documentacion raiz de negocio, requerimientos, arquitectura, flujos y contratos.
- Alinear documentacion backend/frontend con los contratos reales observados.
- Registrar decisiones pendientes que requieren definicion del owner del producto/proyecto.

## Decisiones Tomadas

1. Permisos de reportes:
   - Se mantiene el modelo backend actual.
   - El frontend usa permisos de dominio existentes (`ORDERS_READ`, `INVENTORY_READ`, `PRODUCTION_READ`, `KDS_READ`).

2. Permisos KDS configuracion:
   - Se mantiene el modelo backend actual.
   - El frontend usa `KDS_READ`, `KDS_SEND` y `KDS_UPDATE`.

3. Versionado API:
   - Se mantienen rutas sin prefijo `/v1`.
   - `API_VERSION` queda como version informativa hasta un cambio coordinado.

4. Inventario por sucursal:
   - El inventario operativo queda estrictamente filtrado por sucursal.
   - Usuarios `ADMIN` pueden consultar inventario global sin `x-branch-id`.

5. Ordenes y KDS:
    - La venta POS usa endpoint transaccional backend.
    - Cancelar una orden cancela sus tickets KDS asociados en backend.

6. Dependencias frontend:
   - Frontend actualizado a Angular 22 y TypeScript 6.
   - `package-lock.json` se versiona para instalaciones reproducibles.

7. Dependencias backend:
   - Backend actualizado a la versión `0.4.2` con correcciones de seguridad compatibles.
   - NestJS, TypeORM, Swagger y dependencias transitivas quedan sin vulnerabilidades reportadas por npm.

8. Edición de catálogo inventariable:
   - El detalle del ítem muestra bloqueos estructurales resueltos por backend.
   - Los cambios que comprometen historial, lotes o dependencias activas se bloquean y requieren migración a un ítem nuevo.
   - El modal conserva los datos disponibles y bloquea el guardado si no puede cargar el detalle validado.
    - El diálogo se monta en el overlay global, queda sobre topbar/sidebar y muestra las últimas transacciones del ítem.

9. Costos de inventario:
   - Los ingresos, el promedio ponderado, recetas y producción usan costos netos, sin IVA.
   - El IVA de compras no se persiste ni calcula hasta definir un módulo tributario separado.

## Riesgos

- Documentacion y codigo pueden volver a divergir si no se actualizan juntos.
- La raiz no es repo git actualmente, por lo que estos archivos deben versionarse de forma explicita.
- Nuevos permisos agregados en frontend deben existir primero en backend/IAM.
- Queda warning de budget CSS en inventario; no bloquea build, pero conviene resolverlo antes de crecer mas la pantalla.
- El despliegue Docker requiere crear fuera del repositorio el archivo de secretos indicado en `infra/README.md`.

## Nueva funcionalidad implementada

- Los horarios se almacenan por sucursal en `branch_business_hours`.
- El sitio público consulta sucursales activas y muestra tabs Material cuando hay más de una.
- La sección “Encuéntranos” y el footer comparten la sucursal seleccionada.
- `/admin/settings` permite editar los siete días usando `BRANCHES_READ` y `BRANCHES_UPDATE`.
