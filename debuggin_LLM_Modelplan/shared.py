from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
import operator
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


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
    full_markdown: str



class FatherState(TypedDict):
    num_lines: int
    raw_data: Annotated[list, operator.add]

    executive_summary: Annotated[list[str], operator.add]
    project_team: Annotated[list[str], operator.add]
    product_description: Annotated[list[str], operator.add]
    market_analysis: Annotated[list[str], operator.add]
    marketing_plan: Annotated[list[str], operator.add]
    production_plan: Annotated[list[str], operator.add]
    organization_personnel: Annotated[list[str], operator.add]
    investment_plan: Annotated[list[str], operator.add]
    income_cashflow_forecast: Annotated[list[str], operator.add]
    financial_plan: Annotated[list[str], operator.add]
    legal_aspects: Annotated[list[str], operator.add]
    risk_assessment: Annotated[list[str], operator.add]
    contingency_coverage: Annotated[list[str], operator.add]
    csr: Annotated[list[str], operator.add]
    final_markdown: str
