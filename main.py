from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = openai.ChatCompletion.create(
          model="gpt-4",  # Assuming GPT-4 is the model you're using
          messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'message': response['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)