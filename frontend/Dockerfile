# Build stage: install dependencies and produce the static export in out/
FROM docker.io/library/node:22-alpine AS build

RUN npm install -g pnpm@12.15.0

WORKDIR /app

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

# NEXT_PUBLIC_* variables are inlined into the JavaScript bundle at build time
ARG NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL \
    NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

# Runtime stage: serve the static files with an unprivileged nginx
FROM docker.io/nginxinc/nginx-unprivileged:1.29-alpine

COPY --from=build /app/out /usr/share/nginx/html
EXPOSE 8080
