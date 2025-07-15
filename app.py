from flask import Flask, render_template, jsonify, send_from_directory
import os
from db import create_combined_prompt, setup_database

app = Flask(__name__, static_folder='frontend/build', static_url_path='')

@app.route('/api/combined-prompt')
def get_combined_prompt():
    try:
        prompt = create_combined_prompt()
        return jsonify({'prompt': prompt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve React static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    static_folder = app.static_folder or 'frontend/build'
    if path != "" and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    else:
        return send_from_directory(static_folder, 'index.html')

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, host='0.0.0.0', port=5000) 