# Deploy to Render (Free)

This project is ready to deploy on Render's Free plan as a Web Service. It serves both the Flask API and the static frontend from the same service.

## Prerequisites

- A Render account (https://render.com)
- GitHub repo: `hcsarker/cf_techlab_bot` (branch `HCS`)

## Option A: One‑click via render.yaml (recommended)

The repository includes `render.yaml` with a Web Service definition:

- Build: `pip install -r requirements.txt`
- Start: `gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT --timeout 120`
- Health check: `/health`

Steps:

1. In Render, click "New" → "Blueprint" → connect this GitHub repo.
2. Select branch `HCS` and confirm the service name (e.g., `cf-techlab-bot`).
3. Keep plan as "Free"; click "Create Resources".
4. Wait for build & deploy to finish.
5. Open the service URL and verify `GET /health` returns a JSON with `status: healthy`.

## Option B: Manual Web Service

1. Click "New" → "Web Service" → connect GitHub repo `hcsarker/cf_techlab_bot`.
2. Runtime: "Python".
3. Build Command: `pip install -r requirements.txt`.
4. Start Command: `gunicorn app:app --workers 1 --bind 0.0.0.0:$PORT --timeout 120`.
5. Health Check Path: `/health`.
6. Plan: "Free" → Create Web Service.

## Notes

- TensorFlow is heavy; the Free plan has limited memory. Using **1 worker** avoids OOM from multiple model loads.
- First request after deploy may be slower due to model load (increased `--timeout`).
- CORS in `app.py` already allows same-origin and specific origins; serving frontend and API together avoids cross-origin issues.

## Verify

- Home: `/` should render the chat UI.
- API: POST `/chat` with `{"message": "hi"}` should return a reply.
- Health: GET `/health` returns `{ status: "healthy" }`.
