from flask import Flask, request, jsonify
from rake_nltk import Rake

app = Flask(__name__)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    data = request.get_json()
    transcript = data['transcript']

    # Define keywords to highlight
    keywords_to_highlight = ["graining", "degradation", "pit window", "box", "traffic", "clear air"]

    # Initialize RAKE
    rake = Rake()

    # Extract keywords from text
    rake.extract_keywords_from_text(transcript)
    keyword_ranked_phrases = rake.get_ranked_phrases()

    # Check for keywords and highlight them
    found_keywords = [word for word in keywords_to_highlight if word in transcript.lower()]

    return jsonify({keyword: transcript.count(keyword) for keyword in found_keywords})

if __name__ == '__main__':
    app.run(port=5000)