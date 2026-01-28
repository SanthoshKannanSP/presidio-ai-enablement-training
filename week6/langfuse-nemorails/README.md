# Langfuse NeMo Rails Agent

A modular LangChain agent with tools for reading file and web search, featuring NeMo Guardrails for safety and Langfuse for observability.

## Prerequisites

### Python Requirements
- Python >= 3.13
- Install dependencies:
```bash
uv sync
```

### AWS Bedrock Access
- Configure AWS credentials with access to Bedrock
- Ensure access to the Claude 3 Haiku model (`anthropic.claude-3-haiku-20240307-v1:0`)

### Environment Configuration
1. Copy `.env.sample` to `.env`
2. Configure Langfuse credentials in `.env`:
```
LANGFUSE_SECRET_KEY=your_secret_key
LANGFUSE_PUBLIC_KEY=your_public_key  
LANGFUSE_BASE_URL=your_langfuse_url
```

## Running the Agent

```bash
uv run main.py
```

The agent will prompt for user input and respond using available tools (file reading and web search) while applying safety guardrails.

## Running Evaluation

```bash
uv run evaluate.py
```

This will run the evaluation test suite and generate a markdown report (`agent_eval_report.md`) with correctness and latency metrics.
