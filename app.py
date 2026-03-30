from flask import Flask, jsonify, Response
import requests
import os

app = Flask(__name__)

SOURCE = "https://badboysxs-morpheus.hf.space"
BLOCKED_KEYWORDS = ["hindi", "moviebox", "doflix", "streamflix"]

def is_blocked(stream: dict) -> bool:
    haystack = " ".join([
        str(stream.get("name", "")),
        str(stream.get("title", "")),
        str(stream.get("description", "")),
        str(stream.get("behaviorHints", "")),
        str(stream.get("url", "")),
        str(stream.get("externalUrl", "")),
    ]).lower()
    return any(keyword in haystack for keyword in BLOCKED_KEYWORDS)

@app.route("/", methods=["GET"])
def root():
    return Response("OK - open /manifest.json", mimetype="text/plain")

@app.route("/manifest.json", methods=["GET"])
def manifest():
    return jsonify({
        "id": "org.nytoowee.miroir",
        "version": "1.0.0",
        "name": "Miroir Filter",
        "resources": ["stream"],
        "types": ["movie", "series"],
        "idPrefixes": ["tt"]
    })

@app.route("/stream/<media_type>/<path:media_id>.json", methods=["GET"])
def stream(media_type, media_id):
    r = requests.get(f"{SOURCE}/stream/{media_type}/{media_id}.json")
    data = r.json()
    data["streams"] = [s for s in data.get("streams", []) if not is_blocked(s)]
    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
