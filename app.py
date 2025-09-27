# app.py
from flask import Flask, render_template, request, jsonify
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Compatibility: try to use new OpenAI client (v1+), else fall back to classic 'openai' usage.
USE_NEW_OPENAI = False
openai_client = None
openai_version = None

def detect_openai():
    global USE_NEW_OPENAI, openai_client, openai_version
    try:
        # try new v1 client
        from openai import OpenAI
        import importlib.metadata as imd
        try:
            openai_version = imd.version('openai')
        except Exception:
            openai_version = "unknown"
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            openai_client = OpenAI(api_key=api_key)
        else:
            # still create client without explicit api_key - OpenAI will read env var
            openai_client = OpenAI()
        USE_NEW_OPENAI = True
        app.logger.info(f"Using new OpenAI client (v1+). openai version={openai_version}")
        return
    except Exception as e_new:
        app.logger.info("New OpenAI client not available or failed: %s", e_new)

    # fallback to classic openai
    try:
        import openai
        import importlib.metadata as imd
        try:
            openai_version = imd.version('openai')
        except Exception:
            openai_version = "unknown"
        openai.api_key = os.getenv("OPENAI_API_KEY")
        openai_client = openai
        USE_NEW_OPENAI = False
        app.logger.info(f"Using classic openai client. openai version={openai_version}")
        return
    except Exception as e_old:
        app.logger.error("No openai package available: %s", e_old)
        openai_version = None
        openai_client = None
        USE_NEW_OPENAI = False

# detect on startup
detect_openai()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health")
def health():
    return {
        "status": "ok",
        "openai_version": openai_version,
        "using_new_openai_client": USE_NEW_OPENAI,
        "openai_api_key_set": bool(os.getenv("OPENAI_API_KEY"))
    }

def ask_openai(prompt: str, max_tokens: int = 200, temp: float = 0.7):
    """Unified wrapper that works with both old and new SDKs."""
    if openai_client is None:
        raise RuntimeError("OpenAI client not available. Set OPENAI_API_KEY and install openai package.")

    if USE_NEW_OPENAI:
        # new client (openai>=1.0.0)
        resp = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Gym Assistant who gives short, friendly workout, diet and booking help. Keep answers actionable and concise."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temp
        )
        # new response object -> choices[0].message.content
        return resp.choices[0].message.content.strip()
    else:
        # classic openai (openai==0.28.x etc.)
        # uses openai.ChatCompletion.create
        resp = openai_client.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Gym Assistant who gives short, friendly workout, diet and booking help. Keep answers actionable and concise."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temp
        )
        return resp.choices[0].message['content'].strip()

@app.route("/get", methods=["POST"])
def get_bot_response():
    data = request.get_json(force=True) or {}
    user_message = data.get("message") or data.get("msg") or ""
    user_message = user_message.strip()
    if not user_message:
        return jsonify({"reply": "Please type a message."})

    # Quick local intents for very common questions (fast & saves tokens)
    low = user_message.lower()
    if any(w in low for w in ["plan", "pricing", "price", "membership"]):
        return jsonify({"reply": "We offer monthly, quarterly and yearly plans. Type 'plans' for details or 'book' to request a free trial."})
    if any(w in low for w in ["book", "trial", "free trial"]):
        return jsonify({"reply": "To book a free trial please click Book Trial (or type: Name: <your name>, Time: YYYY-MM-DD HH:MM)."})
    # Otherwise call AI
    try:
        reply = ask_openai(user_message)
        return jsonify({"reply": reply})
    except Exception as e:
        app.logger.error("OpenAI call failed: %s", e, exc_info=True)
        # Safe fallback
        fallback = "Sorry — I couldn't reach the AI service right now. Please try again later or type 'book' to request a trial."
        return jsonify({"reply": f"⚠️ Error: {str(e)}\n\nFallback: {fallback}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
