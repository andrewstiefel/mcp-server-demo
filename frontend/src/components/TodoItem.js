import React from 'react';
import './TodoItem.css';

function TodoItem({ todo, onDelete, onToggleComplete }) {
  const formatDate = (dateString) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const isExpired = (dateString) => {
    if (!dateString) return false;
    return new Date(dateString) < new Date();
  };

  const expired = isExpired(todo.expiration_date);

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''} ${expired ? 'expired' : ''}`}>
      <div className="todo-content">
        <input
          type="checkbox"
          className="todo-checkbox"
          checked={todo.completed}
          onChange={() => onToggleComplete(todo.id)}
        />
        
        <div className="todo-details">
          <span className="todo-title">{todo.title}</span>
          {todo.expiration_date && (
            <span className="todo-date">
              {expired ? '⚠️ ' : '📅 '}
              {formatDate(todo.expiration_date)}
              {expired && ' (Expired)'}
            </span>
          )}
          {todo.image && (
            <div className="todo-image-container">
              <img 
                src={`http://localhost:5000/api/images/${todo.image}`} 
                alt="Todo attachment" 
                className="todo-image"
              />
            </div>
          )}
        </div>
      </div>
      
      <button
        className="delete-button"
        onClick={() => onDelete(todo.id)}
        aria-label="Delete todo"
      >
        🗑️
      </button>
    </div>
  );
}

export default TodoItem;

