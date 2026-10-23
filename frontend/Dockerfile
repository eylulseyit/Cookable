# Build stage: install dependencies and produce the static build in dist/
FROM docker.io/library/node:22-alpine AS build

RUN npm install -g pnpm@12.15.0

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

# VITE_* variables are inlined into the JavaScript bundle at build time
ARG VITE_API_URL=http://localhost:8000/api/v1
ENV VITE_API_URL=$VITE_API_URL
RUN pnpm build

# Runtime stage: serve the static files with an unprivileged nginx
FROM docker.io/nginxinc/nginx-unprivileged:1.29-alpine

COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
