from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.json["msg"].lower()

    # Simple rule-based replies
    if "hello" in user_msg or "hi" in user_msg:
        reply = "Hey there! 👋 Ready for your workout?"
    elif "workout" in user_msg:
        reply = "I can suggest Push-Pull-Legs, Full Body, or Cardio. 💪 Which one do you want?"
    elif "diet" in user_msg:
        reply = "For muscle gain: eat high protein 🥩🍳. For fat loss: focus on calorie deficit 🥗."
    elif "help" in user_msg:
        reply = "You can ask me about workouts, diet, or motivation! 🔥"
    else:
        reply = "I’m still learning 🤖. Try asking me about workouts, diet, or help."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
