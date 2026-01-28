from langchain_aws.chat_models import ChatBedrockConverse
from langchain_community.tools import DuckDuckGoSearchRun, ReadFileTool
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from dotenv import load_dotenv
from langchain.agents import create_agent

# Load environment variables
load_dotenv()

def load_system_prompt() -> str:
    """Load system prompt from file"""
    with open('system_prompt.txt', 'r') as f:
        return f.read()
    
system_prompt = load_system_prompt()

base_model = ChatBedrockConverse(
    model="anthropic.claude-3-sonnet-20240229-v1:0"
)
search_tool = DuckDuckGoSearchRun()
read_tool = ReadFileTool()
llm = base_model.bind_tools([read_tool,search_tool])

config = RailsConfig.from_path("guardrails_config")
guard_rails = RunnableRails(config=config,llm=llm)
agent = create_agent(
    guard_rails,
    system_prompt=system_prompt
)