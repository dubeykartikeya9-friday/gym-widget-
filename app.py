from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    user_message = request.json.get("message")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Free/cheap and good
            messages=[
                {"role": "system", "content": "You are a helpful Gym Assistant who gives workout, diet, and motivation advice in a friendly way."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.7
        )

        bot_reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})
