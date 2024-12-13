"""
Application entrypoint
"""

import os
from dotenv import load_dotenv
from flask import jsonify

from src.app import create_app

# Load environment variables
load_dotenv()

app, api = create_app()


@app.route("/swagger.json")
def swagger_json():
    return jsonify(api.spec.to_dict())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
