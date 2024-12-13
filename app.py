"""
Application entrypoint
"""

from flask import jsonify
from src.app import create_app

app, api = create_app()


@app.route("/swagger.json")
def swagger_json():
    return jsonify(api.spec.to_dict())


if __name__ == "__main__":
    app.run()
