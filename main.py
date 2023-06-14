import re
from flask import Flask, request, jsonify, render_template
import openai
import os
from gunicorn.app.base import BaseApplication
import json


class FlaskApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",  # Assuming GPT-4 is the model you're using
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=1024,
            # stream=True,
        )
        # Format the response message
        response_message = re.sub(r"\n", "<br>", response["choices"][0]["text"])
        return jsonify({"message": response_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # app.run(debug=True)
    options = {
        "bind": "0.0.0.0:8003",
        "workers": 4,
        "timeout": 120,
        "graceful_timeout": 30,
        "keepalive": 5,
        "debug": True,
    }
    FlaskApplication(app, options).run()
