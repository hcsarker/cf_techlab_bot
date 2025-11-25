import sqlite3
import json
from datetime import datetime
import os

DATABASE_PATH = 'chatbot_feedback.db'

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create user_info table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT,
            session_id TEXT UNIQUE NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create conversations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            intent_tag TEXT,
            confidence REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            session_id TEXT,
            ip_address TEXT,
            FOREIGN KEY (session_id) REFERENCES user_info (session_id)
        )
    ''')
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            feedback_type TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    ''')
    
    # Create index for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_confidence ON conversations(confidence)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON conversations(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_feedback_type ON feedback(feedback_type)')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def save_user_info(name, mobile, email, session_id):
    """Save user information"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO user_info (name, mobile, email, session_id)
            VALUES (?, ?, ?, ?)
        ''', (name, mobile, email, session_id))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Session ID already exists
        conn.close()
        return False

def get_user_info(session_id):
    """Get user information by session ID"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, mobile, email, timestamp
        FROM user_info
        WHERE session_id = ?
    ''', (session_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'name': row[0],
            'mobile': row[1],
            'email': row[2],
            'timestamp': row[3]
        }
    return None

def log_conversation(user_message, bot_response, intent_tag, confidence, session_id=None, ip_address=None):
    """Log a conversation to the database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO conversations (user_message, bot_response, intent_tag, confidence, session_id, ip_address)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_message, bot_response, intent_tag, confidence, session_id, ip_address))
    
    conversation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return conversation_id

def add_feedback(conversation_id, feedback_type):
    """Add feedback for a conversation"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO feedback (conversation_id, feedback_type)
        VALUES (?, ?)
    ''', (conversation_id, feedback_type))
    
    conn.commit()
    conn.close()
    
    return True

def get_low_confidence_conversations(threshold=0.7, limit=50):
    """Get conversations with low confidence scores"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.id, c.user_message, c.bot_response, c.intent_tag, c.confidence, c.timestamp,
               f.feedback_type, u.name, u.mobile, u.email
        FROM conversations c
        LEFT JOIN feedback f ON c.id = f.conversation_id
        LEFT JOIN user_info u ON c.session_id = u.session_id
        WHERE c.confidence < ?
        ORDER BY c.confidence ASC, c.timestamp DESC
        LIMIT ?
    ''', (threshold, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row[0],
            'user_message': row[1],
            'bot_response': row[2],
            'intent_tag': row[3],
            'confidence': row[4],
            'timestamp': row[5],
            'feedback': row[6],
            'user_name': row[7],
            'user_mobile': row[8],
            'user_email': row[9]
        }
        for row in rows
    ]

def get_negative_feedback_conversations(limit=50):
    """Get conversations with negative feedback"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.id, c.user_message, c.bot_response, c.intent_tag, c.confidence, c.timestamp,
               u.name, u.mobile, u.email
        FROM conversations c
        JOIN feedback f ON c.id = f.conversation_id
        LEFT JOIN user_info u ON c.session_id = u.session_id
        WHERE f.feedback_type = 'negative'
        ORDER BY c.timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row[0],
            'user_message': row[1],
            'bot_response': row[2],
            'intent_tag': row[3],
            'confidence': row[4],
            'timestamp': row[5],
            'user_name': row[6],
            'user_mobile': row[7],
            'user_email': row[8]
        }
        for row in rows
    ]

def get_all_conversations(limit=100):
    """Get all recent conversations with user info"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.id, c.user_message, c.bot_response, c.intent_tag, c.confidence, c.timestamp,
               f.feedback_type, u.name, u.mobile, u.email, c.session_id
        FROM conversations c
        LEFT JOIN feedback f ON c.id = f.conversation_id
        LEFT JOIN user_info u ON c.session_id = u.session_id
        ORDER BY c.timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row[0],
            'user_message': row[1],
            'bot_response': row[2],
            'intent_tag': row[3],
            'confidence': row[4],
            'timestamp': row[5],
            'feedback': row[6],
            'user_name': row[7],
            'user_mobile': row[8],
            'user_email': row[9],
            'session_id': row[10]
        }
        for row in rows
    ]

def get_all_users(limit=100):
    """Get all registered users"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.id, u.name, u.mobile, u.email, u.session_id, u.timestamp,
               COUNT(c.id) as conversation_count
        FROM user_info u
        LEFT JOIN conversations c ON u.session_id = c.session_id
        GROUP BY u.id
        ORDER BY u.timestamp DESC
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            'id': row[0],
            'name': row[1],
            'mobile': row[2],
            'email': row[3],
            'session_id': row[4],
            'timestamp': row[5],
            'conversation_count': row[6]
        }
        for row in rows
    ]

def get_statistics():
    """Get overall statistics"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Total conversations
    cursor.execute('SELECT COUNT(*) FROM conversations')
    total_conversations = cursor.fetchone()[0]
    
    # Average confidence
    cursor.execute('SELECT AVG(confidence) FROM conversations')
    avg_confidence = cursor.fetchone()[0] or 0
    
    # Positive feedback count
    cursor.execute("SELECT COUNT(*) FROM feedback WHERE feedback_type = 'positive'")
    positive_feedback = cursor.fetchone()[0]
    
    # Negative feedback count
    cursor.execute("SELECT COUNT(*) FROM feedback WHERE feedback_type = 'negative'")
    negative_feedback = cursor.fetchone()[0]
    
    # Low confidence conversations
    cursor.execute('SELECT COUNT(*) FROM conversations WHERE confidence < 0.7')
    low_confidence_count = cursor.fetchone()[0]
    
    # Total users
    cursor.execute('SELECT COUNT(*) FROM user_info')
    total_users = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_conversations': total_conversations,
        'total_users': total_users,
        'average_confidence': round(avg_confidence, 4),
        'positive_feedback': positive_feedback,
        'negative_feedback': negative_feedback,
        'low_confidence_count': low_confidence_count,
        'feedback_rate': round((positive_feedback + negative_feedback) / total_conversations * 100, 2) if total_conversations > 0 else 0
    }

def export_training_data():
    """Export conversations for retraining"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Get conversations with positive feedback or high confidence
    cursor.execute('''
        SELECT DISTINCT c.user_message, c.intent_tag
        FROM conversations c
        LEFT JOIN feedback f ON c.id = f.conversation_id
        WHERE c.confidence > 0.8 OR f.feedback_type = 'positive'
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Group by intent
    training_data = {}
    for message, tag in rows:
        if tag not in training_data:
            training_data[tag] = []
        if message not in training_data[tag]:
            training_data[tag].append(message)
    
    return training_data

if __name__ == '__main__':
    # Initialize database when run directly
    init_db()
