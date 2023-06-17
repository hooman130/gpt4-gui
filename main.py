"""
This module contains a Flask application that uses OpenAI's GPT-4 model to chat with users.
"""
import os
import markdown
from flask import Flask, request, jsonify, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap
from gunicorn.app.base import BaseApplication
import openai
import logging

logging.basicConfig(level=logging.DEBUG)


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
Bootstrap(app)
"""
The Flask application object.
"""

class MessageForm(FlaskForm):
  message = StringField('Message')
  submit = SubmitField('Send')

openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=["GET"])
def home():
    """
    Renders the home page.
    """
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.get_json().get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",  # Assuming GPT-4 is the model you're using
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=2048,
            temperature=0.5,
            # stream=True,
        )
        # Format the response message
        response_message = response["choices"][0]["message"]["content"]
        response_message = markdown.markdown(response_message)
        # logging.debug(response_message)
        # response_message = response_message.replace(". ", ".<br>")
        return jsonify({"message": response_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5006)

"""     options = {
        "bind": "0.0.0.0:8001",
        "workers": 4,
        "timeout": 120,
        "graceful_timeout": 30,
        "keepalive": 5,
        "debug": True,
    }

    FlaskApplication(app, options).run() """
