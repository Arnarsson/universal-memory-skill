# Universal Memory Skill  

This repository implements a **Claude agent skill** that interfaces with the Universal Memory Memory Control Panel (MCP). It enables agents to read and write persistent long‑term memory via HTTP endpoints.  

## Overview  

The `UniversalMemorySkill` allows a conversational agent (such as Claude or ChatGPT) to recall and store long‑term information. When a user asks questions like:  

- "What am I working on?"  
- "Remember that I did X"  
- "Show me my memory stats"  
  
The skill can answer by using scripts provided in this repository.  

## Available Scripts  

| Script | Description |  
|-------|-------------|  
| `scripts/get_graph.js` | Fetches the full context graph for an entity. |  
| `scripts/add_observation.js` | Adds a new memory observation to the database. |  
| `scripts/create_entity.js` | Creates a new entity (person, organization, project). |  
| `scripts/search_entities.js` | Searches the memory database by keyword. |  
| `scripts/stats.js` | Retrieves global memory statistics. |  
  
Each script returns a structured JSON object that the agent can parse and present to the user.  

## Data & Utilities  

The `data` directory contains split conversation history chunks and a README with instructions.  
`import_conversations.py` reconstructs conversation data from Claude and ChatGPT chunks and imports them into Universal Memory.  
`query_memories.py` provides a way to search through conversation history.  
The `utils` folder includes helper functions for asynchronous HTTP requests.  

## Getting Started  

1. Clone this repository.  
2. Ensure you have Python 3.8+ installed.  
3. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  
4. Use the scripts in the `scripts` folder to interact with Universal Memory MCP.  
5. Refer to `SKILL.md` for manifest details and usage guidance.  

## License  

Specify an appropriate license for your project.
