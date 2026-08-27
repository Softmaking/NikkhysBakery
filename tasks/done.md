# Done Proyecto

## Documentacion

- Creada capa raiz spec-driven para coordinar frontend y backend.
- Registrado mapa de dominios, flujos end-to-end y contratos front-back.
- Detectadas decisiones pendientes de permisos y versionado.
- Resuelta decision conservadora de permisos: frontend alineado a permisos backend existentes.
- Resuelta decision de versionado: `/v1` queda informativo por ahora.
- Implementado alcance de inventario por sucursal con consulta global para `ADMIN`.
- Implementado endpoint POS transaccional para crear orden, items y KDS juntos.
- Implementada cancelacion backend de tickets KDS al cancelar una orden.
- Actualizado frontend para usar `POST /orders/pos` y retirar cancelacion manual de tickets KDS.
- Implementado selector de alcance de inventario para `ADMIN`: sucursal activa o vista global.
- Optimizado refresh token con digest indexado y validacion bcrypt de una fila candidata.
- Alineadas acciones de detalle de orden con permisos granulares backend.
- Actualizado frontend a Angular 22, Angular Material 22 y TypeScript 6; build, chequeo de tipos y 23 pruebas pasan.
- Corregidos fixtures de pruebas para usar la configuración real de la aplicación y eliminada la aserción de título obsoleta.
- Versionado `NikkhysBakery-Front/package-lock.json` para instalaciones reproducibles.
- Actualizado backend a `0.4.2` con correcciones compatibles de NestJS, TypeORM, Swagger, Joi, PostgreSQL, Helmet y dependencias transitivas; build, tipos, pruebas y auditoría pasan.
- Renombrada la identidad del proyecto a NikkhysBakery en carpetas, paquetes, runtime, documentación, scripts, interfaz pública y manuales.
- Integrado `.sdd/` en la raíz y adaptado a los repositorios separados frontend/backend, contratos documentados y versiones reales instaladas.
- Corregida la documentación para Angular `22.0.7`, Angular Material `22.0.5`, TypeScript `6.0.3`, NestJS `11.1.28` y backend `0.4.2`.
- Implementado modal persistente de configuración para ítems del catálogo inventariable: abre al seleccionar tarjeta, solo cierra con su botón y permite guardar cambios autorizados.
- Protegida la edición de ítems con historial o dependencias: backend informa bloqueos y valida unidad base, tipo, lotes, stock negativo y estado antes de guardar.
- Corregido el detalle de ítem para usar consultas compatibles al calcular bloqueos; el modal queda sobre el navbar y se adapta al viewport móvil.
- Movido el detalle de catálogo inventariable a `MatDialog` con cierre exclusivo por botón, protección conservadora ante fallo de bloqueos y lista de transacciones asociadas.
- Implementados horarios configurables por sucursal, consulta pública y tabs Material sincronizados entre la sección de ubicación y el footer.
- Normalizada la edición y respuesta de horarios al formato de 24 horas `HH:mm`.
- Mejorada la visualización pública de horarios con filas separadas por grupo de días.
