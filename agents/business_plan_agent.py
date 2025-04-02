from typing import Annotated
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llama3.2:latest")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    description: str
    market_analysis: str
    marketing_plan: str
    financial_plan: str
    final_markdown: str


def ask_llm(prompt: str) -> str:
    response = llm.invoke([HumanMessage(content=prompt)])   # response of the llm
    return response.content.strip()                         # clean with no spaces


def market_analysis_node(state: State) -> State:
    print("▶️ market_analysis_node")
    prompt = f"""
You are a professional market research analyst.

Using the company description below, write a detailed and well-structured **Market Analysis** section for a business plan. 
Use a formal, professional tone and Markdown formatting.

Your response should include:
- **Target Customer Profile**: demographics, behaviors, needs
- **Industry Trends**: current and emerging trends
- **Competitive Landscape**: key competitors and their strengths/weaknesses
- **Market Size & Growth Potential**: estimated figures, sources if possible

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"market_analysis": result}


def marketing_plan_node(state: State) -> State:
    print("▶️ marketing_plan_node")
    prompt = f"""
You are an experienced marketing strategist.

Using the company description below, write a comprehensive and professional **Marketing Plan** section for a business plan. 
Use Markdown format for clarity and structure.

Your response should include:
- **Overall Marketing Strategy**: positioning and key messaging
- **Customer Acquisition Channels**: online/offline, social media, SEO, etc.
- **Branding Approach**: visual identity, tone of voice
- **Sales Funnel & Conversion**: how leads are captured and converted
- **Marketing Budget Overview**: rough distribution if possible

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"marketing_plan": result}


def financial_plan_node(state: State) -> State:
    print("▶️ financial_plan_node")
    prompt = f"""
You are a professional financial advisor.

Using the company description below, write a detailed and realistic **Financial Plan** section for a business plan. 
Use clear Markdown formatting and structure your response with the following key areas:

- **Startup Costs**: estimated initial investment (equipment, software, staff, etc.)
- **Revenue Projections**: monthly or quarterly revenue for the first year
- **Break-even Analysis**: when the company expects to cover its costs
- **Cost Structure**: fixed and variable costs
- **Funding Needs**: how much capital is needed and what it will be used for

Make reasonable assumptions when necessary, and ensure clarity for potential investors or stakeholders.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"financial_plan": result}
