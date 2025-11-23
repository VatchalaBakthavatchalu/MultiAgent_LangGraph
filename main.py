from fastapi import FastAPI
from pydantic import BaseModel
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import Field
from typing import Optional, TypedDict, List, Literal
from langchain.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from typing import Annotated, Sequence, TypedDict

app = FastAPI()


class UserQuestionRequest(BaseModel):
    question: str
    chat_id: int
    user_id: int


class UserQuestionResponse(BaseModel):
    answer: str
    chat_id: int
    user_id: int





# ---------------------
# TOOL DEFINITIONS
# ---------------------

@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def subtract_numbers(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


@tool
def divide_numbers(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        return "Error: Cannot divide by zero."
    return a / b


math_tools = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]


# ---------------------
# LANGGRAPH SETUP
# ---------------------
class GraphState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2).bind_tools(math_tools)


# ---- NODE 1: LLM Node ----
def llm_node(state: GraphState):
    system_prompt = SystemMessage(content=
                                  "You are my AI assistant, please answer my query to the best of your ability."
                                  )
    response = llm.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}


# ---- NODE 2: TOOL NODE ----


def should_continue(state: dict) -> Literal["tool_node", END]:
    """Route to tool_node or END based on LLM output"""
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "tool_node"

    return END


tool_node = ToolNode(tools=math_tools)
graph = StateGraph(GraphState)
graph.add_node("llm_node", llm_node)
graph.add_node("tool_node", tool_node)

# ---------------------
# GRAPH EDGES
# ---------------------
graph.set_entry_point("llm_node")

graph.add_conditional_edges(
    "llm_node",
    should_continue,
    ["tool_node", END]  # Auto-maps to function return values
)
graph.add_edge("tool_node", "llm_node")

app_graph = graph.compile()


@app.post("/answer", response_model=UserQuestionResponse)
async def post_user_question(user_question: UserQuestionRequest) -> UserQuestionResponse:
    inputs = {"messages": [HumanMessage(content=user_question.question)]}
    result = app_graph.invoke(inputs)

    final_answer = result["messages"][-1].content[0]['text']

    return UserQuestionResponse(
        answer=final_answer,
        chat_id=user_question.chat_id,
        user_id=user_question.user_id
    )