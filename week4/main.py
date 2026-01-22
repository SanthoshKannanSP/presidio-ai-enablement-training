from utils.agent import bedrock_chat_agent
import asyncio

history = {"messages":[]}

async def chat():
    agent = await bedrock_chat_agent()
    
    print("Presidio AI Agent")
    user_query = input(">>>").strip()
    while True:
        if is_command(user_query):
            should_continue = execute_command(user_query)
            if not should_continue:
                break
        else:
            history["messages"].append({"role":"user", "content": user_query})
            response = await agent.ainvoke(history)

            assistant_response = response["messages"][-1].content

            print(f"\nAssistant: {assistant_response}\n")
            history["messages"].append({"role":"assistant","content":assistant_response})

        user_query = input(">>>").strip()


def is_command(user_query: str):
    if user_query[0]=="/":
        return True
    return False

def execute_command(user_query: str):
    if user_query == "/exit":
        return False
    
    if user_query == "/clear":
        history["messages"].clear()
    
    elif user_query == "/help":
        print("""
        Commands:
        /help: List of all available commands
        /clear: Clear conversation history
        /exit: Stop the program
        """.strip())
    
    elif user_query == "/history":
        print(history)
    else:
        print("Unknown command: Use '/help' to view all available commands")
    return True
        

if __name__ == "__main__":
    asyncio.run(chat())
