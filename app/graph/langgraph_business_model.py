from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage


llm = ChatOllama(model="llama3.2:latest")

class State(TypedDict):

    raw_data: str
    company_description: str

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


### Functions ###


def ask_llm(prompt: str) -> str:
    response = llm.invoke([HumanMessage(content=prompt)])   # response of the llm
    return response.content.strip()                         # clean with no spaces



def convert_input_into_markdown(data: dict) -> str:                            # Take form data and built a legible promt 
    sections = []

    for key, value in data.items():

        pretty_key = key.replace("_", " ").capitalize()
        sections.append(f"### {pretty_key}\n{value.strip()}")             # ### as markdown section

    return "\n\n".join(sections)                                          # join each section with spaces between them


### NODES ###


def convert_form_node(state: dict) -> State:

    result = convert_input_into_markdown(state["raw_data"])  
    return {"raw_data": result}


def company_description_node(state: State) -> State:
    prompt = f"""

You are a business consultant with expertise in startups and venture analysis.

Your task is to carefully read the following company information provided by a founder and generate a 
**professional and detailed company description** of at least **400-600 words**, in **Markdown** format.

---

📄 **Guidelines:**

- Use a formal and informative tone.
- Avoid repetition and generic phrases.
- Include relevant details about the product/service, the market opportunity, target audience, business model, and competitive advantage.
- Organize your answer with headers and subheaders using Markdown.
- The text should be engaging and suitable for an investor or stakeholder presentation.

---

📬 **Company Input**:
{state['raw_data']}

---

✍️ Now generate the full company description below:
"""
    result = ask_llm(prompt)
    return {"company_description": result}

########## PARALEL NODES ###########


def executive_summary_node(state: State) -> State:

    prompt = f"""
You are a business strategist.

Based on the company description below, write an insightful and persuasive **Executive Summary**.
Use Markdown formatting and include the mission, vision, core offering, and unique value proposition.
Make sure it feels like an elevator pitch to investors.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"executive_summary": result}



def project_team_node(state: State) -> State:

    prompt = f"""
You are an HR and startup consultant.

Using the company description below, describe the **Project Promotion Team**.
Include roles, responsibilities, relevant experience, and key strengths of the founding members.
Use Markdown format, and if team details are missing, infer plausible structure.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"project_team": result}



def product_description_node(state: State) -> State:

    prompt = f"""
You are a product development expert.

Based on the company description below, write a clear and compelling **Description of the Product or Service**.
Use Markdown format and include features, benefits, use cases, and technological aspects if relevant.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"product_description": result}



def market_analysis_node(state: State) -> State:

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
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"market_analysis": result}



def marketing_plan_node(state: State) -> State:

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
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"marketing_plan": result}



def production_plan_node(state: State) -> State:

    prompt = f"""
You are a production and operations expert.

Based on the company description below, write a realistic **Production Plan**.
Use Markdown format and describe production steps, timelines, technology, equipment, and logistics involved.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"production_plan": result}


def organization_personnel_node(state: State) -> State:

    prompt = f"""
You are an HR and management expert.

Using the company description below, write a professional **Organization and Personnel** section.
Include company structure, number of employees, roles, and hiring plans. Format in Markdown.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"organization_personnel": result}



def investment_plan_node(state: State) -> State:

    prompt = f"""
You are a financial investment advisor.

Based on the following description, write a compelling **Investment Plan**.
Include capital required, funding stages, and what the investment will be used for. Use Markdown.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"investment_plan": result}



def income_cashflow_forecast_node(state: State) -> State:

    prompt = f"""
You are a financial expert.

Based on the company description below, write a detailed **Forecast of Income Statement and Cash Flow**.
Use Markdown format and include key revenue streams, monthly income projections, and expected cash flow.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"income_cashflow_forecast": result}



def financial_plan_node(state: State) -> State:

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
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"financial_plan": result}



def legal_aspects_node(state: State) -> State:

    prompt = f"""
You are a legal advisor for startups.

