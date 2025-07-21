from flask import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS
from prompt_of_the_day import getPromptOfTheDay
from db import get_storybook
from datetime import datetime, timezone

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)  # Enable CORS for all routes

@app.route('/api/storybook')
def get_full_storybook():
    try:
        current_datetime = datetime.now(timezone.utc)
        storybook = get_storybook()
        potd = getPromptOfTheDay(current_datetime)

        return jsonify({'title': potd['title'], 'prompt': potd['prompt'], 'story': storybook})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    # Run on port 5000 for API access from React dev server
    app.run(debug=True, host='0.0.0.0', port=5000) 