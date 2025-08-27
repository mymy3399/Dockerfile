# Custom Caddy Docker Build

Custom Caddy web server Docker image with Cloudflare DNS and security plugins. Built using multi-stage Docker build with xcaddy.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Build
- **Primary build command**: `docker build -t custom-caddy .`
  - **NEVER CANCEL**: Build takes 3-5 minutes when network access is available. Set timeout to 10+ minutes.
  - **CRITICAL**: Build requires internet access to download Go modules from github.com and proxy.golang.org
  - **Network Issues**: Build fails in restricted network environments with certificate verification or DNS resolution errors

- **Alternative build with network workarounds**:
  ```bash
  # Try if primary build fails due to network issues
  docker build --build-arg GOPROXY=direct --build-arg GOSUMDB=off -t custom-caddy .
  ```

- **Build failure troubleshooting**:
  - Error "tls: failed to verify certificate: x509: certificate signed by unknown authority" = network/proxy issues
  - Error "Could not resolve host: github.com" = DNS/network restrictions
  - These are environment limitations, not code issues

### Testing and Validation

- **Test base Caddy functionality**:
  ```bash
  # Verify base Caddy image works
  docker run --rm caddy:latest caddy version
  
  # Start basic file server for testing
  docker run --rm -p 8080:80 caddy:latest caddy file-server --browse --root /usr/share/caddy
  ```

- **Test custom build (when successful)**:
  ```bash
  # Run the custom built image
  docker run --rm -p 8080:80 custom-caddy caddy file-server --browse --root /usr/share/caddy
  
  # Verify custom plugins are available
  docker run --rm custom-caddy caddy list-modules | grep -E "(cloudflare|security)"
  ```

- **Manual validation scenarios**:
  - Always test HTTP server responds: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/`
  - Expected response: `200`
  - Test basic web server functionality by accessing http://localhost:8080 in browser
  - Verify the server starts without errors in the logs

### Build Time Expectations
- **NEVER CANCEL**: Docker build takes 3-5 minutes with good network connectivity
- **NEVER CANCEL**: Initial image pulls may take 1-2 minutes for base images  
- **NEVER CANCEL**: Go module download and compilation takes 2-3 minutes
- **Timeout recommendations**: Set 10+ minute timeouts for docker build commands
- **When build fails**: Usually fails within 30 seconds due to network issues, not after long compilation

## Repository Structure and Key Components

### Core Files
```
/home/runner/work/Dockerfile/Dockerfile/
├── Dockerfile          # Multi-stage build definition
└── README.md          # Minimal documentation
```

### Dockerfile Analysis
The Dockerfile creates a custom Caddy build with:
- **Base**: Uses `caddy:builder` for building, `caddy:latest` for final image
- **Custom Plugins**: 
  - `github.com/caddy-dns/cloudflare` - Cloudflare DNS challenge support for ACME certificates
  - `github.com/greenpau/caddy-security` - Additional security middleware and authentication
- **Build tool**: Uses `xcaddy` to compile custom Caddy binary with plugins
- **Output**: Single-stage final image with custom Caddy binary at `/usr/bin/caddy`

## Common Issues and Solutions

### Build Failures
- **Issue**: `tls: failed to verify certificate` or `Could not resolve host: github.com`
- **Cause**: Network restrictions in Docker build environment
- **Solution**: Document as known limitation, test functionality using base `caddy:latest` image instead
- **Workaround**: Use base Caddy image for basic functionality testing

### Network Environment Limitations
- **Do not try to fix network issues** - these are environment constraints
- **Do not modify Dockerfile** to work around network issues without explicit requirements
- **Always document when build fails** due to network restrictions
- **Use base Caddy image** for functionality validation when custom build fails

### Testing Without Custom Build
When custom build fails due to network restrictions:
```bash
# Test basic Caddy functionality
docker run --rm -p 8080:80 caddy:latest caddy file-server --browse --root /usr/share/caddy

# Validate HTTP response
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/
```

## Validation Checklist
Before completing any changes to this repository:
- [ ] Run `docker build -t custom-caddy .` (expected to fail in restricted networks)
- [ ] If build fails, document the specific error message
- [ ] Test base Caddy functionality: `docker run --rm caddy:latest caddy version`
- [ ] Start test server: `docker run --rm -p 8080:80 caddy:latest caddy file-server --browse`
- [ ] Verify HTTP response: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/`
- [ ] Expected result: HTTP 200 response from localhost:8080

## Expected Behavior
- **In unrestricted networks**: Build succeeds in 3-5 minutes, custom plugins available
- **In restricted networks**: Build fails with network/certificate errors, base functionality works
- **Always**: Basic Caddy image works for testing core web server functionality
- **Never**: Modify Dockerfile without understanding plugin requirements and network dependencies