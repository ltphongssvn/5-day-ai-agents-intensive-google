# ~/code/ltphongssvn/5-day-ai-agents-intensive-google/agents-to-build.md
# AI Agents to Build for 5-Day Intensive Course

## Day 1: Foundational Agents
### 1. Simple Reflex Agent
- **Purpose**: Demonstrate basic stimulus-response patterns
- **Core Features**: Rule-based actions, immediate response to inputs
- **Technologies**: Python, basic if-then logic

### 2. Model-Based Agent
- **Purpose**: Show how agents maintain internal state
- **Core Features**: World model, state tracking, prediction
- **Technologies**: Python, state management

## Day 2: Tool-Integrated Agents
### 3. Web Search Agent
- **Purpose**: Integrate external APIs and tools
- **Core Features**: API calls, result parsing, query optimization
- **Technologies**: MCP, REST APIs, web scraping

### 4. Code Execution Agent
- **Purpose**: Demonstrate safe code execution capabilities
- **Core Features**: Sandboxed execution, result interpretation
- **Technologies**: Python subprocess, Docker containers

## Day 3: Memory-Enhanced Agents
### 5. Conversational Agent with Session Memory
- **Purpose**: Maintain context across multiple turns
- **Core Features**: Short-term memory, context window management
- **Technologies**: Vector databases, embedding models

### 6. Knowledge Base Agent
- **Purpose**: Long-term memory and retrieval
- **Core Features**: Document storage, semantic search, RAG
- **Technologies**: ChromaDB/Pinecone, embeddings

## Day 4: Observable & Evaluatable Agents
### 7. Self-Monitoring Agent
- **Purpose**: Demonstrate logging and observability
- **Core Features**: Performance metrics, error tracking, self-evaluation
- **Technologies**: OpenTelemetry, Prometheus, custom metrics

### 8. A/B Testing Agent
- **Purpose**: Compare different strategies and learn
- **Core Features**: Experiment tracking, performance comparison
- **Technologies**: MLflow, custom evaluation framework

## Day 5: Production-Ready Multi-Agent Systems
### 9. Orchestrator Agent
- **Purpose**: Coordinate multiple specialized agents
- **Core Features**: Task decomposition, agent routing, result aggregation
- **Technologies**: A2A Protocol, message queues

### 10. Research Assistant Multi-Agent System
- **Purpose**: Complete system combining all learned concepts
- **Core Features**: 
  - Research agent (web search, data gathering)
  - Analysis agent (data processing, insights)
  - Writer agent (report generation)
  - Quality assurance agent (fact-checking, evaluation)
- **Technologies**: All previous + orchestration layer

## Implementation Priority
1. Start with Simple Reflex Agent (Day 1 foundation)
2. Build Web Search Agent (Day 2 - most reusable)
3. Add Conversational Agent (Day 3 - user interaction)
4. Implement Orchestrator (Day 5 - ties everything together)
5. Fill in remaining agents based on learning needs

## Next Steps
- Create project structure for each agent
- Set up development environment
- Define interfaces between agents
- Establish testing framework
