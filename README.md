# JustThinking

JustThinking is a social media API that can be used to create posts and comments by registered users. It was created as a side project to  sharpen my Python, API's and CI/CD skills.

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

Example usage in swagger:

[justthinking_example.webm](https://user-images.githubusercontent.com/83092575/219463387-6898f439-56ed-4f43-9daa-3163e9044fbb.webm)
