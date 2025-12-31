# customcommands

Write your command content here.

This command will be available in chat with /customcommands

{
  "commands": [
    {
      "name": "Run Security Audit",
      "command": "npm run security:audit || python -m pip-audit || safety check",
      "description": "Run security vulnerability checks on dependencies"
    },
    {
      "name": "Run Tests",
      "command": "npm test || pytest || python -m pytest",
      "description": "Run all unit and integration tests"
    },
    {
      "name": "Check Code Coverage",
      "command": "npm run test:coverage || pytest --cov || python -m pytest --cov",
      "description": "Generate and view test coverage report"
    },
    {
      "name": "Lint Code",
      "command": "npm run lint || pylint . || flake8 .",
      "description": "Run linter to check code quality"
    },
    {
      "name": "Format Code",
      "command": "npm run format || black . || prettier --write .",
      "description": "Format code according to style guide"
    },
    {
      "name": "Generate API Docs",
      "command": "npm run docs:generate || swagger-codegen generate",
      "description": "Generate API documentation from OpenAPI spec"
    },
    {
      "name": "Database Migration",
      "command": "npm run db:migrate || alembic upgrade head || python manage.py migrate",
      "description": "Run database migrations"
    },
    {
      "name": "Start Development Server",
      "command": "npm run dev || python manage.py runserver || uvicorn main:app --reload",
      "description": "Start the development server with hot reload"
    }
  ]
}