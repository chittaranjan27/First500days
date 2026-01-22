import React from 'react';
import './AnalyticsSummary.css';

const AnalyticsSummary = ({ summary }) => {
  if (!summary) return null;

  const stats = [
    {
      label: 'Total Active Users',
      value: summary.total_active_users,
      icon: '👥',
      color: '#2196f3'
    },
    {
      label: 'New Users (Last 7 Days)',
      value: summary.total_new_users,
      icon: '🆕',
      color: '#ff9800'
    },
    {
      label: 'Avg Daily Active Users',
      value: summary.avg_daily_active_users,
      icon: '📊',
      color: '#4caf50'
    },
    {
      label: 'Users Active 4+ Days',
      value: summary.users_active_4plus_days_count,
      icon: '⭐',
      color: '#9c27b0'
    }
  ];

  return (
    <div className="analytics-summary">
      <h2>Analytics Summary</h2>
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <div key={index} className="stat-card" style={{ borderTopColor: stat.color }}>
            <div className="stat-icon">{stat.icon}</div>
            <div className="stat-value">{stat.value}</div>
            <div className="stat-label">{stat.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AnalyticsSummary;
