import React, { useState } from 'react';

// This form takes the user to be edited and functions to call on save/cancel
function UserEditForm({ user, onSave, onCancel }) {
  
  const [username, setUsername] = useState(user.username);
  const [email, setEmail] = useState(user.email);

  const handleSave = (event) => {
    event.preventDefault();
    
    onSave(user.id, { username, email });
  };

  return (
    <form onSubmit={handleSave}>
      <h4>Editing: {user.username}</h4>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      {/* The Save button triggers the save handler */}
      <button type="submit">Save</button>
      {/* The Cancel button simply calls the onCancel function passed from App.js */}
      <button type="button" onClick={onCancel} style={{ marginLeft: '10px' }}>
        Cancel
      </button>
    </form>
  );
}

export default UserEditForm;
