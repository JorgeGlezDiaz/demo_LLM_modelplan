from typing import Annotated
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llama3.2:latest")

class State(TypedDict):
    messages: Annotated[list, add_messages]
    description: str
    executive_summary: str
    project_team: str
    product_description: str
    market_analysis: str
    marketing_plan: str
    production_plan: str
    organization_personnel: str
    investment_plan: str
    income_cashflow_forecast: str
    financial_plan: str
    legal_aspects: str
    risk_assessment: str
    contingency_coverage: str
    csr: str
    final_markdown: str


def ask_llm(prompt: str) -> str:
    response = llm.invoke([HumanMessage(content=prompt)])   # response of the llm
    return response.content.strip()                         # clean with no spaces


def executive_summary_node(state: State) -> State:
    print("\u25B6\ufe0f executive_summary_node")
    prompt = f"""
You are a business strategist.

Based on the company description below, write an insightful and persuasive **Executive Summary**.
Use Markdown formatting and include the mission, vision, core offering, and unique value proposition.
Make sure it feels like an elevator pitch to investors.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"executive_summary": result}


def project_team_node(state: State) -> State:
    print("\u25B6\ufe0f project_team_node")
    prompt = f"""
You are an HR and startup consultant.

Using the company description below, describe the **Project Promotion Team**.
Include roles, responsibilities, relevant experience, and key strengths of the founding members.
Use Markdown format, and if team details are missing, infer plausible structure.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"project_team": result}


def product_description_node(state: State) -> State:
    print("\u25B6\ufe0f product_description_node")
    prompt = f"""
You are a product development expert.

Based on the company description below, write a clear and compelling **Description of the Product or Service**.
Use Markdown format and include features, benefits, use cases, and technological aspects if relevant.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"product_description": result}


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


def production_plan_node(state: State) -> State:
    print("\u25B6\ufe0f production_plan_node")
    prompt = f"""
You are a production and operations expert.

Based on the company description below, write a realistic **Production Plan**.
Use Markdown format and describe production steps, timelines, technology, equipment, and logistics involved.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"production_plan": result}


def organization_personnel_node(state: State) -> State:
    print("\u25B6\ufe0f organization_personnel_node")
    prompt = f"""
You are an HR and management expert.

Using the company description below, write a professional **Organization and Personnel** section.
Include company structure, number of employees, roles, and hiring plans. Format in Markdown.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"organization_personnel": result}


def investment_plan_node(state: State) -> State:
    print("\u25B6\ufe0f investment_plan_node")
    prompt = f"""
You are a financial investment advisor.

Based on the following description, write a compelling **Investment Plan**.
Include capital required, funding stages, and what the investment will be used for. Use Markdown.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"investment_plan": result}


def income_cashflow_forecast_node(state: State) -> State:
    print("\u25B6\ufe0f income_cashflow_forecast_node")
    prompt = f"""
You are a financial expert.

Based on the company description below, write a detailed **Forecast of Income Statement and Cash Flow**.
Use Markdown format and include key revenue streams, monthly income projections, and expected cash flow.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"income_cashflow_forecast": result}



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


def legal_aspects_node(state: State) -> State:
    print("\u25B6\ufe0f legal_aspects_node")
    prompt = f"""
You are a legal advisor for startups.

Based on the company description, write the **Legal Aspects** section.
Include legal structure, intellectual property, licenses, and regulatory considerations.
Use Markdown format.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"legal_aspects": result}


def risk_assessment_node(state: State) -> State:
    print("\u25B6\ufe0f risk_assessment_node")
    prompt = f"""
You are a business risk consultant.

Using the company description, write a **Risk Assessment** section.
Identify main business risks (financial, operational, market, etc.) and suggest mitigation strategies.
Use Markdown format.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"risk_assessment": result}


def contingency_coverage_node(state: State) -> State:
    print("\u25B6\ufe0f contingency_coverage_node")
    prompt = f"""
You are a strategic planner.

Based on the company description, write a **Main Contingencies and Coverage** section.
List major potential problems and backup plans or strategies for handling them. Use Markdown format.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"contingency_coverage": result}

def csr_node(state: State) -> State:
    print("\u25B6\ufe0f csr_node")
    prompt = f"""
You are a sustainability and ethics advisor.

Based on the company description, write a clear **Corporate Social Responsibility (CSR)** section.
Include environmental goals, social impact, and ethical practices. Use Markdown format.

Company Description:
{state['description']}
"""
    result = ask_llm(prompt)
    return {"csr": result}
