# langgraph_agente.py
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage

llm = ChatOllama(model="llama3:latest")

def generate_company_description(prompt: str) -> str:
    full_prompt = f"""
You are a business analyst and startup expert.
Read the following information provided by a founder and generate a **detailed description of the company**.
Use a professional tone, Markdown format, and write at least 400-600 words.

Company Information:
{prompt}
"""
    response = llm.invoke([HumanMessage(content=full_prompt)])
    return response.content.strip()
