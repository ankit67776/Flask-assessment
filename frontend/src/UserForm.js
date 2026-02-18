import React, { useState } from 'react';
import axios from 'axios';


function UserForm({ onUserCreated }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();

    // The data we want to send to the API
    const newUser = { username, email };

    // Make the POST request
    axios.post('http://localhost:8080/users', newUser)
      .then(response => {
        console.log('User created:', response.data);
        // Clear the form fields
        setUsername('');
        setEmail('');
        // Call the function passed from the parent to trigger a refresh
        onUserCreated();
      })
      .catch(error => {
        console.error('Error creating user:', error);
      });
  };

  return (
    <div className="user-form">
      <h2>Create New User</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit">Create User</button>
      </form>
    </div>
  );
}

export default UserForm;
