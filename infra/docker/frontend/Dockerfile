FROM node:22-alpine AS builder

WORKDIR /app/frontend

COPY NikkhysBakery-Front/package.json NikkhysBakery-Front/package-lock.json ./
RUN npm ci

COPY NikkhysBakery-Front .
RUN npm run build

FROM nginx:1.27-alpine AS runtime

COPY --from=builder /app/frontend/dist/NikkhysBakery/browser /usr/share/nginx/html
COPY infra/nginx/nikkhysbakery.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
