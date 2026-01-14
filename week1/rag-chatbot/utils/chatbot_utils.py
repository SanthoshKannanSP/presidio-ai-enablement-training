from datetime import datetime
import uuid
import boto3
import json
import os
from utils.search_utils import semantic_search, get_context_with_sources

conversations = {}

def get_bedrock_client():
    """Initialize AWS Bedrock client"""
    try:
        # Get AWS credentials from environment variables
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError("AWS credentials not found in environment variables")
        
        client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        return client
    except Exception as e:
        print(f"Error initializing Bedrock client: {str(e)}")
        raise e

def invoke_bedrock_model(prompt: str, temperature: float = 0.0, max_tokens: int = 500):
    """Invoke AWS Bedrock Claude model"""
    try:
        client = get_bedrock_client()
        
        # Claude 3 Haiku model configuration
        model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json',
            accept='application/json'
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
        
    except Exception as e:
        print(f"Error invoking Bedrock model: {str(e)}")
        raise e

def create_session():
    """Create a new conversation session"""
    session_id = str(uuid.uuid4())
    conversations[session_id] = []
    return session_id

def add_message(session_id: str, role: str, content: str):
    """Add a message to the conversation history"""
    if session_id not in conversations:
        conversations[session_id] = []

    conversations[session_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })

def get_conversation_history(session_id: str, max_messages: int = None):
    """Get conversation history for a session"""
    if session_id not in conversations:
        return []

    history = conversations[session_id]
    if max_messages:
        history = history[-max_messages:]

    return history

def format_history_for_prompt(session_id: str, max_messages: int = 5):
    """Format conversation history for inclusion in prompts"""
    history = get_conversation_history(session_id, max_messages)
    formatted_history = ""

    for msg in history:
        role = "Human" if msg["role"] == "user" else "Assistant"
        formatted_history += f"{role}: {msg['content']}\n\n"

    return formatted_history.strip()

def contextualize_query(query: str, conversation_history: str):
    """Convert follow-up questions into standalone queries"""
    contextualize_prompt = f"""Given a chat history and the latest user question 
    which might reference context in the chat history, formulate a standalone 
    question which can be understood without the chat history. Do NOT answer 
    the question, just reformulate it if needed and otherwise return it as is.

    Chat history:
    {conversation_history}

    Question:
    {query}

    Reformulated standalone question:"""

    try:
        response = invoke_bedrock_model(
            prompt=contextualize_prompt,
            temperature=0.0,
            max_tokens=500
        )
        return response.strip()
    except Exception as e:
        print(f"Error contextualizing query: {str(e)}")
        return query

def get_prompt(context, conversation_history, query):
  prompt = f"""Based on the following context and conversation history, please provide a relevant and contextual response.
    If the answer cannot be derived from the context, only use the conversation history or say "I cannot answer this based on the provided information."

    Context from documents:
    {context}

    Previous conversation:
    {conversation_history}

    Human: {query}

    Assistant:"""
  return prompt

def generate_response(query: str, context: str, conversation_history: str = ""):
    """Generate a response using AWS Bedrock with conversation history"""
    prompt = get_prompt(context, conversation_history, query)
    
    # Add system message context to the prompt for Claude
    full_prompt = f"""You are a helpful assistant that answers questions based on the provided context.

{prompt}"""

    try:
        response = invoke_bedrock_model(
            prompt=full_prompt,
            temperature=0.0,
            max_tokens=500
        )
        return response.strip()
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return "I apologize, but I'm unable to generate a response at the moment due to a technical issue."

def conversational_rag_query(
    collection,
    query: str,
    session_id: str,
    n_chunks: int = 10
):
    """Perform RAG query with conversation history"""
    # Get conversation history
    conversation_history = format_history_for_prompt(session_id)

    # Handle follo up questions
    query = contextualize_query(query, conversation_history)

    # Get relevant chunks
    context, sources = get_context_with_sources(
        semantic_search(collection, query, n_chunks)
    )

    response = generate_response(query, context, conversation_history)

    # Add to conversation history
    add_message(session_id, "user", query)
    add_message(session_id, "assistant", response)

    return response, sources
