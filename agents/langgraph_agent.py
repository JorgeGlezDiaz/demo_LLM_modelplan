from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(model="llama3.2:latest")

def generate_company_description(prompt: str) -> str:
    full_prompt = f"""

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
{prompt}

---

✍️ Now generate the full company description below:
"""
    response = llm.invoke([HumanMessage(content=full_prompt)])
    return response.content.strip()
