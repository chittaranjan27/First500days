"""
WhatsApp Chat Parser
Parses exported WhatsApp chat .txt files and extracts structured message data
"""

from datetime import datetime
from typing import List, Dict, Optional
import re


def parse_whatsapp_chat(text_content: str) -> List[Dict]:
    """
    Parse WhatsApp chat export text format
    
    Expected format examples:
    - [DD/MM/YYYY, HH:MM:SS AM/PM] Username: Message text
    - [DD/MM/YYYY, HH:MM:SS AM/PM] Username joined
    - [DD/MM/YYYY, HH:MM:SS AM/PM] Username left
    
    Handles:
    - Multiple date formats
    - Multiline messages
    - System messages (joined/left)
    - Different time formats
    """
    messages = []
    lines = text_content.split('\n')
    
    # Pattern to match WhatsApp message format
    # Supports formats like:
    # [DD/MM/YYYY, HH:MM:SS AM/PM] or [MM/DD/YYYY, HH:MM:SS AM/PM] (with brackets)
    # DD/MM/YYYY, HH:MM:SS AM/PM - (without brackets, with dash)
    # [DD/MM/YYYY, HH:MM:SS] (24-hour format)
    # Try bracket format first, then dash format
    date_pattern_brackets = r'\[(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\]\s*(.*)'
    date_pattern_dash = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}),\s*(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)\s*-\s*(.*)'
    
    current_message = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Try to match message header - first try bracket format, then dash format
        match = re.match(date_pattern_brackets, line)
        if not match:
            match = re.match(date_pattern_dash, line)
        
        if match:
            # Save previous message if exists
            if current_message:
                messages.append(current_message)
            
            # Extract groups - format depends on which pattern matched
            groups = match.groups()
            date_str = groups[0]
            time_str = groups[1]
            # For bracket format, remaining is in group 2, for dash format it's in group 2
            # But dash format already has remaining text in group 2, bracket needs extraction
            if len(groups) >= 3:
                remaining = groups[2].strip()
            else:
                remaining = line[match.end():].strip()
            
            # Parse date - try multiple formats
            date_obj = parse_date(date_str)
            if not date_obj:
                # Skip invalid date lines
                continue
            
            # Parse time
            time_obj = parse_time(time_str)
            if not time_obj:
                continue
            
            # Combine date and time
            timestamp = datetime.combine(date_obj, time_obj)
            
            # Check if it's a system message (joined/left)
            if 'joined' in remaining.lower() or 'left' in remaining.lower() or 'added' in remaining.lower():
                # Extract username from system message
                username = extract_username_from_system_message(remaining)
                messages.append({
                    'timestamp': timestamp,
                    'username': username,
                    'message': remaining,
                    'is_system': True,
                    'action': 'joined' if 'joined' in remaining.lower() or 'added' in remaining.lower() else 'left'
                })
                current_message = None
            else:
                # Regular user message
                # Format: Username: Message text
                colon_index = remaining.find(':')
                if colon_index > 0:
                    username = remaining[:colon_index].strip()
                    message_text = remaining[colon_index + 1:].strip()
                    
                    current_message = {
                        'timestamp': timestamp,
                        'username': username,
                        'message': message_text,
                        'is_system': False
                    }
                else:
                    # No colon found, might be continuation or malformed
                    current_message = None
        else:
            # Continuation of previous message (multiline)
            if current_message and not current_message.get('is_system'):
                current_message['message'] += '\n' + line
    
    # Add last message
    if current_message:
        messages.append(current_message)
    
    return messages


def parse_date(date_str: str) -> Optional[datetime.date]:
    """
    Parse date string in various formats
    Supports: DD/MM/YYYY, MM/DD/YYYY, DD-MM-YYYY, etc.
    """
    formats = [
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%d-%m-%Y',
        '%m-%d-%Y',
        '%d/%m/%y',
        '%m/%d/%y',
        '%Y/%m/%d',
        '%Y-%m-%d'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None


def parse_time(time_str: str) -> Optional[datetime.time]:
    """
    Parse time string in various formats
    Supports: HH:MM:SS AM/PM, HH:MM:SS, HH:MM AM/PM, HH:MM
    """
    formats = [
        '%I:%M:%S %p',  # 12-hour with seconds
        '%I:%M %p',     # 12-hour without seconds
        '%H:%M:%S',     # 24-hour with seconds
        '%H:%M'         # 24-hour without seconds
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str.strip(), fmt).time()
        except ValueError:
            continue
    
    return None


def extract_username_from_system_message(message: str) -> str:
    """
    Extract username from system messages like:
    - "John Doe joined"
    - "John Doe left"
    - "John Doe added you"
    """
    # Remove common system message keywords
    cleaned = message
    for keyword in ['joined', 'left', 'added', 'you', 'using', 'this', 'group']:
        cleaned = cleaned.replace(keyword, '')
    
    # Extract potential username (everything before keywords)
    parts = message.split()
    if len(parts) > 0:
        # Try to get username before action words
        action_words = ['joined', 'left', 'added', 'removed']
        username_parts = []
        for part in parts:
            if part.lower() in action_words:
                break
            username_parts.append(part)
        if username_parts:
            return ' '.join(username_parts)
    
    return cleaned.strip() or 'System'
