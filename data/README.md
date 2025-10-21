# Conversation Data

This directory contains conversation history from Claude and ChatGPT, split into chunks to comply with GitHub's file size limits.

## Contents

- `claude/` - Claude conversation exports (2 chunks, ~35MB total)
- `chatgpt/` - ChatGPT conversation exports (8 chunks, ~158MB total)

## Reconstruction

To reconstruct the original zip files:

### Claude Conversations
```bash
cd claude
cat claude_conversations_part_* > claude_conversations.zip
unzip claude_conversations.zip
```

### ChatGPT Conversations
```bash
cd chatgpt
cat chatgpt_conversations_part_* > chatgpt_conversations.zip
unzip chatgpt_conversations.zip
```

## Import to Database

Use the provided `import_conversations.py` script to import these conversations into a SQLite database:

```bash
python3 import_conversations.py
```

This will create a `conversations_memory.db` file containing:
- All conversations organized by source
- Searchable memories for quick retrieval
- Message-level granularity with metadata

## Database Schema

The database contains three main tables:

1. **conversations** - High-level conversation metadata
   - id, title, source, created_at, updated_at, metadata

2. **messages** - Individual messages within conversations
   - id, conversation_id, role, content, created_at, metadata

3. **memories** - Searchable memory entries
   - id, content, source, created_at, metadata

## Statistics

- **Total Conversations**: 8,577
  - Claude: 7,454 conversations (50,511 messages)
  - ChatGPT: 1,123 conversations (12,047 messages)
- **Total Messages**: 62,558
- **Total Searchable Memories**: 62,558

## Usage

Query the database using `query_memories.py`:

```bash
# Show statistics
python3 query_memories.py

# Search for specific content
python3 query_memories.py "search term"
```

## Date Range

- Claude conversations: Up to October 21, 2025
- ChatGPT conversations: Up to October 21, 2025
