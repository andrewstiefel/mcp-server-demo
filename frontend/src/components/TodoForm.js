import React, { useState } from 'react';
import './TodoForm.css';

function TodoForm({ onAddTodo }) {
  const [title, setTitle] = useState('');
  const [expirationDate, setExpirationDate] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!title.trim()) return;
    
    onAddTodo(title, expirationDate || null);
    setTitle('');
    setExpirationDate('');
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <input
          type="text"
          className="todo-input"
          placeholder="What needs to be done?"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>
      
      <div className="form-group">
        <input
          type="date"
          className="date-input"
          value={expirationDate}
          onChange={(e) => setExpirationDate(e.target.value)}
          min={new Date().toISOString().split('T')[0]}
        />
      </div>
      
      <button type="submit" className="add-button">
        Add Todo
      </button>
    </form>
  );
}

export default TodoForm;

