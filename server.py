from flask import Flask, request, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # allows your website (opened as a local file) to talk to this server

FREEMODEL_URL = "https://api.freemodel.dev/v1/chat/completions"

@app.route("/chat", methods=["POST"])
def chat():
    auth_header = request.headers.get("Authorization", "")
    payload = request.get_json()

    def generate():
        with requests.post(
            FREEMODEL_URL,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": auth_header
            },
            stream=True,
            timeout=120
        ) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk

    return Response(generate(), content_type="text/event-stream")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"Relay server running on port {port}")
    app.run(host="0.0.0.0", port=port)
