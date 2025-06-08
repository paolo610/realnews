from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import csv
import secrets
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verify_key(username, key):
    try:
        with open('data/users.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 2 and row[0].strip() == username.strip() and row[1].strip() == key.strip():
                    return True
    except FileNotFoundError:
        return False
    return False

@app.route('/')
def index():
    posts = []
    try:
        with open('data/posts.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            posts = list(reader)
    except FileNotFoundError:
        pass
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def create_post():
    username = request.form.get('username')
    key = request.form.get('key')
    content = request.form.get('content')
    
    if not verify_key(username, key):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    image_path = None
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f"uploads/{filename}"
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post_data = [timestamp, username, content, image_path]
    
    with open('data/posts.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(post_data)
    
    return jsonify({'success': True})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Add a 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', posts=[]), 404

if __name__ == '__main__':
    # Use environment variable for port if available (for GitHub Pages)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 