---
name: UniversalMemorySkill
description: "Interface to the Universal Memory MCP — allows the agent to read and write persistent memory via HTTP."
---

# Usage  
Use this skill to recall or store long-term information.  
When a user asks questions like:
- "What am I working on?"  
- "Remember that I did X"  
- "Show me my memory stats"  
you can use the scripts below.

# Available Scripts  
- `scripts/get_graph.js`: Fetch full context graph for an entity.  
- `scripts/add_observation.js`: Add a new memory observation.  
- `scripts/create_entity.js`: Create new entity (person, org, project).  
- `scripts/search_entities.js`: Search memory database by keyword.  
- `scripts/stats.js`: Retrieve global memory statistics.  

Each script returns a structured JSON object.
