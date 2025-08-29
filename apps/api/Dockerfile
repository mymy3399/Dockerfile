# API Dockerfile
FROM node:18-alpine AS base
WORKDIR /app

# Install pnpm
RUN corepack enable && corepack prepare pnpm@8.15.0 --activate

# Copy package files
COPY package.json pnpm-workspace.yaml pnpm-lock.yaml* ./
COPY turbo.json ./
COPY packages packages
COPY apps/api/package.json apps/api/

# Development stage
FROM base AS development
RUN pnpm install --frozen-lockfile
COPY apps/api apps/api
RUN pnpm --filter @government-asset/api run db:generate
EXPOSE 4000
CMD ["pnpm", "--filter", "@government-asset/api", "run", "start:dev"]

# Build stage
FROM base AS builder
RUN pnpm install --frozen-lockfile
COPY apps/api apps/api
RUN pnpm --filter @government-asset/api run db:generate
RUN pnpm --filter @government-asset/api run build

# Production stage
FROM node:18-alpine AS production
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@8.15.0 --activate
RUN addgroup -g 1001 -S nodejs && adduser -S nestjs -u 1001

COPY --from=builder --chown=nestjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nestjs:nodejs /app/packages ./packages
COPY --from=builder --chown=nestjs:nodejs /app/apps/api/dist ./apps/api/dist
COPY --from=builder --chown=nestjs:nodejs /app/apps/api/prisma ./apps/api/prisma
COPY --from=builder --chown=nestjs:nodejs /app/apps/api/package.json ./apps/api/

USER nestjs
EXPOSE 4000

ENV NODE_ENV=production
CMD ["node", "apps/api/dist/main.js"]