# Project Structure:
# .
# ├── app.py
# ├── Fbook/
# │   ├── index.html
# │   └── libraryTable.html
# ├── uploads/
# └── library/

# =============================
# app.py (Flask server)
# =============================

from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
import os
import subprocess
import time
from flask_cors import CORS

app = Flask(__name__, static_folder='Fbook')
CORS(app)

UPLOAD_FOLDER = 'uploads'
LIBRARY_FOLDER = 'Fbook/FbookLibrary'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/uploads', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    with open("log.txt", "a") as f:
       print("File", file.filename, file=f, flush=True)
    filepath = os.path.join(UPLOAD_FOLDER, 'input_file.txt')
    file.save(filepath)
    try:
        subprocess.run(
            ['/usr/local/bin/python3.10', 'Fbook/buildUserChapter.py', file.filename],
            check=True
        )
        time.sleep(2)
        return redirect(url_for('serve_static', filename='index.html'))
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/select-library-chapter', methods=['POST'])
def select_library_chapter():
    data = request.get_json()
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400

    source_path = os.path.join(LIBRARY_FOLDER, filename)
    target_path = os.path.join(UPLOAD_FOLDER, 'input_file.txt')

    if not os.path.exists(source_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        with open(source_path, 'r') as src, open(target_path, 'w') as dst:
            dst.write(src.read())

        subprocess.run(
            ['/usr/local/bin/python3.10', 'Fbook/buildUserChapter.py', filename],
            #['/usr/local/bin/python3.10', 'Fbook/buildUserChapter.py', '/uploads'],
            check=True
        )

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run-script')
def run_script():
    param1 = request.args.get('param1', 'default1')
    param2 = request.args.get('param2', 'default2')
    try:
        result = subprocess.run(
            ['/usr/local/bin/python3.10', '/Users/paologiommi/Fbook/openai4Fbook.py', param1, param2],
            capture_output=True,
            text=True,
            env=os.environ  # includes OPENAI_API_KEY if needed
        )
        output = result.stdout.strip()
        error = result.stderr.strip()
        if error:
            print("⚠️ Script stderr:", error)
        return output
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(port=5000, debug=True)


