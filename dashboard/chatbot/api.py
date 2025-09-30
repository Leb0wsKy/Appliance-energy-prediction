from flask import Flask, request, jsonify
from flask_cors import CORS
from quuery import rag_query

app = Flask(__name__)
CORS(app)  # autorise toutes les origines et méthodes

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("question", "")
    answer = rag_query(question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
