import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to the JSON file
DB_FILE = 'db.json'

# Load articles from the JSON file
def load_articles():
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('articles', [])  # Ensure it returns a list of articles
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
    except json.JSONDecodeError:
        return []  # Return an empty list if the file is malformed

# Save articles to the JSON file
def save_articles(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump({'articles': data}, f, ensure_ascii=False, indent=4)

# Initialize articles from the file
articles = load_articles()

@app.route('/data', methods=['GET'])
def get_articles():
    return jsonify(articles)

@app.route('/data', methods=['POST'])
def add_article():
    article = request.json
    if not article:
        return jsonify({"message": "Invalid data"}), 400
    # Check for duplicate articles by Title
    if not any(a['Title'] == article.get('Title') for a in articles):
        articles.append(article)
        save_articles(articles)  # Save updated articles to file
        return jsonify(article), 201
    return jsonify({"message": "Article already exists"}), 409

if __name__ == '__main__':
    app.run(debug=True)
