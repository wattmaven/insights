# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Setup and Installation
```bash
# Install uv package manager (required)
# See: https://docs.astral.sh/uv/getting-started/installation/

# Create virtual environment
make

# Activate virtual environment
source .venv/bin/activate

# Install all dependencies
uv sync --all-packages

# Install git hooks
make install-hooks
```

### Development Workflow
```bash
# Run development server with auto-reload
make dev
# or
insights --reload true

# Run tests
make test

# Run specific test markers
uv run pytest -m unit
uv run pytest -m integration
uv run pytest -m e2e

# Run a single test
uv run pytest tests/integration/test_root.py::test_root -v

# Code quality checks
make lint-check         # Check linting
make format-check       # Check formatting
make fix                # Fix all linting and formatting issues
make pre-commit-tasks   # Run pre-commit tasks
make ci-smoke-test      # Run tests in CI

# Clean project
make clean
```

### Release Process
```bash
# Bump version (uses conventional commits)
cz bump --major-version-zero

# Push changes and tags
git push
git push -u origin v<new-version>
```

## High-Level Architecture

### Project Structure
The codebase follows a clean, modular structure:

- **`src/insights/`**: Main application module
  - `main.py`: FastAPI application instance and route definitions
  - `settings.py`: Pydantic settings management with environment variable support
  - `cli.py`: Click-based CLI entry point that launches uvicorn server

- **Configuration Management**: 
  - Uses Pydantic Settings with `.env` file support
  - Settings are cached using `@lru_cache` for performance
  - Key settings: `python_env` (default: "production"), `insights_domain`

- **Testing Strategy**:
  - Tests organized by type using pytest markers (unit, integration, e2e)
  - Integration tests use FastAPI's TestClient
  - Coverage reporting enabled for `src` directory

- **Development Tools**:
  - **Ruff**: All-in-one linting and formatting (replaces flake8, black, isort)
  - **uv**: Fast Python package manager for dependency management
  - **Lefthook**: Git hooks for code quality (runs Trufflehog and quality checks)
  - **Commitizen**: Enforces conventional commits for automated versioning

### Key Design Decisions

1. **Minimal Template**: This is intentionally a minimal template without opinionated choices for:
   - Database/ORM (no SQLAlchemy, Alembic)
   - Authentication/Authorization
   - API versioning strategy
   - Background tasks/queuing

2. **Modern Python Tooling**: 
   - Uses `pyproject.toml` exclusively (no setup.py)
   - Hatchling build backend with VCS versioning
   - Python 3.13+ compatibility

3. **Docker-Ready**: 
   - Efficient Dockerfile using `uv` for fast builds
   - Runs on uvicorn with configurable workers
   - Exposes port 8000 by default

4. **CI/CD Pipeline**: 
   - GitHub Actions for automated testing
   - Renovate for dependency updates
   - Conventional commit enforcement