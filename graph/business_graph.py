from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from typing_extensions import TypedDict
from typing import Annotated
from agents.langgraph_agent import generate_company_description
from agents.business_plan_agent import (
    market_analysis_node,
    marketing_plan_node,
    financial_plan_node
)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    description: str
    market_analysis: str
    marketing_plan: str
    financial_plan: str
    final_markdown: str

def build_prompt_from_form(data: dict) -> str:                          # Take form data and built a legible promt 
    sections = []
    for key, value in data.items():
        pretty_key = key.replace("_", " ").capitalize()
        sections.append(f"### {pretty_key}\n{value.strip()}")
    return "\n\n".join(sections)                                          # join each section with spaces between them


def company_describer_node(state: State) -> State:
    prompt = state["messages"][-1].content
    description = generate_company_description(prompt)
    return {"description": description}


def merge_to_markdown_node(state: State) -> State:
    markdown = f"""# Business Plan

## Market Analysis
{state.get("market_analysis", "")}

---

## Marketing Plan
{state.get("marketing_plan", "")}

---

## Financial Plan
{state.get("financial_plan", "")}
"""
    return {"final_markdown": markdown}

graph_builder = StateGraph(State)


graph_builder.add_node("company_describer", company_describer_node)
graph_builder.add_node("node_market_analysis", market_analysis_node)
graph_builder.add_node("node_marketing_plan", marketing_plan_node)
graph_builder.add_node("node_financial_plan", financial_plan_node)
graph_builder.add_node("merge_to_markdown", merge_to_markdown_node)

graph_builder.set_entry_point("company_describer")

parallel_nodes = [
    "node_market_analysis",
    "node_marketing_plan",
    "node_financial_plan"
]

for node in parallel_nodes:
    graph_builder.add_edge("company_describer", node)
    graph_builder.add_edge(node, "merge_to_markdown")

graph_builder.set_finish_point("merge_to_markdown")

graph = graph_builder.compile()

def run_business_plan_pipeline(data: dict) -> str:
    initial_prompt = build_prompt_from_form(data)
    
    state = {
        "messages": [HumanMessage(content=initial_prompt)],
        "description": "",
        "market_analysis": "",
        "marketing_plan": "",
        "financial_plan": "",
        "final_markdown": ""
    }

    final_state = graph.invoke(state)
    return final_state["final_markdown"]
