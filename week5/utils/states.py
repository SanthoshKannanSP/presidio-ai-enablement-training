from typing_extensions import Literal, TypedDict
from pydantic import BaseModel, Field

class State(TypedDict):
    user_query: str
    decision: str
    reasoning: str
    final_response: str

class Route(BaseModel):
    step: Literal["it_agent","finance_agent","end"] = Field(None, description="The agent to call next in the routing process, or 'end' if the query is unrelated to IT or finance")
    reasoning: str = Field(None, description="Brief reasoning on why the next agent was chosen or why the execution should end")
