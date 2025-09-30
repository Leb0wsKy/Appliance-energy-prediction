from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

GROQ_API_TOKEN = os.environ.get("GROQ_API_TOKEN")
GROQ_API_URL = os.environ.get("GROQ_API_URL")

client = Groq(api_key=GROQ_API_TOKEN)

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question manquante"}), 400

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un ingénieur électricien expérimenté. "
                        "Réponds toujours aux questions sur l'électricité de façon claire, concise et simple. "
                        
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,  # un peu plus stable et précis
            max_completion_tokens=200,  # limite la longueur de la réponse
            top_p=1,
            reasoning_effort="medium",
            stream=False
        )

        answer = completion.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        print("Erreur GROQ :", str(e))
        return jsonify({"error": "Erreur serveur"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
