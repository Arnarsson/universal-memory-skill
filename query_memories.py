#!/usr/bin/env python3
"""
Simple tool to query the conversation memory database.
"""

import sqlite3
import json
import sys
from datetime import datetime

def search_memories(db_path: str, query: str, limit: int = 10):
    """Search memories containing the query string."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Search for memories containing the query
    cursor.execute('''
        SELECT id, content, source, created_at, metadata
        FROM memories
        WHERE content LIKE ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (f'%{query}%', limit))
    
    results = cursor.fetchall()
    conn.close()
    
    print(f"\nFound {len(results)} memories matching '{query}':\n")
    
    for i, (mem_id, content, source, created_at, metadata_str) in enumerate(results, 1):
        metadata = json.loads(metadata_str) if metadata_str else {}
        
        print(f"{i}. [{source.upper()}] {metadata.get('conversation_title', 'Untitled')}")
        print(f"   Role: {metadata.get('role', 'unknown')}")
        print(f"   Date: {created_at}")
        print(f"   Content: {content[:200]}{'...' if len(content) > 200 else ''}")
        print()

def get_conversation_stats(db_path: str):
    """Get statistics about the conversation database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get conversation counts by source
    cursor.execute('SELECT source, COUNT(*) FROM conversations GROUP BY source')
    conv_stats = cursor.fetchall()
    
    # Get message counts by source  
    cursor.execute('''
        SELECT c.source, COUNT(m.id) 
        FROM conversations c 
        LEFT JOIN messages m ON c.id = m.conversation_id 
        GROUP BY c.source
    ''')
    msg_stats = cursor.fetchall()
    
    # Get memory counts by source
    cursor.execute('SELECT source, COUNT(*) FROM memories GROUP BY source')
    mem_stats = cursor.fetchall()
    
    # Get recent conversations
    cursor.execute('''
        SELECT title, source, created_at 
        FROM conversations 
        ORDER BY created_at DESC 
        LIMIT 10
    ''')
    recent_convs = cursor.fetchall()
    
    conn.close()
    
    print("=== CONVERSATION DATABASE STATISTICS ===\n")
    
    print("Conversations by source:")
    for source, count in conv_stats:
        print(f"  {source}: {count:,}")
    
    print("\nMessages by source:")
    for source, count in msg_stats:
        print(f"  {source}: {count:,}")
    
    print("\nMemories by source:")
    for source, count in mem_stats:
        print(f"  {source}: {count:,}")
    
    print("\nMost recent conversations:")
    for title, source, created_at in recent_convs:
        print(f"  [{source.upper()}] {title[:60]}{'...' if len(title) > 60 else ''} ({created_at})")
    
    print()

def main():
    """Main function."""
    db_path = "/Users/sven/Downloads/conversations_memory.db"
    
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        search_memories(db_path, query)
    else:
        get_conversation_stats(db_path)
        print("Usage: python3 query_memories.py <search term>")
        print("Example: python3 query_memories.py 'memory MCP'")

if __name__ == "__main__":
    main()