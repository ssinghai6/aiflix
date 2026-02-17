# Moving AiFlix to Production

Currently, AiFlix runs as a local CLI script. To move to a production-grade web application, follow this roadmap.

## 1. Expose as an API (FastAPI)
Wrap the `Orchestrator` in a REST API to allow web frontends to trigger productions.

**Required Changes:**
- Create `src/api.py`.
- Define endpoints:
    - `POST /projects` (Accept concept, return project_id)
    - `GET /projects/{id}/status` (Return state/progress)
    - `GET /projects/{id}/media` (Return URLs)

## 2. Asynchronous Task Queue (Celery/Redis)
Video generation is slow (minutes/hours). Do not run it in the main HTTP request loop.
- **Tools**: Redis (Broker), Celery (Worker).
- **Flow**: API pushes `run_pipeline` job to Redis -> Celery Worker calls Replicate -> Worker updates Database.

## 3. Persistent Database (PostgreSQL)
Replace the in-memory `ProjectState` with a real database.
- **Tables**: `Projects`, `Scripts`, `Shots`, `Characters`.
- Use `SQLAlchemy` or `Prisma` for ORM.

## 4. Dockerization
Containerize the application for easy deployment.

**Dockerfile Example (Draft):**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 5. Storage (S3 / Cloud Storage)
Stop saving files to local `output/` folder.
- configure `ImageGenerator` and `VideoGenerator` to upload to AWS S3 or Google Cloud Storage.
- Save the S3 URLs in the Database.

## 6. Deployment (Render / Railway / AWS)
- Deploy the Docker container.
- Set environment variables (`GROQ_API_KEY`, `REPLICATE_API_TOKEN`, `DATABASE_URL`) in the cloud dashboard.
