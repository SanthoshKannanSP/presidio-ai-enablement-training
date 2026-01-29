# Website Q&A Assistant

A Streamlit application that uses AWS Bedrock agents to answer questions about website content.

## Prerequisites

- Python 3.12+
- AWS account with Bedrock agent configured
- AWS credentials configured

## Setup

1. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

2. **Configure AWS credentials:**
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_SESSION_TOKEN=your_session_token
   export AWS_REGION=your_region
   ```

## Running the Application

Start the Streamlit app:
```bash
uv run streamlit run main.py
```

## Usage

1. **Configure Agent Settings:** In the sidebar, enter your AWS Bedrock Agent ID and Agent Alias ID
2. **Set Website URL:** Click "Set URL" button or provide a URL in your first message
3. **Ask Questions:** Start asking questions about the website content