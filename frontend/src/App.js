import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserForm from './UserForm';
import UserEditForm from './UserEditForm'; // Import the new edit form

function App() {
  const [users, setUsers] = useState([]);
  // --- New state to track which user is being edited ---
  const [editingUserId, setEditingUserId] = useState(null);

  const fetchUsers = () => {
    axios.get('http://localhost:8080/users')
      .then(response => {
        setUsers(response.data);
      })
      .catch(error => {
        console.error('Error fetching users:', error);
      });
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleUserCreated = () => {
    fetchUsers();
  };

  const handleUserDeleted = (userId) => {
    axios.delete(`http://localhost:8080/users/${userId}`)
      .then(() => {
        console.log(`User ${userId} deleted.`);
        fetchUsers();
      })
      .catch(error => {
        console.error(`Error deleting user ${userId}:`, error);
      });
  };

  // --- New Save Handler for Updates ---
  const handleUserUpdated = (userId, updatedData) => {
    // Make a PUT request to update the user
    axios.put(`http://localhost:8080/users/${userId}`, updatedData)
      .then(() => {
        console.log(`User ${userId} updated.`);
        setEditingUserId(null); // Exit edit mode
        fetchUsers(); // Refresh the user list
      })
      .catch(error => {
        console.error(`Error updating user ${userId}:`, error);
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>User Management</h1>
      </header>

      <UserForm onUserCreated={handleUserCreated} />

      <div className="user-list">
        <h2>All Users</h2>
        <ul>
          {users.map(user => (
            <li key={user.id}>
              {
                // --- Conditional Rendering Logic ---
                
                editingUserId === user.id ? (
                  <UserEditForm
                    user={user}
                    onSave={handleUserUpdated}
                    onCancel={() => setEditingUserId(null)} 
                  />
                ) : (
                  
                  <div>
                    {user.username} - ({user.email})
                    <button onClick={() => setEditingUserId(user.id)} style={{ marginLeft: '10px' }}>
                      Edit
                    </button>
                    <button onClick={() => handleUserDeleted(user.id)} style={{ marginLeft: '10px' }}>
                      Delete
                    </button>
                  </div>
                )
              }
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
