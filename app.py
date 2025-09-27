from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Load environment variables (future ready)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")   # for AI responses
DATABASE_URL = os.getenv("DATABASE_URL")       # for saving leads/bookings
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")     # for email notifications

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Simple placeholder response (replace with AI later)
    if user_message:
        response = f"Hello! You said: {user_message}. (Gym bot here 💪)"
    else:
        response = "Hi! I'm your Gym Assistant. Ask me about plans, trainers, or bookings."

    return jsonify({"reply": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render needs this
    app.run(host="0.0.0.0", port=port)
