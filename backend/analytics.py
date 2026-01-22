"""
Analytics Computation Module
Computes metrics for the last 7 days from parsed WhatsApp messages
"""

from datetime import datetime, timedelta
from typing import List, Dict, Set
from collections import defaultdict


def compute_analytics(messages: List[Dict]) -> Dict:
    """
    Compute analytics for the last 7 days
    
    Returns:
    - daily_active_users: List of {date, active_users, new_users} for last 7 days
    - users_active_4plus_days: List of usernames active on 4+ days
    - summary: Overall statistics
    """
    if not messages:
        return get_empty_analytics()
    
    # Get current date (end of today)
    today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
    
    # Calculate date range (last 7 days including today)
    date_range = []
    for i in range(6, -1, -1):  # 6 days ago to today
        date = (today - timedelta(days=i)).date()
        date_range.append(date)
    
    # Filter messages from last 7 days
    seven_days_ago = today - timedelta(days=6)
    seven_days_ago = seven_days_ago.replace(hour=0, minute=0, second=0, microsecond=0)
    
    recent_messages = [
        msg for msg in messages
        if msg['timestamp'] >= seven_days_ago
    ]
    
    # Track active users per day
    daily_active_users = defaultdict(set)  # date -> set of usernames
    daily_new_users = defaultdict(set)     # date -> set of new users who joined
    
    # Track user activity across days
    user_activity_days = defaultdict(set)  # username -> set of dates active
    
    # Process messages
    for msg in recent_messages:
        msg_date = msg['timestamp'].date()
        
        # Skip if message is outside our 7-day window
        if msg_date not in date_range:
            continue
        
        username = msg.get('username', 'Unknown')
        
        if msg.get('is_system') and msg.get('action') == 'joined':
            # User joined the group
            daily_new_users[msg_date].add(username)
            daily_active_users[msg_date].add(username)
            user_activity_days[username].add(msg_date)
        elif not msg.get('is_system'):
            # Regular message from user
            daily_active_users[msg_date].add(username)
            user_activity_days[username].add(msg_date)
    
    # Build daily data structure
    daily_data = []
    for date in date_range:
        active_count = len(daily_active_users.get(date, set()))
        new_count = len(daily_new_users.get(date, set()))
        
        daily_data.append({
            'date': date.isoformat(),
            'date_display': date.strftime('%Y-%m-%d'),
            'active_users': active_count,
            'new_users': new_count
        })
    
    # Find users active on 4+ days
    users_active_4plus_days = [
        username for username, active_dates in user_activity_days.items()
        if len(active_dates) >= 4
    ]
    users_active_4plus_days.sort()
    
    # Calculate summary statistics
    total_active_users = len(user_activity_days)
    total_new_users = len(set(
        user for date_users in daily_new_users.values()
        for user in date_users
    ))
    avg_daily_active = sum(len(users) for users in daily_active_users.values()) / max(len(daily_data), 1)
    
    return {
        'daily_data': daily_data,
        'users_active_4plus_days': users_active_4plus_days,
        'summary': {
            'total_active_users': total_active_users,
            'total_new_users': total_new_users,
            'avg_daily_active_users': round(avg_daily_active, 1),
            'users_active_4plus_days_count': len(users_active_4plus_days)
        }
    }


def get_empty_analytics() -> Dict:
    """Return empty analytics structure when no messages found"""
    today = datetime.now().date()
    date_range = [(today - timedelta(days=i)).date() for i in range(6, -1, -1)]
    
    return {
        'daily_data': [
            {
                'date': date.isoformat(),
                'date_display': date.strftime('%Y-%m-%d'),
                'active_users': 0,
                'new_users': 0
            }
            for date in date_range
        ],
        'users_active_4plus_days': [],
        'summary': {
            'total_active_users': 0,
            'total_new_users': 0,
            'avg_daily_active_users': 0,
            'users_active_4plus_days_count': 0
        }
    }
