from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from datetime import datetime
import uuid
import os
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

# In-memory storage for todos
todos = []

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """Get all todos"""
    return jsonify(todos), 200

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """Create a new todo"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    todo_id = str(uuid.uuid4())
    image_filename = None
    
    # Handle image upload if provided
    if 'image' in data and data['image']:
        try:
            # Extract base64 image data
            image_data = data['image']
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode and save image
            image_bytes = base64.b64decode(image_data)
            image_filename = f"{todo_id}.jpg"
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
        except Exception as e:
            return jsonify({'error': f'Failed to process image: {str(e)}'}), 400
    
    todo = {
        'id': todo_id,
        'title': data['title'],
        'expiration_date': data.get('expiration_date', None),
        'image': image_filename,
        'created_at': datetime.now().isoformat(),
        'completed': False
    }
    
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/api/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo by id"""
    global todos
    initial_length = len(todos)
    
    # Find the todo to get the image filename
    todo_to_delete = next((todo for todo in todos if todo['id'] == todo_id), None)
    
    # Delete the image file if it exists
    if todo_to_delete and todo_to_delete.get('image'):
        image_path = os.path.join(UPLOAD_FOLDER, todo_to_delete['image'])
        if os.path.exists(image_path):
            os.remove(image_path)
    
    todos = [todo for todo in todos if todo['id'] != todo_id]
    
    if len(todos) == initial_length:
        return jsonify({'error': 'Todo not found'}), 404
    
    return jsonify({'message': 'Todo deleted successfully'}), 200

@app.route('/api/todos/<todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    """Update a todo's completed status"""
    data = request.get_json()
    
    for todo in todos:
        if todo['id'] == todo_id:
            if 'completed' in data:
                todo['completed'] = data['completed']
            return jsonify(todo), 200
    
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/images/<filename>', methods=['GET'])
def get_image(filename):
    """Serve an uploaded image"""
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpeg')
    return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(debug=False, port=5000)

