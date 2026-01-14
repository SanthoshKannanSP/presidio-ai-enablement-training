# Task - RAG Chatbot

## Prerequisites
1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure you have AWS Bedrock access with Claude 3 Sonnet model enabled in your AWS account.

## Setting up AWS Credentials
Set the following environment variables before running the chatbot:
```bash
export AWS_ACCESS_KEY_ID="your_access_key_here"
export AWS_SECRET_ACCESS_KEY="your_secret_key_here"
export AWS_REGION="your_preferred_region_with_Bedrock_access"
```

## Create the vector DB
Add the relavent documents to `docs` folder and run:
```bash
python create-vector-db.py
```

## Running the Chatbot
Once AWS credentials are configured, run:
```bash
python chatbot.py
```