# NikkhysBakery

Proyecto fullstack para operar NikkhysBakery: sitio publico, panel administrativo,
POS, KDS, catalogo, inventario, recetas, costeo, produccion, usuarios, permisos y
reporteria.

La raiz funciona como capa de especificacion y coordinacion. El codigo vive en
repositorios separados:

- `NikkhysBakery-Front`: frontend Angular.
- `NikkhysBakery-Back`: backend NestJS.

## Mapa del Proyecto

- `docs/`: especificacion funcional y tecnica fullstack.
- `tasks/`: backlog, tarea actual y registro de avances del proyecto completo.
- `agents/`: roles de trabajo para desarrollo asistido por agentes.
- `NikkhysBakery-Front/`: aplicacion Angular.
- `NikkhysBakery-Back/`: API NestJS y modelo de datos.

## Documentacion Principal

1. `docs/01-contexto-negocio.md`
2. `docs/02-requerimientos-generales.md`
3. `docs/03-arquitectura-general.md`
4. `docs/04-flujos-end-to-end.md`
5. `docs/05-contratos-front-back.md`

## Fuentes de Verdad

- Negocio y alcance fullstack: `docs/`.
- Contratos front-back: `docs/05-contratos-front-back.md`.
- Arquitectura frontend: `NikkhysBakery-Front/docs/`.
- Arquitectura backend, API y datos: `NikkhysBakery-Back/docs/`.
- Estado operativo del trabajo: `tasks/current-task.md`.

Cuando una feature cambia comportamiento, contratos, permisos o modelo de datos,
la documentacion debe actualizarse en el mismo cambio.

## Puesta en Marcha

Backend:

```bash
cd NikkhysBakery-Back
npm install
cp .env.example .env
npm run migration:run
npm run start:dev
```

Frontend:

```bash
cd NikkhysBakery-Front
npm install
npm start
```

Configuracion esperada por defecto:

- Backend: `http://localhost:3000`
- Frontend: `http://localhost:4200`
- Swagger: `http://localhost:3000/docs`

## Regla Spec-Driven

Antes de implementar una feature no trivial:

1. Definir objetivo de negocio.
2. Revisar flujo end-to-end afectado.
3. Definir o actualizar contrato front-back.
4. Identificar permisos, errores y migraciones.
5. Implementar en el repo correspondiente.
6. Validar y registrar resultado en `tasks/done.md`.
