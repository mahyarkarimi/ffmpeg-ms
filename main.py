import os
import uuid
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from starlette.middleware.authentication import AuthenticationMiddleware

import subprocess
import shlex
import logging
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import magic
from middlewares.authentication_middleware import BasicAuthMiddlewareBackend
from middlewares.limit_upload_size import LimitUploadSize
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address


file_upload_limit = int(os.environ.get('FILE_UPLOAD_LIMIT', '50_000_000'))

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    LimitUploadSize, max_upload_size=file_upload_limit
)

if os.path.exists('.htpasswd'):
    app.add_middleware(AuthenticationMiddleware, backend=BasicAuthMiddlewareBackend())

@app.post('/convert')
@limiter.limit("5/minute")
def convert(request: Request, action: str, file: UploadFile = File(...), buffer_size: int=524288):
    try:
        command = f"ffmpeg -loglevel quiet -i /dev/stdin {action} -"
        ffmpeg_cmd = subprocess.Popen(
            shlex.split(command),
            stdin=file.file,
            stdout=subprocess.PIPE,
            shell=False
        )
        mime_type = 'application/octet-stream'
        def generate():
            while True:
                output = ffmpeg_cmd.stdout.read(buffer_size)
                if len(output) > 0:
                    mime_type = magic.Magic(mime=True).from_buffer(output)
                    yield output
                else:
                    ffmpeg_cmd.wait()
                    last = ffmpeg_cmd.stdout.read(buffer_size)
                    yield last
                    break
        
        return StreamingResponse(generate(), media_type=mime_type)
    except Exception as e:
        logging.error(e)
        if ffmpeg_cmd is not None:
            ffmpeg_cmd.terminate()
        return {'error': str(e) }



@app.post('/convert-file')
@limiter.limit("5/minute")
def convert(request: Request, action: str, file: UploadFile = File(...)):
    try:
        suffix = action.split(' ')[action.split(' ').index('-f') + 1]
        temp_df, temp_path = tempfile.mkstemp(suffix, prefix=str(uuid.uuid4()))
        command = f"ffmpeg -loglevel quiet -y -i /dev/stdin {action} {temp_path}"
        ffmpeg_cmd = subprocess.Popen(
            shlex.split(command),
            stdin=file.file,
            shell=False,
        )
        ffmpeg_cmd.wait()
        mime_type = magic.Magic(mime=True).from_file(temp_path)
        return FileResponse(temp_path, media_type=f'{mime_type}')
    except Exception as e:
        logging.error(e)
        if ffmpeg_cmd is not None:
            ffmpeg_cmd.terminate()
        return {'error': str(e) }