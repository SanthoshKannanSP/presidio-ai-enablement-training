# Research Agent Using LangChain

## Prerequisites
1. Install required dependencies
```bash
pip install -r requirements.txt
```

2. Ensure you have AWS Bedrock access with Claude 3 Sonnet model enabled in your AWS account.

3. Enable [Google Drive API](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com) and [authorize credentials for desktop app](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application)

4. Download the credentials and save it as `credentials.json`

## Create Vector DB
Add the relavent documents to `docs` folder and run:
```bash
python create-vector-db.py
```

## Add documents to MCP tool
Add the Google Doc document ids in `mcp-server.py` to add them to MCP tool. You can obtain your folder and document id from the URL: docs.google.com/document/d/**1bfaMQ18_i56204VaQDVeAFpqEijJTgvurupdEDiaUQw**/edit 

## Running the Chatbot
Once the Google Drive credentials and vector db are created, run:
```bash
python main.py
```