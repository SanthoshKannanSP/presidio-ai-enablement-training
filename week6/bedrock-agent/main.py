import streamlit as st
import boto3
import uuid
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Website Q&A Assistant",
    page_icon="🌐",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'current_url' not in st.session_state:
    st.session_state.current_url = None
if 'agent_id' not in st.session_state:
    st.session_state.agent_id = ""
if 'agent_alias_id' not in st.session_state:
    st.session_state.agent_alias_id = ""

# Initialize Bedrock Agent Runtime client
@st.cache_resource
def get_bedrock_client():
    """Initialize and cache Bedrock Agent Runtime client"""
    try:
        client = boto3.client(
            'bedrock-agent-runtime'
        )
        return client
    except Exception as e:
        st.error(f"Failed to initialize AWS Bedrock client: {str(e)}")
        return None


def invoke_bedrock_agent(client, prompt, session_id, agent_id, agent_alias_id):
    """
    Invoke Bedrock Agent with the given prompt
    """
    # Check if agent IDs are configured
    if not agent_id or not agent_alias_id:
        return None, "Agent ID and Agent Alias ID must be configured in the AWS Settings sidebar before using the assistant."
    
    # Validate agent IDs format (basic validation)
    if not agent_id.strip() or not agent_alias_id.strip():
        return None, "Agent ID and Agent Alias ID cannot be empty or contain only whitespace."
    
    try:
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=prompt
        )
        
        # Process the streaming response
        completion = ""
        for event in response.get('completion', []):
            if 'chunk' in event:
                chunk = event['chunk']
                if 'bytes' in chunk:
                    completion += chunk['bytes'].decode('utf-8')
        
        return completion, None
        
    except client.exceptions.BadGatewayException:
        return None, "Service temporarily unavailable. Please try again."
    except client.exceptions.ThrottlingException:
        return None, "Too many requests. Please wait a moment and try again."
    except client.exceptions.ValidationException as e:
        return None, f"Invalid request: {str(e)}. Please verify your Agent ID and Agent Alias ID are correct."
    except client.exceptions.ResourceNotFoundException as e:
        return None, f"Agent not found: {str(e)}. Please check your Agent ID and Agent Alias ID."
    except client.exceptions.AccessDeniedException as e:
        return None, f"Access denied: {str(e)}. Please check your AWS permissions and credentials."
    except Exception as e:
        error_msg = str(e)
        if "InvalidParameterException" in error_msg:
            return None, "Invalid agent configuration. Please verify your Agent ID and Agent Alias ID are correct."
        elif "UnauthorizedException" in error_msg:
            return None, "Unauthorized access. Please check your AWS credentials and permissions."
        else:
            return None, f"Error invoking agent: {error_msg}"


def display_message(role, content, timestamp=None):
    """Display a chat message with styling"""
    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)
            if timestamp:
                st.caption(timestamp)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(content)
            if timestamp:
                st.caption(timestamp)


def main():
    # Title and description
    st.title("🌐 Website Q&A Assistant")
    st.markdown("""
    Ask questions about any website! Provide a URL and I'll analyze the content to answer your questions.
    """)
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # AWS Settings (collapsed by default)
        with st.expander("AWS Settings", expanded=True):
            st.session_state.agent_id = st.text_input(
                "Agent ID", 
                value=st.session_state.agent_id,
                type="password",
                help="Enter your AWS Bedrock Agent ID"
            )
            st.session_state.agent_alias_id = st.text_input(
                "Agent Alias ID", 
                value=st.session_state.agent_alias_id,
                type="password",
                help="Enter your AWS Bedrock Agent Alias ID"
            )
            
            # Settings status indicator
            if st.session_state.agent_id and st.session_state.agent_alias_id:
                st.success("✅ Agent settings configured")
            else:
                st.warning("⚠️ Please configure Agent ID and Agent Alias ID")
        
        st.divider()
        
        # Current URL display
        st.header("📄 Current Website")
        if st.session_state.current_url:
            st.info(f"🔗 {st.session_state.current_url}")
        else:
            st.warning("No URL set yet")
        
        st.divider()
        
        # Session info
        st.header("💬 Session Info")
        st.text(f"Messages: {len(st.session_state.messages)}")
        st.text(f"Session ID: {st.session_state.session_id[:8]}...")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.current_url = None
            st.rerun()
        
        st.divider()
        
        # Instructions
        with st.expander("📖 How to Use"):
            st.markdown("""
            1. **Set URL**: Start by providing a website URL
            2. **Ask Questions**: Ask anything about the website content
            3. **Get Answers**: The AI will analyze the page and respond
            
            **Example Questions:**
            - What is this page about?
            - Summarize the main points
            - Find information about [topic]
            - What are the key features mentioned?
            """)
    
    # Main chat area
    st.divider()
    
    # Display chat history
    for message in st.session_state.messages:
        display_message(
            message["role"],
            message["content"],
            message.get("timestamp")
        )
    
    # Chat input area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.chat_input("Ask a question or provide a URL...")
    
    with col2:
        if st.button("📎 Set URL", use_container_width=True):
            st.session_state.show_url_input = True
    
    # URL input dialog
    if st.session_state.get('show_url_input', False):
        with st.form("url_form"):
            st.subheader("Enter Website URL")
            new_url = st.text_input(
                "URL",
                placeholder="https://example.com",
                value=st.session_state.current_url or ""
            )
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Set URL", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit and new_url:
                st.session_state.current_url = new_url
                st.session_state.show_url_input = False
                # Add system message
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"✅ URL set to: {new_url}\n\nYou can now ask questions about this website!",
                    "timestamp": timestamp
                })
                st.rerun()
            
            if cancel:
                st.session_state.show_url_input = False
                st.rerun()
    
    # Process user input
    if user_input:
        # Get Bedrock client
        client = get_bedrock_client()
        
        if client is None:
            st.error("❌ Failed to connect to AWS Bedrock. Please check your configuration.")
            return
        
        # Add user message to chat
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })
        
        # Display user message
        display_message("user", user_input, timestamp)
        
        # Prepare prompt with URL context if available
        if st.session_state.current_url:
            full_prompt = f"Website URL: {st.session_state.current_url}\n\nQuestion: {user_input}"
        else:
            full_prompt = user_input
        
        # Show thinking indicator
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                # Invoke Bedrock Agent
                response, error = invoke_bedrock_agent(
                    client,
                    full_prompt,
                    st.session_state.session_id,
                    st.session_state.agent_id,
                    st.session_state.agent_alias_id
                )
        
        # Handle response
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if error:
            error_message = f"❌ Error: {error}"
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
                "timestamp": timestamp
            })
            st.error(error_message)
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": timestamp
            })
            display_message("assistant", response, timestamp)
        
        # Rerun to update the chat
        st.rerun()


if __name__ == "__main__":
    main()
