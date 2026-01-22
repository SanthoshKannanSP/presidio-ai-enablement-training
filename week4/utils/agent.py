from langchain_aws.chat_models import ChatBedrockConverse
from langchain.agents import create_agent
from langchain.messages import SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

from utils.vector_db import create_or_get_collection
from utils.search_utils import get_context_with_sources, semantic_search


@tool
def query_documents(query: str) -> str:
    """
    Retrieve related information from Presidio related documents based on the given query.

    :param query: The query to fetch relevant information
    :type query: str
    :return: String of relevant information to the given query
    :rtype: str
    """
    collection = create_or_get_collection("presidio-research")
    context = semantic_search(collection, query, 10)

    return context


async def create_bedrock_agent():
    model = ChatBedrockConverse(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
    )

    prompt_string = SystemMessage(
        "system",
        """
        You are a specialized research agent designed to assist employees with accurate, contextual, and actionable information retrieval and analysis. Your primary purpose is to help employees make informed decisions by delivering well-researched, synthesized information from multiple sources. You combine internal company knowledge with external research capabilities to provide comprehensive answers.

        Available tools:
        {tools}
                                  
        Response Framework:
        Step 1: Understand the core question and intent and identify what information sources are needed.
        Step 2: Use appropriate tools to collect relevant data. Use internal sources before referring to external sources.
        Step 3: Combine information and provide a clear, direct answer.
                                  
        If you don't have the necessary information to answer a question, please say that you don't have necessary information to answer the question.
    """,
    )

    client = MultiServerMCPClient(
        {
            "mcpTool": {
                "transport": "stdio",
                "command": "python3.13",
                "args": ["mcp-server.py"],
            }
        }
    )

    mcp_tools = await client.get_tools()
    web_search_tool = DuckDuckGoSearchRun()

    agent = create_agent(
        model=model,
        tools=[*mcp_tools, web_search_tool, query_documents],
        system_prompt=prompt_string,
    )
    return agent
