from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from agents.langgraph_agent import generate_company_description
from agents.business_plan_agent import (
    executive_summary_node,
    project_team_node,
    product_description_node,
    market_analysis_node,
    marketing_plan_node,
    production_plan_node,
    organization_personnel_node,
    investment_plan_node,
    income_cashflow_forecast_node,
    financial_plan_node,
    legal_aspects_node,
    risk_assessment_node,
    contingency_coverage_node,
    csr_node
)


class State(TypedDict):
    #messages: Annotated[list, add_messages]
    raw_data: str
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


def convert_input_into_markdown(data: dict) -> str:                            # Take form data and built a legible promt 
    sections = []
    for key, value in data.items():
        pretty_key = key.replace("_", " ").capitalize()
        sections.append(f"### {pretty_key}\n{value.strip()}")             # ### as markdown section
    return "\n\n".join(sections)                                          # join each section with spaces between them

 

def company_describer_node(state: State) -> State:                  ### make two nodes ####
    markdown = convert_input_into_markdown(state["raw_data"])
    description = generate_company_description(markdown)

    return {"description": description}


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
        anchor = title.lower().replace(" ", "-")
        content = state.get(section, "*No content available.*")

        toc += f"{idx}. {title}\n"
        body += f"\n## {idx}. {title}\n{content}\n\n---\n"

    markdown = f"# Business Plan\n\n{toc}\n{body}"
    return {"final_markdown": markdown}


graph_builder = StateGraph(State)


graph_builder.add_node("company_describer", company_describer_node)
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
graph_builder.add_node("merge_to_markdown", merge_to_markdown_node)

graph_builder.set_entry_point("company_describer")

parallel_nodes = [
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

for node in parallel_nodes:
    graph_builder.add_edge("company_describer", node)
    graph_builder.add_edge(node, "merge_to_markdown")

graph_builder.set_finish_point("merge_to_markdown")

graph = graph_builder.compile()

def run_business_plan_pipeline(data: dict) -> str:
    final_state = graph.invoke({"raw_data":data})
    return final_state["final_markdown"]
