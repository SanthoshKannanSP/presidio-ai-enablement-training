# Multi-Agent Support System using LangGraph

A multi-agent chatbot system built with LangChain and AWS Bedrock that provides intelligent support for IT and Finance queries. The system uses a supervisor agent to route user queries to specialized agents, each equipped with domain-specific knowledge through vector-based document retrieval.

## Architecture
The system consists of:
- **Supervisor Node**: Routes queries using Claude 3 Haiku model
- **IT Agent**: Handles technology-related queries using Claude 3 Sonnet model
- **Finance Agent**: Handles finance-related queries using Claude 3 Sonnet model
- **Vector Database**: ChromaDB stores and retrieves relevant documents

## Prerequisites
### 1. AWS Bedrock Access
- AWS account with Bedrock service access
- Access to the following models in your AWS region:
  - `anthropic.claude-3-haiku-20240307-v1:0`
  - `anthropic.claude-3-sonnet-20240229-v1:0`
- AWS credentials configured (via AWS CLI, environment variables, or IAM roles)

### 2. Installing Dependencies
```bash
uv sync
```

## Setup
### Creating Vector Database
Before running the chatbot, you need to create the vector database and populate it with documents:

1. **Add Documents**: Place your documents in the respective folders:
   - **IT Documents**: Add PDF files to the `it_docs/` folder
   - **Finance Documents**: Add PDF files to the `finance_docs/` folder

2. **Create and Populate Vector Database**:
```bash
uv run create-vector-db.py
```

This script will:
- Create ChromaDB collections for IT and Finance documents
- Process all PDF files in both `it_docs/` and `finance_docs/` folders
- Generate embeddings and store them in the vector database
- Create a `chroma_db/` directory with the database files

## Running the Chatbot
Start the interactive chatbot:
```bash
uv run main.py
```

The system will:
1. Initialize the multi-agent workflow
2. Present a command prompt (`>>>`)
3. Accept user queries and route them to appropriate agents
4. Return responses based on the relevant documents