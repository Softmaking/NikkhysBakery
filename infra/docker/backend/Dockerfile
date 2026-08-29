FROM node:22-alpine AS dependencies

WORKDIR /app/backend

COPY NikkhysBakery-Back/package.json NikkhysBakery-Back/package-lock.json ./
RUN npm ci

FROM dependencies AS builder

COPY NikkhysBakery-Back .
RUN npm run build

FROM node:22-alpine AS runtime

WORKDIR /app/backend
ENV NODE_ENV=production

COPY NikkhysBakery-Back/package.json NikkhysBakery-Back/package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY --from=builder /app/backend/dist ./dist

EXPOSE 3000
CMD ["node", "dist/main.js"]
