
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage
from typing_extensions import Annotated
from dotenv import load_dotenv
import operator
import time
import json
import os
from shared import  State
from lines_nodes import *
from fs_nodes import (
    fs_start_node,
    fs_executive_summary_node,
    fs_project_team_node,
    fs_product_description_node,
    fs_market_analysis_node,
    fs_marketing_plan_node,
    fs_production_plan_node,
    fs_organization_personnel_node,
    fs_investment_plan_node,
    fs_income_cashflow_forecast_node,
    fs_financial_plan_node,
    fs_legal_aspects_node,
    fs_risk_assessment_node,
    fs_contingency_coverage_node,
    fs_csr_node,
    fs_merge_to_markdown_node
)
from shared import FatherState


lines = [
    {
        'business_line_name': 'Business Line 1',
        'customer_segments': 'ATRINEO serves prestigious scientific institutions such as universities, research centers, and innovation-driven companies. These clients seek strategic consulting, operational support, and intellectual property management systems.',
        'value_propositions': 'Offers expert consulting and IT solutions for knowledge and technology transfer, guiding organizations from research to market through tailored innovation strategies and capacity-building.',
        'channels': 'Direct consulting engagements, strategic partnerships, conference presentations, publication of whitepapers, and participation in innovation alliances.',
        'customer_relationships': 'Maintains trust-based, personalized relationships through tailored support, training, and measurable innovation outcomes.',
        'revenue_streams': 'Consulting fees, IT system licensing, training program revenues, and workshop facilitation.',
        'key_resources': 'Consulting talent, proprietary methodologies, a strong institutional network, and reputation in European innovation ecosystems.',
        'key_activities': 'Developing innovation strategies, performing feasibility studies, managing IT systems, and delivering training programs.',
        'key_partnerships': 'Collaborates with universities, research hubs, innovation agencies, and international knowledge networks.',
        'cost_structure': 'Salaries for consultants, IT system development, training content creation, and event participation.'
    },
    {
        'business_line_name': 'Business Line 2',
        'customer_segments': 'ATRINEO’s waste management line targets urban municipalities and commercial property managers in need of sustainable solutions. Their key needs include regulatory compliance, environmental impact reduction, and cost optimization.',
        'value_propositions': 'Delivers integrated, eco-friendly waste management systems that reduce environmental impact, comply with regulations, and increase operational efficiency through smart technologies.',
        'channels': 'Direct sales to municipalities, collaborations with environmental groups, email campaigns, trade shows, and sustainability-focused webinars.',
        'customer_relationships': 'Builds long-term contracts supported by proactive communication, regulatory updates, and dedicated service teams.',
        'revenue_streams': 'Subscriptions for waste services, equipment sales, sustainability audits, and service contracts.',
        'key_resources': 'Specialized waste technology, environmental engineers, compliance expertise, and sustainability tracking tools.',
        'key_activities': 'Conducting waste audits, installing systems, ensuring compliance, and improving recycling processes.',
        'key_partnerships': 'Works with NGOs, regulators, recycling tech providers, and public sector stakeholders.',
        'cost_structure': 'Equipment costs, maintenance, staff salaries, regulatory work, and ongoing R&D for green tech.'
    },
    {
        'business_line_name': 'Business Line 3',
        'customer_segments': 'ATRINEO´s wellness tech division targets young professionals and fitness enthusiasts aged 20-40 looking for personalized, digital-first fitness and nutrition guidance.',
        'value_propositions': 'Provides an AI-powered mobile app that delivers personalized workout and nutrition plans based on user data, preferences, and health goals.',
        'channels': 'Digital marketing via influencers, SEO-rich content, app store optimization, and partnerships with wellness brands and gyms.',
        'customer_relationships': 'Leverages digital-first, interactive relationships with AI-driven personalization, in-app support, and community engagement.',
        'revenue_streams': 'Freemium mobile subscriptions, premium plan upgrades, sponsored content, and affiliate programs.',
        'key_resources': 'AI/ML algorithms, app development team, expert content creators, and cloud infrastructure.',
        'key_activities': 'Developing the app, producing content, refining algorithms, and supporting customers.',
        'key_partnerships': 'Partners with fitness influencers, gyms, nutritionists, wellness brands, and tech platforms like Apple Health.',
        'cost_structure': 'Software development, server costs, marketing, content creation, and user acquisition.'
    }
]


