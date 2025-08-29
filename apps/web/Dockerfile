# Web Dockerfile
FROM node:18-alpine AS base
WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@8.15.0 --activate

# Copy package files
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml* ./
COPY turbo.json ./
COPY packages packages
COPY apps/web/package.json apps/web/

# Development stage
FROM base AS development
RUN pnpm install --frozen-lockfile
COPY apps/web apps/web
EXPOSE 3000
CMD ["pnpm", "--filter", "@government-asset/web", "run", "dev"]

# Build stage
FROM base AS builder
RUN pnpm install --frozen-lockfile
COPY apps/web apps/web
RUN pnpm --filter @government-asset/web run build

# Production stage
FROM node:18-alpine AS production
WORKDIR /app

RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001

# Copy built application
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/.next/static ./apps/web/.next/static
COPY --from=builder --chown=nextjs:nodejs /app/apps/web/public ./apps/web/public

USER nextjs
EXPOSE 3000

ENV NODE_ENV=production
ENV HOSTNAME=0.0.0.0

CMD ["node", "apps/web/server.js"]