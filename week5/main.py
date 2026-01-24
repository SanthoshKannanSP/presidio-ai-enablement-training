from langchain_aws.chat_models import ChatBedrockConverse
from utils.states import State
import functools
from utils.nodes import supervisor_node, route_decision, it_agent_node, finance_agent_node
from langgraph.graph import StateGraph, START, END

supervisor_llm = ChatBedrockConverse(
    model="anthropic.claude-3-haiku-20240307-v1:0"
)

agent_llm = ChatBedrockConverse(
    model="anthropic.claude-3-sonnet-20240229-v1:0"
)

call_supervisor = functools.partial(supervisor_node, llm=supervisor_llm)
call_it_agent = functools.partial(it_agent_node, llm=agent_llm)
call_finance_agent = functools.partial(finance_agent_node, llm=agent_llm)

router_builder = StateGraph(State)

router_builder.add_node("call_supervisor",call_supervisor)
router_builder.add_node("call_it_agent",call_it_agent)
router_builder.add_node("call_finance_agent",call_finance_agent)

router_builder.add_edge(START,"call_supervisor")
router_builder.add_conditional_edges(
    "call_supervisor",
    route_decision,
    {
        "call_it_agent":"call_it_agent",
        "call_finance_agent":"call_finance_agent",
        "end":END
    }
)

router_builder.add_edge("call_it_agent",END)
router_builder.add_edge("call_finance_agent",END)

router_workflow = router_builder.compile()

print("Presidio Support System")
user_query = input(">>>")
state = router_workflow.invoke({"user_query": user_query})

if "final_response" in state and state["final_response"]:
    print(f"Assistant: {state["final_response"]}")
else:
    print(f"Assistant: I'm sorry, but your question '{state['user_query']}' is outside my scope. I can only help with IT and Finance related queries. Please ask about technology support or financial matters.")
