from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage
import json

llm = ChatOllama(model="llama3:latest")


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

class FatherState(TypedDict):
    raw_data: list

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
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()


def convert_input_into_markdown(data: dict) -> str:
    sections = [f"### {k.replace('_', ' ').capitalize()}\n{v.strip()}" for k, v in data.items()]
    return "\n\n".join(sections)


### NODES ###

def convert_form_node(state: dict) -> State:
    raw_data_dict = json.loads(state["raw_data"])  # Ahora sí es un dict correctamente
    result = convert_input_into_markdown(raw_data_dict)
    state["raw_data"] = result
    return state

def company_description_node(state: State) -> State:
    prompt = f"""
You are a business consultant with expertise in startup analysis and pitch preparation.

Carefully read the company's foundational information below and generate a well-structured, detailed, and persuasive **company description** in **Markdown format**. Write between **400-600 words**.

### Guidelines:
- Use a professional, yet engaging tone (like addressing investors).
- Include:
  - What the company does
  - The product/service
  - The market opportunity
  - Target customers
  - Business model and key advantages
  - Competitive positioning
- Structure with clear headings and subheadings.
- Avoid repetition or generalities.

### Founder Input:
{state['raw_data']}

---

Write the full company description below:
"""
    return {"company_description": ask_llm(prompt)}


### BUSINESS PLAN SECTION NODES ###

def executive_summary_node(state: State) -> State:
    prompt = f"""
You are a business strategist and investor pitch expert.

Using the company description below, write an **Executive Summary** in Markdown. It should be persuasive and concise (max 350 words), highlighting:

- A strong opening hook
- The key problem addressed
- The product/service and its core innovation
- Market opportunity
- Unique Value Proposition
- Vision and mission
- Call to action for potential investors

Company Description:
{state['company_description']}
"""
    return {"executive_summary": ask_llm(prompt)}


def project_team_node(state: State) -> State:
    prompt = f"""
You are an HR and startup advisor.

Based on the company description, describe the **Project Promotion Team** in Markdown format. Include:

- Key roles and responsibilities
- Required expertise
- Suggested team structure
- Justification for these roles in early-stage operations

If the original input lacks specifics, infer plausible but realistic startup team members.

Company Description:
{state['company_description']}
"""
    return {"project_team": ask_llm(prompt)}


def product_description_node(state: State) -> State:
    prompt = f"""
You are a product strategy consultant.

Write a detailed **Product or Service Description** in Markdown. Include:

- What it is and how it works
- Features and benefits
- Use cases and scenarios
- Technical and operational aspects
- Value delivered to end-users

Company Description:
{state['company_description']}
"""
    return {"product_description": ask_llm(prompt)}


def market_analysis_node(state: State) -> State:
    prompt = f"""
You are a senior market analyst.

Based on the company description, generate a **Market Analysis** section in Markdown that includes:

- Target customer profile (demographics, behavior, needs)
- Market size and TAM/SAM/SOM if inferable
- Key trends and market dynamics
- Competitor landscape (3-5 key players)
- Competitive advantage and differentiation

Company Description:
{state['company_description']}
"""
    return {"market_analysis": ask_llm(prompt)}


def marketing_plan_node(state: State) -> State:
    prompt = f"""
You are a marketing and growth strategist.

Using the company description, write a **Marketing Plan** in Markdown. Include:

- Positioning and branding strategy
- Customer acquisition channels
- Marketing tactics: SEO, social media, influencers, etc.
- Lead nurturing and conversion funnel
- Budget allocation if applicable
- KPIs and metrics to track

Company Description:
{state['company_description']}
"""
    return {"marketing_plan": ask_llm(prompt)}


def production_plan_node(state: State) -> State:
    prompt = f"""
You are a production and operations expert.

Create a **Production Plan** in Markdown based on the company description. Cover:

- Product/service development phases
- Key operational steps
- Required tools, platforms, technologies
- Timeline estimates (e.g. MVP, beta, full launch)
- Logistics and scalability considerations

Company Description:
{state['company_description']}
"""
    return {"production_plan": ask_llm(prompt)}


def organization_personnel_node(state: State) -> State:
    prompt = f"""
You are an organizational designer for startups.

Write the **Organization and Personnel** section in Markdown. Include:

- Organizational structure
- Core departments and their functions
- Key roles and hiring priorities for Year 1
- Growth plan for staffing

Company Description:
{state['company_description']}
"""
    return {"organization_personnel": ask_llm(prompt)}


def investment_plan_node(state: State) -> State:
    prompt = f"""
You are an investment advisor.

Generate the **Investment Plan** section in Markdown. Include:

- Funding needed (pre-seed, seed, Series A, etc.)
- Use of funds breakdown
- Proposed investor terms or equity
- Expected outcomes from each funding stage

Company Description:
{state['company_description']}
"""
    return {"investment_plan": ask_llm(prompt)}


