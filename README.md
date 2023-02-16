# JustThinking

JustThinking is a simple social media API template where you can create users, posts and comments. 
It was created as a side project for training my Python, API's and CI/CD skills.

# Documentation

https://just-thinking.fly.dev/docs (Swagger) & https://just-thinking.fly.dev/redoc (Redocly)

# Technologies

- The core is in Python using FastAPI and SQLalchemy libraries.
- PostgreSQL database using Alembic for migrations.
- Integration and unit tests using Pytest.
- Automated pipeline using GitHub Actions for test, build a Docker image and deploy in production using Fly.io.

# Usage

API url: https://just-thinking.fly.dev/

JustThinking uses OAuth2 as authentication protocol for posts and comments endpoints. 
So first you need to already have a user or create a new one using users endpoint.
After that use the login endpoint which return a access token with 30 minutes to expire.

# Example usage in swagger