def line_a_business_plan_node(state: FatherState) -> FatherState:
    result = business_plan(lines[0])
    state["raw_data"].append(result)
    return state

def line_b_business_plan_node(state: FatherState) -> FatherState:
    result = business_plan(lines[1])
    state["raw_data"].append(result)
    return state

def line_c_business_plan_node(state: FatherState) -> FatherState:
    result = business_plan(lines[2])
    state["raw_data"].append(result)
    return state


def union(state: FatherState) -> FatherState:
    return state


# GRAPH OF BUSINESS LINES

graph_builder = StateGraph(State)

graph_builder.add_node("convert_form", convert_form_node)
graph_builder.add_node("company_describer", company_description_node)

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

graph_builder.add_node("merge_sections", merge_sections_node)

graph_builder.set_entry_point("convert_form")

# --- EDGES ---

graph_builder.add_edge("convert_form", "company_describer")

graph_builder.add_edge("company_describer", "node_executive_summary")
graph_builder.add_edge("company_describer", "node_project_team")
graph_builder.add_edge("company_describer", "node_product_description")
graph_builder.add_edge("company_describer", "node_market_analysis")
graph_builder.add_edge("company_describer", "node_marketing_plan")
graph_builder.add_edge("company_describer", "node_production_plan")
graph_builder.add_edge("company_describer", "node_organization_personnel")
graph_builder.add_edge("company_describer", "node_investment_plan")
graph_builder.add_edge("company_describer", "node_income_cashflow_forecast")
graph_builder.add_edge("company_describer", "node_financial_plan")
graph_builder.add_edge("company_describer", "node_legal_aspects")
graph_builder.add_edge("company_describer", "node_risk_assessment")
graph_builder.add_edge("company_describer", "node_contingency_coverage")
graph_builder.add_edge("company_describer", "node_csr")

graph_builder.add_edge("node_executive_summary", "merge_sections")
graph_builder.add_edge("node_project_team", "merge_sections")
graph_builder.add_edge("node_product_description", "merge_sections")
graph_builder.add_edge("node_market_analysis", "merge_sections")
graph_builder.add_edge("node_marketing_plan", "merge_sections")
graph_builder.add_edge("node_production_plan", "merge_sections")
graph_builder.add_edge("node_organization_personnel", "merge_sections")
graph_builder.add_edge("node_investment_plan", "merge_sections")
graph_builder.add_edge("node_income_cashflow_forecast", "merge_sections")
graph_builder.add_edge("node_financial_plan", "merge_sections")
graph_builder.add_edge("node_legal_aspects", "merge_sections")
graph_builder.add_edge("node_risk_assessment", "merge_sections")
graph_builder.add_edge("node_contingency_coverage", "merge_sections")
graph_builder.add_edge("node_csr", "merge_sections")


lines_graph = graph_builder.compile()



def business_plan(data) -> State:

    state = State({"raw_data": json.dumps(data)})

    return lines_graph.invoke(state)



def run_business_line_a(state: FatherState) -> FatherState:
    result = business_plan(lines[0])
    state["raw_data"].append(result)
    return state

def run_business_line_b(state: FatherState) -> FatherState:
    result = business_plan(lines[1])
    state["raw_data"].append(result)
    return state

def run_business_line_c(state: FatherState) -> FatherState:
    result = business_plan(lines[2])
    state["raw_data"].append(result)
    return state

from typing import Optional

def condition_line_a(state: FatherState) -> Optional[str]:
    return "run_business_line_a"  

def condition_line_b(state: FatherState) -> Optional[str]:
    if state.get("num_lines", 0) >= 2:
        return "run_business_line_b"
    return None

def condition_line_c(state: FatherState) -> Optional[str]:
    if state.get("num_lines", 0) >= 3:
        return "run_business_line_c"
    return None


fs_graph = StateGraph(FatherState)

# Add nodes
fs_graph.add_node("start", fs_start_node)

fs_graph.add_node("run_business_line_a",run_business_line_a)
fs_graph.add_node("run_business_line_b",run_business_line_b)
fs_graph.add_node("run_business_line_c",run_business_line_c)

fs_graph.add_node("union",union)

