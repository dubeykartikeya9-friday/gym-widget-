from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# ✅ Load OpenAI key from Render Environment Variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"response": "⚠️ No message received."})

    try:
        # ✅ Using correct ChatCompletion call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message["content"].strip()
        return jsonify({"response": bot_reply})

    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
