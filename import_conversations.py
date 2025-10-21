#!/usr/bin/env python3
"""
Import Claude and ChatGPT conversations into the memory MCP database.
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Any
import uuid
import hashlib

def create_database(db_path: str):
    """Create the memory database with required tables."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create memories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSON
        )
    ''')
    
    # Create conversations table for better organization
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            title TEXT,
            source TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            metadata JSON
        )
    ''')
    
    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT,
            role TEXT,
            content TEXT,
            created_at TIMESTAMP,
            metadata JSON,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    ''')
    
    conn.commit()
    return conn

def import_claude_conversations(conn: sqlite3.Connection, file_path: str):
    """Import Claude conversation data."""
    print(f"Importing Claude conversations from {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    cursor = conn.cursor()
    
    for conv in conversations:
        if not conv.get('mapping'):
            continue
            
        conv_id = str(uuid.uuid4())
        title = conv.get('title', 'Untitled')
        created_at = datetime.fromtimestamp(conv.get('create_time', 0))
        updated_at = datetime.fromtimestamp(conv.get('update_time', 0))
        
        # Insert conversation
        cursor.execute('''
            INSERT OR REPLACE INTO conversations 
            (id, title, source, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (conv_id, title, 'claude', created_at, updated_at, json.dumps({
            'original_create_time': conv.get('create_time'),
            'original_update_time': conv.get('update_time')
        })))
        
        # Process messages from mapping
        messages = []
        for node_id, node in conv['mapping'].items():
            message = node.get('message')
            if not message or not message.get('content'):
                continue
                
            content = message['content']
            if content.get('content_type') == 'text' and content.get('parts'):
                text_content = '\n'.join(content['parts']) if isinstance(content['parts'], list) else str(content['parts'])
                if text_content.strip():
                    messages.append({
                        'id': message['id'],
                        'role': message.get('author', {}).get('role', 'unknown'),
                        'content': text_content,
                        'created_at': created_at,
                        'metadata': json.dumps({
                            'node_id': node_id,
                            'status': message.get('status'),
                            'weight': message.get('weight')
                        })
                    })
        
        # Insert messages
        for msg in messages:
            cursor.execute('''
                INSERT OR REPLACE INTO messages
                (id, conversation_id, role, content, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (msg['id'], conv_id, msg['role'], msg['content'], msg['created_at'], msg['metadata']))
            
            # Also add to memories table for searchability
            memory_id = f"claude_{msg['id']}"
            cursor.execute('''
                INSERT OR REPLACE INTO memories
                (id, content, source, created_at, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (memory_id, msg['content'], 'claude', msg['created_at'], json.dumps({
                'conversation_id': conv_id,
                'conversation_title': title,
                'role': msg['role'],
                'type': 'conversation_message'
            })))
    
    conn.commit()
    print(f"Imported {len([c for c in conversations if c.get('mapping')])} Claude conversations")

def import_chatgpt_conversations(conn: sqlite3.Connection, file_path: str):
    """Import ChatGPT conversation data."""
    print(f"Importing ChatGPT conversations from {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    cursor = conn.cursor()
    
    for conv in conversations:
        conv_id = conv.get('uuid', str(uuid.uuid4()))
        title = conv.get('name', 'Untitled')
        created_at = datetime.fromisoformat(conv.get('created_at', '').replace('Z', '+00:00'))
        updated_at = datetime.fromisoformat(conv.get('updated_at', '').replace('Z', '+00:00'))
        
        # Insert conversation
        cursor.execute('''
            INSERT OR REPLACE INTO conversations
            (id, title, source, created_at, updated_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (conv_id, title, 'chatgpt', created_at, updated_at, json.dumps({
            'summary': conv.get('summary'),
            'account_uuid': conv.get('account', {}).get('uuid')
        })))
        
        # Process messages
        messages = conv.get('chat_messages', [])
        for i, msg in enumerate(messages):
            msg_id = f"{conv_id}_msg_{i}"
            role = msg.get('role', 'unknown')
            content = msg.get('message', '') or msg.get('content', '')
            
            if isinstance(content, dict):
                # Handle structured content
                if 'parts' in content:
                    content = '\n'.join(content['parts']) if isinstance(content['parts'], list) else str(content['parts'])
                elif 'text' in content:
                    content = content['text']
                else:
                    content = str(content)
            elif isinstance(content, list):
                # Handle list content
                content = '\n'.join(str(item) for item in content)
            else:
                content = str(content)
            
            if content.strip():
                msg_created_at = created_at  # ChatGPT export doesn't have individual message timestamps
                
                cursor.execute('''
                    INSERT OR REPLACE INTO messages
                    (id, conversation_id, role, content, created_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (msg_id, conv_id, role, content, msg_created_at, json.dumps({
                    'message_index': i,
                    'original_message': msg
                })))
                
                # Also add to memories table
                memory_id = f"chatgpt_{msg_id}"
                cursor.execute('''
                    INSERT OR REPLACE INTO memories
                    (id, content, source, created_at, metadata)
                    VALUES (?, ?, ?, ?, ?)
                ''', (memory_id, content, 'chatgpt', msg_created_at, json.dumps({
                    'conversation_id': conv_id,
                    'conversation_title': title,
                    'role': role,
                    'type': 'conversation_message'
                })))
    
    conn.commit()
    print(f"Imported {len(conversations)} ChatGPT conversations")

def main():
    """Main import function."""
    downloads_dir = "/Users/sven/Downloads"
    db_path = os.path.join(downloads_dir, "conversations_memory.db")
    
    # Create database
    conn = create_database(db_path)
    
    try:
        # Import Claude conversations
        claude_file = os.path.join(downloads_dir, "claude_data", "conversations.json")
        if os.path.exists(claude_file):
            import_claude_conversations(conn, claude_file)
        else:
            print(f"Claude file not found: {claude_file}")
        
        # Import ChatGPT conversations
        chatgpt_file = os.path.join(downloads_dir, "chatgpt_data", "conversations.json")
        if os.path.exists(chatgpt_file):
            import_chatgpt_conversations(conn, chatgpt_file)
        else:
            print(f"ChatGPT file not found: {chatgpt_file}")
        
        # Print summary
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM conversations")
        conv_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM messages")
        msg_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM memories")
        memory_count = cursor.fetchone()[0]
        
        print(f"\nImport completed successfully!")
        print(f"Total conversations: {conv_count}")
        print(f"Total messages: {msg_count}")
        print(f"Total memories: {memory_count}")
        print(f"Database saved to: {db_path}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()