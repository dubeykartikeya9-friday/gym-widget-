from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)

# Home route → loads chatbot UI
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot endpoint
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Simple bot logic (replace with OpenAI API later)
    if "plan" in user_message.lower():
        bot_response = "We offer monthly, quarterly, and yearly gym plans. Would you like details?"
    elif "trainer" in user_message.lower():
        bot_response = "We have certified trainers available. Do you want to book a free session?"
    else:
        bot_response = "Welcome to our Gym! 💪 Ask me about memberships, trainers, or book a trial session."

    return jsonify({"reply": bot_response})

# Booking endpoint
@app.route("/api/book", methods=["POST"])
def book():
    data = request.get_json()
    name = data.get("name")
    phone = data.get("phone")

    # Forward booking to Google Apps Script (if set)
    webhook_url = os.getenv("SHEET_WEBHOOK_URL")
    secret = os.getenv("SHEET_SECRET")

    if webhook_url and secret:
        try:
            requests.post(webhook_url, json={
                "name": name,
                "phone": phone,
                "secret": secret
            })
        except:
            pass  # Ignore failures

    return jsonify({"status": "success", "message": f"Booking received for {name} 📅"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