def income_cashflow_forecast_node(state: State) -> State:
    prompt = f"""
You are a financial modeling expert.

Create a **Forecast of Income Statement and Cash Flow** in Markdown. Include:

- Assumptions (ARPU, CAC, churn, etc.)
- Revenue and cost forecast (Year 1-3)
- Cash inflow and outflow estimates
- Optional tables to support clarity

Company Description:
{state['company_description']}
"""
    return {"income_cashflow_forecast": ask_llm(prompt)}


def financial_plan_node(state: State) -> State:
    prompt = f"""
You are a business financial planner.

Generate a comprehensive **Financial Plan** in Markdown. Include:

- Startup costs and capex
- Operating costs (fixed and variable)
- Revenue streams and pricing logic
- Break-even analysis
- Financial KPIs (ROI, EBITDA margin, gross margin)
- Sensitivity or risk factors

Company Description:
{state['company_description']}
"""
    return {"financial_plan": ask_llm(prompt)}


def legal_aspects_node(state: State) -> State:
    prompt = f"""
You are a legal advisor for startups.

Write the **Legal Aspects** section in Markdown. Include:

- Legal structure (LLC, C-Corp, etc.)
- IP and trademarks
- Contracts or licenses needed
- Regulatory compliance relevant to the market

Company Description:
{state['company_description']}
"""
    return {"legal_aspects": ask_llm(prompt)}


def risk_assessment_node(state: State) -> State:
    prompt = f"""
You are a business risk manager.

Write a **Risk Assessment** in Markdown. Include:

- Key risk categories: market, financial, legal, technical
- How each risk may impact the business
- Mitigation strategies or contingency plans

Company Description:
{state['company_description']}
"""
    return {"risk_assessment": ask_llm(prompt)}


def contingency_coverage_node(state: State) -> State:
    prompt = f"""
You are a strategic operations expert.

Write the **Main Contingencies and Coverage** section in Markdown. List:

- Critical operational risks
- Failover or response strategies
- Backup systems or workflows
- Insurance or financial coverage plans

Company Description:
{state['company_description']}
"""
    return {"contingency_coverage": ask_llm(prompt)}


def csr_node(state: State) -> State:
    prompt = f"""
You are a sustainability and ethics advisor.

Generate a **Corporate Social Responsibility (CSR)** section in Markdown. Include:

- Environmental sustainability plans
- Social/community engagement
- Governance and ethical practices
- Measurable CSR goals if applicable

Company Description:
{state['company_description']}
"""
    return {"csr": ask_llm(prompt)}


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

    markdown = f"# Business Plan\n\n{toc}\n\n{body}"
    return {"final_markdown": markdown}



### BUILD GRAPH ###

graph_builder = StateGraph(State)

graph_builder.add_node("convert_form", convert_form_node)
graph_builder.add_node("company_describer", company_description_node)

# business sections
section_nodes = {
    "node_executive_summary": executive_summary_node,
    "node_project_team": project_team_node,
    "node_product_description": product_description_node,
    "node_market_analysis": market_analysis_node,
    "node_marketing_plan": marketing_plan_node,
    "node_production_plan": production_plan_node,
    "node_organization_personnel": organization_personnel_node,
    "node_investment_plan": investment_plan_node,
    "node_income_cashflow_forecast": income_cashflow_forecast_node,
    "node_financial_plan": financial_plan_node,
    "node_legal_aspects": legal_aspects_node,
    "node_risk_assessment": risk_assessment_node,
    "node_contingency_coverage": contingency_coverage_node,
    "node_csr": csr_node,
}

for name, func in section_nodes.items():
    graph_builder.add_node(name, func)

graph_builder.add_node("merge_to_markdown", merge_to_markdown_node)


# graph logic
graph_builder.set_entry_point("convert_form")
graph_builder.add_edge("convert_form", "company_describer")

for name in section_nodes:
    graph_builder.add_edge("company_describer", name)
    graph_builder.add_edge(name, "merge_to_markdown")


graph_builder.set_finish_point("merge_to_markdown")

graph = graph_builder.compile()


def run_business_plan_pipeline(data: dict) -> State:
    state = State({"raw_data":json.dumps(data)})
    final_state = graph.invoke(state)
    return final_state



##################################

def fs_start_node(state: FatherState) -> FatherState:
    return state

def fs_executive_summary_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into an executive_summary section
Lines:
{data[0]["executive_summary"]}
{data[1]["executive_summary"]}
{data[2]["executive_summary"]}
"""
    return {"executive_summary": ask_llm(prompt)}

def fs_project_team_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a project_team section
Lines:
{data[0]["project_team"]}
{data[1]["project_team"]}
{data[2]["project_team"]}
"""
    return {"project_team": ask_llm(prompt)}

