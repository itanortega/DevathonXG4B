import eventlet
eventlet.monkey_patch()

from flask import Flask, request, send_file
from sio_asyncapi import AsyncAPISocketIO
from dotenv import load_dotenv
import os
import pathlib

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

if os.getenv("FLASK_ENV") == "development":
    origins = "*"
else:
    origins = os.getenv("FRONTEND_URL", "").split(",")

socketio = AsyncAPISocketIO(
    app,
    cors_allowed_origins=origins,
    validate=True,
    generate_docs=True,
    version="1.0.0",
    title="Tic-Tac-Toe API",
    description="Tic-Tac-Toe Game API",
    server_url="http://localhost:5000",
    server_name="TIC_TAC_TOE_BACKEND",
)


from events import register_handlers
register_handlers(socketio)


@app.route('/asyncapi.yaml')
def get_asyncapi_spec():
    spec_path = pathlib.Path(__file__).parent / "asyncapi.yaml"
    if spec_path.exists():
        return send_file(spec_path, mimetype='application/yaml')
    return {"error": "Spec not found"}, 404


if __name__ == '__main__':
    path = pathlib.Path(__file__).parent / "asyncapi.yaml"
    doc_str = socketio.asyncapi_doc.get_yaml()
    with open(path, "w") as f:
        f.write(doc_str)
    print(f"✅ AsyncAPI spec saved to {path}")

    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=(os.getenv("FLASK_ENV") == "development"),
        use_reloader=False
    )