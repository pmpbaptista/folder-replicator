[![Tox](https://github.com/pmpbaptista/folder-replicator/actions/workflows/tox.yml/badge.svg)](https://github.com/pmpbaptista/folder-replicator/actions/workflows/tox.yml)
[![Deploy Documentation](https://github.com/pmpbaptista/folder-replicator/actions/workflows/docs.yml/badge.svg)](https://github.com/pmpbaptista/folder-replicator/actions/workflows/docs.yml)

# folder-replicator
Python utility for file backup and synchronization.

[folder-replicator Documentation](https://pmpbaptista.github.io/folder-replicator/)

## Installation
```bash
poetry install
```

## Usage
```bash
poetry run folder-replicator --help
```

## Docker Usage
Edit the `docker-compose.yml` file to set the source and destination folders.
```bash
docker compose up build
```

## Development
```bash
poetry install
poetry run tox
```
