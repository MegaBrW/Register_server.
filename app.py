from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://megabrw.github.io"}})

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GIST_ID = '972e50b39619c7a851a78aea17bdb6bd'

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    gist_url = f'https://api.github.com/gists/{GIST_ID}'
    gist_response = requests.get(gist_url, headers=headers)
    
    if gist_response.status_code != 200:
        return jsonify({"error": "Failed to access Gist"}), 500

    gist_data = gist_response.json()
    login_data = gist_data['files']['login_data.txt']['content']

    if f'{username}:' in login_data:
        return jsonify({"error": "Username already exists"}), 400

    new_login_data = login_data + f'\n{username}:{password}'
    
    update_response = requests.patch(gist_url, headers=headers, json={
        "files": {
            "login_data.txt": {
                "content": new_login_data
            }
        }
    })
    
    if update_response.status_code == 200:
        return jsonify({"message": "Registration successful"}), 200
    else:
        return jsonify({"error": "Failed to update Gist"}), 500

if __name__ == '__main__':
    app.run(debug=True)
