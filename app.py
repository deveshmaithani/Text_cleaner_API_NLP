from flask import Flask, request, jsonify
from text_cleaner import TextCleaner

app = Flask(__name__)
cleaner = TextCleaner()

@app.route("/clean", methods=["POST"])
def clean_text():
    data = request.get_json()
    paragraph = data.get("text", "")

    cleaned = cleaner.clean(paragraph)
    return jsonify({"cleaned_sentences": cleaned})

if __name__ == "__main__":
    app.run(debug=True)