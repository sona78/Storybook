from flask import Flask, render_template, jsonify
from db import create_combined_prompt, setup_database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/combined-prompt')
def get_combined_prompt():
    try:
        prompt = create_combined_prompt()
        return jsonify({'prompt': prompt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    setup_database()
    app.run(debug=True, host='0.0.0.0', port=5000) 