from langchain_community.chat_models import ChatOpenAI
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
    raw_data: Annotated[list, operator.add]

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