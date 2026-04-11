---
name: docker
description: Docker-based markitdown converter. Use when uvx is unavailable or for isolated execution.
---

# Docker Converter

Convert documents using markitdown in a Docker container.

## Setup (once)

Clone and build the image:

```bash
git clone https://github.com/microsoft/markitdown.git /tmp/markitdown
cd /tmp/markitdown
docker build -t markitdown:latest .
```

## Usage

### With volume mount (recommended)

```bash
docker run --rm -v "$(pwd):/data" -w /data markitdown:latest input.pdf -o output_docker.md
```

### Via stdin/stdout

```bash
docker run --rm -i markitdown:latest < input.pdf > output_docker.md
```

### With absolute paths

```bash
docker run --rm -v "/path/to/files:/data" -w /data markitdown:latest document.pdf -o document_docker.md
```

## Verify image exists

```bash
docker images markitdown:latest
```

If no image found, run the setup steps above.

## Notes

- Container runs as non-root user by default
- All markitdown features are included (`[all]` dependencies)
- First build takes a few minutes; subsequent runs are fast
