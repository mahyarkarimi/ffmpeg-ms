FROM python:3.9-slim-buster
RUN --mount=type=cache,target=/var/cache/apt \
	apt-get update && apt-get install -y --no-install-recommends pipenv ffmpeg libmagic1 openssl

WORKDIR /app
COPY Pipfile.lock ./Pipfile.Lock
COPY Pipfile ./Pipfile
RUN --mount=type=cache,target=/root/.cache/pip pipenv install --deploy --ignore-pipfile
COPY . .

EXPOSE 8000
CMD [ "pipenv", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info", "--use-colors", "main:app" ]