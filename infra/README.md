# Despliegue Docker

La infraestructura Docker de NikkhysBakery ejecuta PostgreSQL, backend NestJS,
migraciones, seed y frontend Angular servido por Nginx.

## Requisitos

- Docker Engine con Docker Compose v2.
- Un archivo de secretos fuera del repositorio en:
  `$SERVER_ROOT/secrets/nikkhysbakery/backend.env`.
- Un archivo `.env` del servidor con `SERVER_ROOT`, `POSTGRES_PASSWORD` y los
  valores de infraestructura necesarios.

El archivo de secretos debe contener las variables del backend definidas en
`NikkhysBakery-Back/.env.example`, además de `DB_USER`, `DB_PASSWORD`,
`JWT_ACCESS_SECRET`, `JWT_REFRESH_SECRET`, `JWT_ISSUER` y `JWT_AUDIENCE`.

## Despliegue

```bash
docker compose build
docker compose up -d postgres
docker compose run --rm backend-migrate
docker compose up -d backend frontend
```

Para crear los datos iniciales, ejecutar una sola vez:

```bash
docker compose run --rm backend-seed
```

## Operación

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
docker compose down
```

El frontend queda disponible en `127.0.0.1:4200`. Un Nginx del servidor puede
terminar TLS y reenviar el dominio público hacia ese puerto. Las solicitudes
`/api/*` son reenviadas internamente al backend y el backend escucha en el
puerto 3000 dentro de la red Docker.

El volumen `nikkhysbakery-postgres-data` conserva la base de datos. Antes de
actualizar migraciones en un servidor, realizar un respaldo de PostgreSQL.
