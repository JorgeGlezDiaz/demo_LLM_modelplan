from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatOpenAI
from langgraph.graph import StateGraph
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage
from typing_extensions import Annotated
from dotenv import load_dotenv
import operator
import time
import json
import os
from lines_nodes import ask_llm
from shared import FatherState


def fs_start_node(state: FatherState) -> FatherState:
    return state

def join_field_from_states(state: FatherState, field: str) -> str:
    result = []
    for linea in state["raw_data"]:
        if field in linea:
            result.append(linea[field])
        else:
            result.append(f"*Field '{field}' not found.*")
    join_text = "\n\n".join(result)
    return join_text


def fs_executive_summary_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a business analyst.

You are given multiple executive summaries (each corresponding to a line of business from the same company). 

Write a **combined executive summary** that unifies the key ideas, strategy and messaging into one single powerful summary in Markdown.

Summaries:
{join_field_from_states(state, "executive_summary")}
"""
    return {"executive_summary": [ask_llm(prompt)]}


def fs_project_team_node(state: FatherState) -> FatherState:
    prompt = f"""
You are an HR strategist. Combine the project team descriptions below into one clear and coherent **Project Promotion Team** section in Markdown.

Descriptions:
{join_field_from_states(state, "project_team")}
"""
    return {"project_team": [ask_llm(prompt)]}


def fs_product_description_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a product strategist. Merge the product/service descriptions below into a single, unified **Product or Service Description** in Markdown.

Descriptions:
{join_field_from_states(state, "product_description")}
"""
    return {"product_description": [ask_llm(prompt)]}


def fs_market_analysis_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a market analyst. Combine the market analyses below into a single, insightful **Market Analysis** in Markdown format.

Analyses:
{join_field_from_states(state, "market_analysis")}
"""
    return {"market_analysis": [ask_llm(prompt)]}


def fs_marketing_plan_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a marketing consultant. Merge the following marketing plans into one strategic and actionable **Marketing Plan** in Markdown.

Plans:
{join_field_from_states(state, "marketing_plan")}
"""
    return {"marketing_plan": [ask_llm(prompt)]}


def fs_production_plan_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a production expert. Consolidate the production plans below into one cohesive **Production Plan** in Markdown format.

Plans:
{join_field_from_states(state, "production_plan")}
"""
    return {"production_plan": [ask_llm(prompt)]}


def fs_organization_personnel_node(state: FatherState) -> FatherState:
    prompt = f"""
You are an organizational consultant. Merge the organizational and HR strategies into one consistent **Organization and Personnel** section in Markdown.

Descriptions:
{join_field_from_states(state, "organization_personnel")}
"""
    return {"organization_personnel": [ask_llm(prompt)]}


def fs_investment_plan_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a startup investment advisor. Unify the investment strategies below into a clear and structured **Investment Plan** in Markdown.

Plans:
{join_field_from_states(state, "investment_plan")}
"""
    return {"investment_plan": [ask_llm(prompt)]}


def fs_income_cashflow_forecast_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a financial analyst. Combine the income and cash flow forecasts into a single, realistic **Forecast of Income Statement and Cash Flow** in Markdown.

Forecasts:
{join_field_from_states(state, "income_cashflow_forecast")}
"""
    return {"income_cashflow_forecast": [ask_llm(prompt)]}


def fs_financial_plan_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a financial planner. Merge the financial strategies below into a unified, coherent **Financial Plan** in Markdown.

Plans:
{join_field_from_states(state, "financial_plan")}
"""
    return {"financial_plan": [ask_llm(prompt)]}


def fs_legal_aspects_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a legal advisor. Combine the legal frameworks and requirements below into one consistent **Legal Aspects** section in Markdown.

Notes:
{join_field_from_states(state, "legal_aspects")}
"""
    return {"legal_aspects": [ask_llm(prompt)]}


def fs_risk_assessment_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a risk manager. Merge the risk assessments from each business line into one integrated **Risk Assessment** section in Markdown.

Assessments:
{join_field_from_states(state, "risk_assessment")}
"""
    return {"risk_assessment": [ask_llm(prompt)]}


def fs_contingency_coverage_node(state: FatherState) -> FatherState:
    prompt = f"""
You are an operations strategist. Consolidate the contingency plans into a comprehensive **Contingency Coverage** section in Markdown.

Plans:
{join_field_from_states(state, "contingency_coverage")}
"""
    return {"contingency_coverage": [ask_llm(prompt)]}


def fs_csr_node(state: FatherState) -> FatherState:
    prompt = f"""
You are a CSR expert. Merge the CSR strategies and commitments from each business line into a unified **Corporate Social Responsibility (CSR)** section in Markdown.

Details:
{join_field_from_states(state, "csr")}
"""
    return {"csr": [ask_llm(prompt)]}


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
        content = "\n\n".join(state.get(section, [])) or "*No content available.*"
        toc += f"{idx}. {title}\n"
        body += f"\n## {idx}. {title}\n{content}\n\n---\n"

    markdown = f"# Business Plan\n\n{toc}\n\n{body}"
    return {"final_markdown": markdown}
