FROM jrottenberg/ffmpeg:5.0.2-alpine313
RUN apk --no-cache --update add python3 libmagic openssl
RUN python3 -m ensurepip
RUN --mount=type=cache,target=/root/.cache/pip pip3 install pipenv

WORKDIR /app
COPY Pipfile.lock ./Pipfile.lock
COPY Pipfile ./Pipfile
RUN --mount=type=cache,target=/root/.cache/pip pipenv install --system --deploy --ignore-pipfile
COPY . .

EXPOSE 8000
ENTRYPOINT [ "pipenv", "run", "uvicorn" ]
CMD [ "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info", "--use-colors", "main:app" ]