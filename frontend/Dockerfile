# frontend/Dockerfile
#
# Build from INSIDE frontend/:
#   docker build -t elephant-frontend .
#
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ── Runtime stage — only the built Nitro output ships, not node_modules/src ──
FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/.output ./.output

ENV HOST=0.0.0.0
ENV PORT=3000
# Overridable at `docker run` time without rebuilding — Nuxt reads
# runtimeConfig.public overrides from env vars at server start.
ENV NUXT_PUBLIC_API_BASE=http://localhost:8000

EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]