Based on the company description, write the **Legal Aspects** section.
Include legal structure, intellectual property, licenses, and regulatory considerations.
Use Markdown format.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"legal_aspects": result}



def risk_assessment_node(state: State) -> State:

    prompt = f"""
You are a business risk consultant.

Using the company description, write a **Risk Assessment** section.
Identify main business risks (financial, operational, market, etc.) and suggest mitigation strategies.
Use Markdown format.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)
    
    return {"risk_assessment": result}



def contingency_coverage_node(state: State) -> State:

    prompt = f"""
You are a strategic planner.

Based on the company description, write a **Main Contingencies and Coverage** section.
List major potential problems and backup plans or strategies for handling them. Use Markdown format.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"contingency_coverage": result}



def csr_node(state: State) -> State:

    prompt = f"""
You are a sustainability and ethics advisor.

Based on the company description, write a clear **Corporate Social Responsibility (CSR)** section.
Include environmental goals, social impact, and ethical practices. Use Markdown format.

Company Description:
{state['company_description']}
"""
    result = ask_llm(prompt)

    return {"csr": result}


######################################################################################################


def merge_to_markdown_node(state: State) -> State:
    sections = [
        "executive_summary",
        "project_team",
        "product_description",
        "market_analysis",
        "marketing_plan",
        "production_plan",
        "organization_personnel",
        "investment_plan",
        "income_cashflow_forecast",
        "financial_plan",
        "legal_aspects",
        "risk_assessment",
        "contingency_coverage",
        "csr"
    ]

    toc = "## Table of Contents\n"
    body = ""

    for idx, section in enumerate(sections, 1):
        title = section.replace("_", " ").title()
        content = state.get(section, "*No content available.*")

        toc += f"{idx}. {title}\n"
        body += f"\n## {idx}. {title}\n{content}\n\n---\n"

    markdown = f"# Business Plan\n\n{toc}\n{body}"
    return {"final_markdown": markdown}


### langgraph Graph Builder ###

graph_builder = StateGraph(State)

graph_builder.add_node("convert_form", convert_form_node)
graph_builder.add_node("company_describer", company_description_node)


### <business_plan_sections nodes> ###

graph_builder.add_node("node_executive_summary", executive_summary_node)
graph_builder.add_node("node_project_team", project_team_node)
graph_builder.add_node("node_product_description", product_description_node)
graph_builder.add_node("node_market_analysis", market_analysis_node)
graph_builder.add_node("node_marketing_plan", marketing_plan_node)
graph_builder.add_node("node_production_plan", production_plan_node)
graph_builder.add_node("node_organization_personnel", organization_personnel_node)
graph_builder.add_node("node_investment_plan", investment_plan_node)
graph_builder.add_node("node_income_cashflow_forecast", income_cashflow_forecast_node)
graph_builder.add_node("node_financial_plan", financial_plan_node)
graph_builder.add_node("node_legal_aspects", legal_aspects_node)
graph_builder.add_node("node_risk_assessment", risk_assessment_node)
graph_builder.add_node("node_contingency_coverage", contingency_coverage_node)
graph_builder.add_node("node_csr", csr_node)

### </business_plan_sections nodes> ###

graph_builder.add_node("merge_to_markdown", merge_to_markdown_node)


graph_builder.set_entry_point("convert_form")
graph_builder.add_edge("convert_form", "company_describer")

business_plan_sections = [
    "node_executive_summary",
    "node_project_team",
    "node_product_description",
    "node_market_analysis",
    "node_marketing_plan",
    "node_production_plan",
    "node_organization_personnel",
    "node_investment_plan",
    "node_income_cashflow_forecast",
    "node_financial_plan",
    "node_legal_aspects",
    "node_risk_assessment",
    "node_contingency_coverage",
    "node_csr"
]

for node in business_plan_sections:
    graph_builder.add_edge("company_describer", node)
    graph_builder.add_edge(node, "merge_to_markdown")

graph_builder.set_finish_point("merge_to_markdown")

graph = graph_builder.compile()

def run_business_plan_pipeline(data: dict) -> dict:
    return graph.invoke({"raw_data": data})
