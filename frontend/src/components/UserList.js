import React from 'react';
import './UserList.css';

const UserList = ({ users }) => {
  if (!users || users.length === 0) {
    return (
      <div className="user-list">
        <h2>Most Active Users</h2>
        <div className="empty-state">
          <p>No users were active on 4 or more days in the last 7 days.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="user-list">
      <h2>Most Active Users</h2>
      <p className="list-description">
        Users who were active on at least 4 different days in the last 7 days:
      </p>
      <div className="users-grid">
        {users.map((user, index) => (
          <div key={index} className="user-card">
            <div className="user-avatar">
              {user.charAt(0).toUpperCase()}
            </div>
            <div className="user-name">{user}</div>
            <div className="user-badge">Active 4+ Days</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default UserList;
