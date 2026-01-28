from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
import ast
from agent import agent,search_tool,read_tool

# Initialize Langfuse client
langfuse = Langfuse()
langfuse_handler = CallbackHandler()

def invoke_agent(user_query:str):
    response = agent.invoke({"messages":[{"role": "user", "content": user_query}]},config={"callbacks": [langfuse_handler]})

    if response["messages"][-1].tool_calls:
        # Get the tool calls from the last message
        tool_calls = response["messages"][-1].tool_calls
        tool_results = []
        
        # Execute each tool call
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]
            
            try:
                # Execute the appropriate tool
                if tool_name == "duckduckgo_search":
                    result = search_tool.run(tool_args.get("query", ""))
                elif tool_name == "read_file":
                    result = read_tool.run(tool_args.get("file_path", ""))
                else:
                    result = f"Unknown tool: {tool_name}"
                
                # Create tool message
                tool_message = {
                    "role": "tool",
                    "content": str(result),
                    "tool_call_id": tool_id
                }
                tool_results.append(tool_message)
                
            except Exception as e:
                # Handle tool execution errors
                tool_message = {
                    "role": "tool", 
                    "content": f"Error executing {tool_name}: {str(e)}",
                    "tool_call_id": tool_id
                }
                tool_results.append(tool_message)
        
        # Add tool results to the message history and invoke agent again
        messages_with_tools = response["messages"] + tool_results
        
        # Continue the conversation with tool results
        final_res = agent.invoke(
            {"messages": messages_with_tools},
            config={"callbacks": [langfuse_handler]}
        )

        return final_res
    else:
        return response
        
if __name__ == "__main__":
    user_query = input(">>> ")
    response = invoke_agent(user_query)

    try:
        final_res = ast.literal_eval(response["messages"][-1].content)
        print(final_res[0]["text"])
    except:
        print(response["messages"][-1].content)
