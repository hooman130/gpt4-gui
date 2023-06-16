"""
This module contains a Flask application that uses OpenAI's GPT-4 model to chat with users.
"""

import os
import json
from flask import Flask, request, jsonify, render_template, Response
from gunicorn.app.base import BaseApplication
import openai


class FlaskApplication(BaseApplication):
    """
    A custom Gunicorn application that wraps the Flask application.
    """

    def __init__(self, app, options=None):
        """
        Initializes the FlaskApplication object.

        Args:
            app (Flask): The Flask application object.
            options (dict): A dictionary of Gunicorn options.
        """
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        """
        Loads the Gunicorn configuration.
        """
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """
        Loads the Flask application.
        """
        return self.application


app = Flask(__name__)
"""
The Flask application object.
"""

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET"])
def home():
    """
    Renders the home page.
    """
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handles chat requests from the user.

    Returns:
        Response: A Flask Response object containing the chat response.
    """
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    def generate():
        """
        Generates the chat response using OpenAI's GPT-4 model.

        Yields:
            str: A string containing the chat response.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",  # Assuming GPT-4 is the model you're using
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=4096,
                stream=True,
                temprature=0.4,
            )
            # Format the response message
            for message in response:
                response_message = message["choices"][0]["y"]
                response_message = response_message.replace(". ", ".<br>")
                yield f"data: {json.dumps({'message': response_message})}\n\n"

        except Exception as error:
            yield f"data: {json.dumps({'error': str(error)})}\n\n"

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(
        debug=True,
    )

    """ options = {
        "bind": "0.0.0.0:8001",
        "workers": 4,
        "timeout": 120,
        "graceful_timeout": 30,
        "keepalive": 5,
        "debug": True,
    }
    FlaskApplication(app, options).run() """
