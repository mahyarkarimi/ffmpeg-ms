from re import sub
from sys import stdin, stdout
from flask import Flask, json, request, make_response, jsonify
import os
import subprocess
import shlex
import traceback

app = Flask(__name__)


@app.route('/convert', methods=['POST'])
def convert():
    print(request.files.get('file'))
    action: str = "-f wav -acodec pcm_s16le -ac 1 -ar 44100"
    command = f"ffmpeg -y -i /dev/stdin -f nut {action} -"
    ffmpeg_cmd = subprocess.Popen(
        shlex.split(command),
        stdin=request.files.get('file').stream,
        stdout=subprocess.PIPE,
        shell=False
    )
    try:
        # while True:
        #     output = ffmpeg_cmd.stdout.read()
        #     if len(output) > 0:
        #         b += output
        #     else:
        #         error_msg = ffmpeg_cmd.poll()
        #         if error_msg is not None:
        #             break
        def generate():
            b = b''
            output = ffmpeg_cmd.stdout.read()
            if len(output) > 0:
                b += output
                pass
            else:
                error_msg = ffmpeg_cmd.poll()
                if error_msg is not None:
                    return
            yield output
        return app.response_class(response=generate(), mimetype='application/octec-stream')
    except Exception as e:
        ffmpeg_cmd.terminate()
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
