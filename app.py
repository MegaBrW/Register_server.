from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GIST_ID = os.getenv('GIST_ID')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Missing username or password'}), 400

    gist_url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(gist_url, headers=headers)

    if response.status_code != 200:
        return jsonify({'success': False, 'error': 'Failed to access Gist'}), 500

    gist_data = response.json()
    login_data = gist_data['files']['login_data.txt']['content']

    if f'{username}:' in login_data:
        return jsonify({'success': False, 'error': 'Username already exists'}), 400

    new_login_data = login_data + f'\n{username}:{password}'
    payload = {
        "files": {
            "login_data.txt": {
                "content": new_login_data
            }
        }
    }

    response = requests.patch(gist_url, headers=headers, json=payload)

    if response.status_code == 200:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Failed to update Gist'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
