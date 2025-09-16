# Custom Caddy Docker Build

This repository contains a Dockerfile that builds a custom Caddy web server with two specific plugins:
- `github.com/caddy-dns/cloudflare` - DNS-01 ACME challenge support for Cloudflare DNS API
- `github.com/greenpau/caddy-security` - Security plugin for Caddy

**Always reference these instructions first** and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Critical Requirements
- **Internet Access Required**: The Docker build process downloads Go modules from github.com and requires unrestricted internet access
- **Build May Fail in Restricted Environments**: Corporate firewalls, sandboxed systems, or environments without GitHub access will cause build failures
- **Expected Build Time**: 2-5 minutes with good network connectivity

## Working Effectively

### Building the Docker Image
- **CRITICAL**: Build requires internet access to download Go modules from github.com and proxy.golang.org
- Build command: `docker build -t custom-caddy .`
- **NEVER CANCEL**: Build takes 2-5 minutes depending on network speed and Go module download time. Set timeout to 10+ minutes.
- If build fails with TLS/certificate errors, try with Go proxy environment variables:
  ```bash
  docker build --build-arg GOPROXY=direct --build-arg GOSUMDB=off -t custom-caddy .
  ```
- If build fails with network connectivity issues (common in restricted environments):
  - Document the limitation: "Build fails due to network restrictions preventing access to github.com"
  - Alternative: Use pre-built images or build in environments with full internet access

### Running the Container
- Basic file server test: `docker run --rm -p 8080:80 custom-caddy caddy file-server --browse --listen :80`
- Access test server: `curl http://localhost:8080/` or browser to `http://localhost:8080`
- Background daemon: `docker run -d --name caddy-server -p 80:80 -p 443:443 custom-caddy`
- Stop daemon: `docker stop caddy-server && docker rm caddy-server`

### Validating the Build
- **ALWAYS** verify plugins are included after building:
  ```bash
  docker run --rm custom-caddy caddy list-modules | grep -E "(dns.providers.cloudflare|security)"
  ```
- Test basic functionality: `docker run --rm -p 8080:80 custom-caddy caddy file-server --browse --listen :80`
- **VALIDATION SCENARIO**: After any changes to the Dockerfile:
  1. Build the image: `docker build -t custom-caddy-test .`
  2. Verify plugins: `docker run --rm custom-caddy-test caddy list-modules | grep -c -E "(dns.providers.cloudflare|security)"`
  3. Check version: `docker run --rm custom-caddy-test caddy version`
  4. Test binary works: `docker run --rm custom-caddy-test caddy help | head -5`
  5. **NOTE**: Full server testing may require different ports or environments depending on Docker setup

## Common Build Issues and Solutions

### Network Connectivity Problems
- **Issue**: `Could not resolve host: github.com` or certificate verification errors
- **Common in**: Restricted environments, corporate firewalls, or sandboxed build systems
- **Solution 1**: Build in environment with full internet access
- **Solution 2**: Use alternative Go proxy settings by modifying Dockerfile:
  ```dockerfile
  FROM caddy:builder AS builder
  
  ENV GOPROXY=direct
  ENV GOSUMDB=off
  
  RUN xcaddy build \
      --with github.com/caddy-dns/cloudflare \
      --with github.com/greenpau/caddy-security
  ```
- **Solution 3**: Use `docker build --network=host` on some systems

### Expected Plugin Output
When the build succeeds, `docker run --rm custom-caddy caddy list-modules` should include:
- `dns.providers.cloudflare` - For Cloudflare DNS ACME challenges
- Various `security.*` modules from the caddy-security plugin (e.g., `security.authentication`, `security.authorization`)

### Base Caddy Modules (for reference)
The base `caddy:latest` image (v2.10.0) includes standard modules like:
- File server capabilities
- Reverse proxy functionality  
- Automatic HTTPS
- Various listeners and adapters
- Docker must be installed and running
- Internet access required for downloading Go modules
- Sufficient disk space for multi-stage build (typically 500MB+)

## Repository Structure
```
.
├── Dockerfile          # Multi-stage build for custom Caddy with plugins
├── README.md          # Basic project description
└── .github/           # GitHub configuration and workflows
    └── copilot-instructions.md  # This file
```

## Dockerfile Analysis
The build process:
1. **Stage 1 (builder)**: Uses `caddy:builder` base image with xcaddy to compile custom binary
2. **Stage 2 (runtime)**: Uses `caddy:latest` and copies the custom binary from builder stage

## Timing Expectations
- **Docker build**: 2-5 minutes (NEVER CANCEL - set 10+ minute timeout)
- **Container startup**: < 5 seconds
- **Plugin verification**: < 10 seconds
- **Basic functionality test**: < 30 seconds

## Key Commands Reference
```bash
# Build (standard)
docker build -t custom-caddy .

# Build (with network workarounds)
docker build --build-arg GOPROXY=direct --build-arg GOSUMDB=off -t custom-caddy .

# Quick test
docker run --rm -p 8080:80 custom-caddy caddy file-server --browse --listen :80

# List available modules/plugins
docker run --rm custom-caddy caddy list-modules

# Get Caddy version
docker run --rm custom-caddy caddy version

# Production deployment with volume mounts
docker run -d --name caddy \
  -p 80:80 -p 443:443 \
  -v $(pwd)/Caddyfile:/etc/caddy/Caddyfile \
  -v caddy_data:/data \
  -v caddy_config:/config \
  custom-caddy
```

## Testing Custom Configurations
When testing Caddyfile configurations that use the included plugins:
- **Cloudflare DNS plugin**: Requires `CLOUDFLARE_EMAIL` and `CLOUDFLARE_API_KEY` environment variables
- **Security plugin**: Test authentication flows and security headers
- Always test in non-production environment first

Example Caddyfile using Cloudflare DNS:
```
example.com {
  tls {
    dns cloudflare {env.CLOUDFLARE_EMAIL} {env.CLOUDFLARE_API_KEY}
  }
  respond "Hello, World!"
}
```

Example with security plugin:
```
example.com {
  security {
    authentication portal myportal {
      crypto default token lifetime 3600
    }
  }
  respond "Secured content"
}
```

## Working with Caddyfiles
- Mount Caddyfile: `docker run -v ./Caddyfile:/etc/caddy/Caddyfile custom-caddy`
- Validate config: `docker run --rm -v ./Caddyfile:/etc/caddy/Caddyfile custom-caddy caddy validate --config /etc/caddy/Caddyfile`
- Format Caddyfile: `docker run --rm -v ./Caddyfile:/etc/caddy/Caddyfile custom-caddy caddy fmt --overwrite --config /etc/caddy/Caddyfile`

## Troubleshooting
- If containers fail to start: Check logs with `docker logs <container-name>`
- If plugins seem missing: Verify with `docker run --rm custom-caddy caddy list-modules`
- If build fails: Ensure internet connectivity and sufficient disk space
- For permission issues: Check if Docker daemon is running and user has proper permissions