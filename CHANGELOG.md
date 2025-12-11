## 0.2.0 (2025-12-11)

### Feat

- add version_provider to commitizen config
- add version_files to commitizen config
- **development**: #13 - add pre-commit script (ruff, black, isort), fix isort issues
- **deployment**: #12 - fix datetime handling for UTC timezone and remove future date validation for existing data, update deployment (Dockerfile, docker-compose.yml)
- **api**: #11 - update routers items/users, servcies, add tests (unit, integration)
- **seed**: add idempotent seed script and linter fixes
- **database**: #10 - configure Alembic migrations and PostgreSQL support
- **api**: #9 - add FastAPI routers and main application
- **application**: #8 - add service layer with business logic
- **application**: #7 - add Pydantic schemas for API layer
- **infrastructure**: #6 - add repository layer with pattern implementation
- **infrasturcture**: #5 - add SQLAlchemy models and database setup
- **deployment**: #4 - add Docker and PostgreSQL configuration
- **config**: #3 - add application settings config
- **domain**: #2 - add domain entities (User, Item, Tag)
- **deps**: #1 - add project dependencies
- **structure**: #1 - add project structure
- init project

### Fix

- **linter**: #6 - fix linter issues