fs_graph.add_node("fs_executive_summary", fs_executive_summary_node)
fs_graph.add_node("fs_project_team", fs_project_team_node)
fs_graph.add_node("fs_product_description", fs_product_description_node)
fs_graph.add_node("fs_market_analysis", fs_market_analysis_node)
fs_graph.add_node("fs_marketing_plan", fs_marketing_plan_node)
fs_graph.add_node("fs_production_plan", fs_production_plan_node)
fs_graph.add_node("fs_organization_personnel", fs_organization_personnel_node)
fs_graph.add_node("fs_investment_plan", fs_investment_plan_node)
fs_graph.add_node("fs_income_cashflow_forecast", fs_income_cashflow_forecast_node)
fs_graph.add_node("fs_financial_plan", fs_financial_plan_node)
fs_graph.add_node("fs_legal_aspects", fs_legal_aspects_node)
fs_graph.add_node("fs_risk_assessment", fs_risk_assessment_node)
fs_graph.add_node("fs_contingency_coverage", fs_contingency_coverage_node)
fs_graph.add_node("fs_csr", fs_csr_node)
fs_graph.add_node("fs_merge_to_markdown", fs_merge_to_markdown_node)

# Entry point
fs_graph.set_entry_point("start")

fs_graph.add_conditional_edges("start", [
    (condition_line_a, "run_business_line_a"),
    (condition_line_b, "run_business_line_b"),
    (condition_line_c, "run_business_line_c"),
])

fs_graph.add_edge("run_business_line_a", "union")
fs_graph.add_edge("run_business_line_b", "union")
fs_graph.add_edge("run_business_line_c", "union")

fs_graph.add_edge("union", "fs_executive_summary")
fs_graph.add_edge("union", "fs_project_team")
fs_graph.add_edge("union", "fs_product_description")
fs_graph.add_edge("union", "fs_market_analysis")
fs_graph.add_edge("union", "fs_marketing_plan")
fs_graph.add_edge("union", "fs_production_plan")
fs_graph.add_edge("union", "fs_organization_personnel")
fs_graph.add_edge("union", "fs_investment_plan")
fs_graph.add_edge("union", "fs_income_cashflow_forecast")
fs_graph.add_edge("union", "fs_financial_plan")
fs_graph.add_edge("union", "fs_legal_aspects")
fs_graph.add_edge("union", "fs_risk_assessment")
fs_graph.add_edge("union", "fs_contingency_coverage")
fs_graph.add_edge("union", "fs_csr")

# All fs nodes go into final markdown node
fs_graph.add_edge("fs_executive_summary", "fs_merge_to_markdown")
fs_graph.add_edge("fs_project_team", "fs_merge_to_markdown")
fs_graph.add_edge("fs_product_description", "fs_merge_to_markdown")
fs_graph.add_edge("fs_market_analysis", "fs_merge_to_markdown")
fs_graph.add_edge("fs_marketing_plan", "fs_merge_to_markdown")
fs_graph.add_edge("fs_production_plan", "fs_merge_to_markdown")
fs_graph.add_edge("fs_organization_personnel", "fs_merge_to_markdown")
fs_graph.add_edge("fs_investment_plan", "fs_merge_to_markdown")
fs_graph.add_edge("fs_income_cashflow_forecast", "fs_merge_to_markdown")
fs_graph.add_edge("fs_financial_plan", "fs_merge_to_markdown")
fs_graph.add_edge("fs_legal_aspects", "fs_merge_to_markdown")
fs_graph.add_edge("fs_risk_assessment", "fs_merge_to_markdown")
fs_graph.add_edge("fs_contingency_coverage", "fs_merge_to_markdown")
fs_graph.add_edge("fs_csr", "fs_merge_to_markdown")

# Compile it
compiled_fs_graph = fs_graph.compile()


initial_state: FatherState = {
    "num_lines": len(lines),
    "raw_data": [],
    "executive_summary": "",
    "project_team": "",
    "product_description": "",
    "market_analysis": "",
    "marketing_plan": "",
    "production_plan": "",
    "organization_personnel": "",
    "investment_plan": "",
    "income_cashflow_forecast": "",
    "financial_plan": "",
    "legal_aspects": "",
    "risk_assessment": "",
    "contingency_coverage": "",
    "csr": "",
    "final_markdown": ""
}

result = compiled_fs_graph.invoke(initial_state)


print("\n===== FINAL BUSINESS PLAN =====\n")
print(result["final_markdown"])