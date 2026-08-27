# Requerimientos Generales

## Funcionales

- Permitir login, refresh de sesion y logout.
- Resolver usuario actual, roles, permisos y sucursales.
- Operar catalogo de productos y categorias.
- Crear, modificar, enviar, cerrar y cancelar ordenes.
- Mostrar tickets KDS por estacion y permitir cambios de estado.
- Administrar estaciones y asignacion producto-estacion.
- Administrar insumos, unidades, ubicaciones, stock, movimientos, lotes y alertas.
- Crear recetas versionadas y calcular costos vigentes.
- Crear perfiles/cotizaciones de costeo y analisis de precio.
- Crear, confirmar, completar y cancelar ordenes de produccion.
- Generar reportes operativos y comerciales.
- Administrar usuarios, roles, permisos y acceso por sucursal.

## No Funcionales

- Backend con NestJS, TypeORM y PostgreSQL.
- Frontend con Angular, Angular Material, Tailwind CSS y Signals.
- API HTTP JSON.
- Autenticacion con access token y refresh token en cookie `HttpOnly`.
- Validacion de payloads en backend con `class-validator`.
- Guards de autenticacion, permisos y sucursal.
- Documentacion actualizada junto a cada cambio relevante.

## Seguridad

- El frontend no debe decidir autorizacion final; backend valida permisos.
- El frontend puede ocultar navegacion segun permisos para mejorar UX.
- Los endpoints mutantes deben requerir autenticacion y permisos adecuados.
- Las operaciones multi-sucursal deben enviar o resolver `x-branch-id`.

## Calidad

- Mantener contratos tipados en servicios Angular.
- Mantener DTOs y entidades backend sincronizados con docs.
- Evitar duplicar reglas de negocio entre componentes.
- Priorizar pruebas en flujos criticos: login, POS, cierre, inventario, produccion,
  KDS y reportes.

## Criterios de Aceptacion por Feature

- Objetivo funcional claro.
- Pantallas y rutas afectadas identificadas.
- Endpoints, payloads y respuestas definidos.
- Permisos definidos.
- Errores esperados definidos.
- Migracion definida si cambia datos.
- Validacion manual o automatizada registrada.

