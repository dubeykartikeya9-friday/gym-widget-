import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

# Load API key from Render environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_ai(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful gym assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Sorry, I couldn’t reach the AI service. Error: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    data = request.get_json()
    user_input = data.get("message")
    reply = chat_with_ai(user_input)
    return jsonify({"response": reply})

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "openai_api_key_set": bool(os.getenv("OPENAI_API_KEY")),
        "using_openai": True
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
