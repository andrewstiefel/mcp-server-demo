import React, { useState } from 'react';
import './TodoForm.css';

function TodoForm({ onAddTodo }) {
  const [title, setTitle] = useState('');
  const [expirationDate, setExpirationDate] = useState('');
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Check if file is an image
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
      }
      
      // Check file size (limit to 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('Image size must be less than 5MB');
        return;
      }

      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setImage(null);
    setImagePreview(null);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!title.trim()) return;
    
    onAddTodo(title, expirationDate || null, image);
    setTitle('');
    setExpirationDate('');
    setImage(null);
    setImagePreview(null);
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

      <div className="form-group">
        <label className="image-label">
          📷 Add Image
          <input
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            style={{ display: 'none' }}
          />
        </label>
        {imagePreview && (
          <div className="image-preview-container">
            <img 
              src={imagePreview} 
              alt="Preview" 
              className="image-preview"
            />
            <button 
              type="button" 
              onClick={removeImage} 
              className="remove-image-btn"
            >
              ✕
            </button>
          </div>
        )}
      </div>
      
      <button type="submit" className="add-button">
        Add Todo
      </button>
    </form>
  );
}

export default TodoForm;

