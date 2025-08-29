# Government Asset Management System - Makefile
# Common development and deployment tasks

.PHONY: help dev build clean install migrate seed up down logs test lint format

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

help: ## Show this help message
	@echo "$(GREEN)Government Asset Management System$(RESET)"
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "  $(BLUE)%-15s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	@echo "$(YELLOW)Installing dependencies...$(RESET)"
	pnpm install

dev: ## Start development servers
	@echo "$(GREEN)Starting development servers...$(RESET)"
	pnpm dev

build: ## Build all applications
	@echo "$(GREEN)Building applications...$(RESET)"
	pnpm run build

clean: ## Clean build artifacts and dependencies
	@echo "$(YELLOW)Cleaning build artifacts...$(RESET)"
	pnpm run clean
	rm -rf node_modules apps/*/node_modules packages/*/node_modules
	rm -rf apps/*/.next apps/*/dist packages/*/dist

# Database commands
migrate: ## Run database migrations
	@echo "$(GREEN)Running database migrations...$(RESET)"
	pnpm --filter @government-asset/api run db:migrate

generate: ## Generate Prisma client
	@echo "$(GREEN)Generating Prisma client...$(RESET)"
	pnpm --filter @government-asset/api run db:generate

seed: ## Seed database with sample data
	@echo "$(GREEN)Seeding database...$(RESET)"
	pnpm --filter @government-asset/api run db:seed

db-reset: migrate generate seed ## Reset database (migrate, generate, seed)
	@echo "$(GREEN)Database reset complete!$(RESET)"

# Docker commands
up: ## Start Docker Compose services
	@echo "$(GREEN)Starting Docker Compose services...$(RESET)"
	docker compose -f infra/docker-compose.yml up -d

down: ## Stop Docker Compose services
	@echo "$(YELLOW)Stopping Docker Compose services...$(RESET)"
	docker compose -f infra/docker-compose.yml down

logs: ## View Docker Compose logs
	@echo "$(BLUE)Viewing Docker Compose logs...$(RESET)"
	docker compose -f infra/docker-compose.yml logs -f

# Development commands
test: ## Run tests
	@echo "$(GREEN)Running tests...$(RESET)"
	pnpm run test

test-watch: ## Run tests in watch mode
	@echo "$(GREEN)Running tests in watch mode...$(RESET)"
	pnpm run test --watch

lint: ## Lint code
	@echo "$(GREEN)Linting code...$(RESET)"
	pnpm run lint

lint-fix: ## Lint and fix code issues
	@echo "$(GREEN)Linting and fixing code issues...$(RESET)"
	pnpm run lint --fix

format: ## Format code
	@echo "$(GREEN)Formatting code...$(RESET)"
	pnpm exec prettier --write "**/*.{js,jsx,ts,tsx,json,css,md,yml,yaml}"

type-check: ## Run TypeScript type checking
	@echo "$(GREEN)Running TypeScript type checking...$(RESET)"
	pnpm run type-check

# Docker build commands
docker-build: ## Build Docker images
	@echo "$(GREEN)Building Docker images...$(RESET)"
	docker compose -f infra/docker-compose.yml build

docker-build-prod: ## Build production Docker images
	@echo "$(GREEN)Building production Docker images...$(RESET)"
	docker build -f apps/api/Dockerfile -t government-asset-api:latest --target production .
	docker build -f apps/web/Dockerfile -t government-asset-web:latest --target production .

# Kubernetes commands
k8s-deploy: ## Deploy to Kubernetes
	@echo "$(GREEN)Deploying to Kubernetes...$(RESET)"
	kubectl apply -f infra/k8s/database.yaml
	kubectl apply -f infra/k8s/api.yaml
	kubectl apply -f infra/k8s/web.yaml

k8s-status: ## Check Kubernetes deployment status
	@echo "$(BLUE)Checking Kubernetes status...$(RESET)"
	kubectl get pods -n government-asset-management
	kubectl get services -n government-asset-management

k8s-logs: ## View Kubernetes logs
	@echo "$(BLUE)Viewing Kubernetes logs...$(RESET)"
	kubectl logs -f -l app=api -n government-asset-management

k8s-clean: ## Clean Kubernetes resources
	@echo "$(YELLOW)Cleaning Kubernetes resources...$(RESET)"
	kubectl delete -f infra/k8s/ --ignore-not-found=true

# Utility commands
health: ## Check application health
	@echo "$(BLUE)Checking application health...$(RESET)"
	@curl -s http://localhost:4000/healthz | jq '.' || echo "API not accessible"
	@curl -s http://localhost:3000 > /dev/null && echo "$(GREEN)Web app is accessible$(RESET)" || echo "$(RED)Web app not accessible$(RESET)"

setup: install migrate generate seed ## Complete development setup
	@echo "$(GREEN)Development setup complete!$(RESET)"
	@echo "Run 'make dev' to start development servers"

prod-deploy: docker-build-prod k8s-deploy ## Production deployment
	@echo "$(GREEN)Production deployment initiated$(RESET)"

# Security commands
security-check: ## Run security vulnerability check
	@echo "$(GREEN)Running security checks...$(RESET)"
	pnpm audit
	@echo "$(YELLOW)Consider running additional security scans for production$(RESET)"

# Backup commands
backup-db: ## Backup database (requires proper DATABASE_URL)
	@echo "$(GREEN)Creating database backup...$(RESET)"
	@echo "$(YELLOW)Implement database backup script for production$(RESET)"

# Environment validation
check-env: ## Check environment configuration
	@echo "$(BLUE)Checking environment configuration...$(RESET)"
	@test -f .env && echo "$(GREEN)✓ .env file exists$(RESET)" || echo "$(RED)✗ .env file missing - copy from .env.example$(RESET)"
	@command -v pnpm >/dev/null && echo "$(GREEN)✓ pnpm installed$(RESET)" || echo "$(RED)✗ pnpm not installed$(RESET)"
	@command -v docker >/dev/null && echo "$(GREEN)✓ Docker installed$(RESET)" || echo "$(RED)✗ Docker not installed$(RESET)"
	@command -v kubectl >/dev/null && echo "$(GREEN)✓ kubectl installed$(RESET)" || echo "$(YELLOW)! kubectl not installed (optional for local dev)$(RESET)"