def fs_product_description_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a product_description section
Lines:
{data[0]["product_description"]}
{data[1]["product_description"]}
{data[2]["product_description"]}
"""
    return {"product_description": ask_llm(prompt)}

def fs_market_analysis_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a market_analysis section
Lines:
{data[0]["market_analysis"]}
{data[1]["market_analysis"]}
{data[2]["market_analysis"]}
"""
    return {"market_analysis": ask_llm(prompt)}

def fs_marketing_plan_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a marketing_plan section
Lines:
{data[0]["marketing_plan"]}
{data[1]["marketing_plan"]}
{data[2]["marketing_plan"]}
"""
    return {"marketing_plan": ask_llm(prompt)}

def fs_production_plan_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a production_plan section
Lines:
{data[0]["production_plan"]}
{data[1]["production_plan"]}
{data[2]["production_plan"]}
"""
    return {"production_plan": ask_llm(prompt)}

def fs_organization_personnel_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into an organization_personnel section
Lines:
{data[0]["organization_personnel"]}
{data[1]["organization_personnel"]}
{data[2]["organization_personnel"]}
"""
    return {"organization_personnel": ask_llm(prompt)}

def fs_investment_plan_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into an investment_plan section
Lines:
{data[0]["investment_plan"]}
{data[1]["investment_plan"]}
{data[2]["investment_plan"]}
"""
    return {"investment_plan": ask_llm(prompt)}

def fs_income_cashflow_forecast_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into an income_cashflow_forecast section
Lines:
{data[0]["income_cashflow_forecast"]}
{data[1]["income_cashflow_forecast"]}
{data[2]["income_cashflow_forecast"]}
"""
    return {"income_cashflow_forecast": ask_llm(prompt)}

def fs_financial_plan_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a financial_plan section
Lines:
{data[0]["financial_plan"]}
{data[1]["financial_plan"]}
{data[2]["financial_plan"]}
"""
    return {"financial_plan": ask_llm(prompt)}

def fs_legal_aspects_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a legal_aspects section
Lines:
{data[0]["legal_aspects"]}
{data[1]["legal_aspects"]}
{data[2]["legal_aspects"]}
"""
    return {"legal_aspects": ask_llm(prompt)}

def fs_risk_assessment_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a risk_assessment section
Lines:
{data[0]["risk_assessment"]}
{data[1]["risk_assessment"]}
{data[2]["risk_assessment"]}
"""
    return {"risk_assessment": ask_llm(prompt)}

def fs_contingency_coverage_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a contingency_coverage section
Lines:
{data[0]["contingency_coverage"]}
{data[1]["contingency_coverage"]}
{data[2]["contingency_coverage"]}
"""
    return {"contingency_coverage": ask_llm(prompt)}

def fs_csr_node(state: FatherState) -> FatherState:
    data = state["raw_data"]
    prompt = f"""
Mix this three lines into a csr section
Lines:
{data[0]["csr"]}
{data[1]["csr"]}
{data[2]["csr"]}
"""
    return {"csr": ask_llm(prompt)}


def fs_merge_to_markdown_node(state: FatherState) -> FatherState:
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

    markdown = f"# Business Plan\n\n{toc}\n\n{body}"
    return {"final_markdown": markdown}


graph_builder = StateGraph(FatherState)

graph_builder.add_node("start", fs_start_node)

# business sections
section_nodes = {
    "node_executive_summary": fs_executive_summary_node,
    "node_project_team": fs_project_team_node,
    "node_product_description": fs_product_description_node,
    "node_market_analysis": fs_market_analysis_node,
    "node_marketing_plan": fs_marketing_plan_node,
    "node_production_plan": fs_production_plan_node,
    "node_organization_personnel": fs_organization_personnel_node,
    "node_investment_plan": fs_investment_plan_node,
    "node_income_cashflow_forecast": fs_income_cashflow_forecast_node,
    "node_financial_plan": fs_financial_plan_node,
    "node_legal_aspects": fs_legal_aspects_node,
    "node_risk_assessment": fs_risk_assessment_node,
    "node_contingency_coverage": fs_contingency_coverage_node,
    "node_csr": fs_csr_node,
}

for name, func in section_nodes.items():
    graph_builder.add_node(name, func)

graph_builder.add_node("merge_to_markdown", fs_merge_to_markdown_node)

graph_builder.set_entry_point("start")

for name in section_nodes:
    graph_builder.add_edge("start", name)
    graph_builder.add_edge(name, "merge_to_markdown")

graph_builder.set_finish_point("merge_to_markdown")

fs_graph = graph_builder.compile()


def fs_run_business_plan_pipeline(states: list[State]) -> FatherState:
    father_state = FatherState({"raw_data": states})
    final_state = fs_graph.invoke(father_state)
    return final_state

