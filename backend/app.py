from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# In-memory storage for todos
todos = []

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
    
    todo = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'expiration_date': data.get('expiration_date', None),
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)

