# backend/Dockerfile
#
# Build from the REPO ROOT, not from inside backend/ — this image needs
# the sibling engine/ folder (inference.py + the serialized .pkl models):
#
#   docker build -f backend/Dockerfile -t elephant-backend .
#
FROM python:3.13-slim

WORKDIR /app

# Install backend + engine dependencies together (backend/requirements.txt
# references ../engine/requirements.txt via -r, so both must exist first)
COPY backend/requirements.txt backend/requirements.txt
COPY engine/requirements.txt engine/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the actual code — engine/ (including models/*.pkl) first, since
# backend/app/main.py imports it via a sys.path insert at ../../engine
COPY engine/ engine/
COPY backend/app/ backend/app/

WORKDIR /app/backend

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]