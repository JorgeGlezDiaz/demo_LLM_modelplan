# business_plan_agent.py

from typing import Annotated
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langchain_core.messages import AIMessage

llm = ChatOllama(model="llama3:latest")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    description: str
    market_analysis: str
    marketing_plan: str
    financial_plan: str
    final_markdown: str


def ask_llm(prompt: str) -> str:
    response = llm.invoke([HumanMessage(content=prompt)])   # response of the llm
    return response.content.strip()     # clean with no spaces


def market_analysis_node(state: State) -> State:
    print("Nmarket_analysis_node")
    prompt = f"""
You are a market research expert. Based on the following company description, write a comprehensive **Market Analysis**.
Use Markdown format and cover target customer, industry trends, competitors, and market size.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"market_analysis": result}


def marketing_plan_node(state: State) -> State:
    print("Node_marketing_plan_node")
    prompt = f"""
You are a marketing strategist. Based on the following company description, write a detailed **Marketing Plan**.
Use Markdown format and include strategy, channels, branding, and customer acquisition methods.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"marketing_plan": result}


def financial_plan_node(state: State) -> State:
    print("financial_plan_node")
    prompt = f"""
You are a financial advisor. Based on the following company description, write a concise but complete **Financial Plan**.
Use Markdown format and include startup costs, revenue projections, and break-even analysis.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"financial_plan": result}
