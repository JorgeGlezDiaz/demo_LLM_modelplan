from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.graph.langgraph_business_model import run_business_plan_pipeline

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/application-form")
def get_application_form(request: Request):
    return templates.TemplateResponse("application_form.html", {"request": request})

@router.post("/submit-form")
async def submit_form(request: Request):
    form_data = await request.form()

    # Crea claramente 3 sets de datos distintos (A, B, C)
    lines = []
    for i in range(3):
        model_data = {
            "customer_segments": form_data.get(f"customer_segments_{i}", ""),
            "value_propositions": form_data.get(f"value_propositions_{i}", ""),
            "channels": form_data.get(f"channels_{i}", ""),
            "customer_relationships": form_data.get(f"customer_relationships_{i}", ""),
            "revenue_streams": form_data.get(f"revenue_streams_{i}", ""),
            "key_resources": form_data.get(f"key_resources_{i}", ""),
            "key_activities": form_data.get(f"key_activities_{i}", ""),
            "key_partnerships": form_data.get(f"key_partnerships_{i}", ""),
            "cost_structure": form_data.get(f"cost_structure_{i}", "")
        }
        lines.append(model_data)

    # Procesa cada línea por separado con tu pipeline y guarda en estados separados claramente
    business_plan_1 = run_business_plan_pipeline(lines[0])
    business_plan_2 = run_business_plan_pipeline(lines[1])
    business_plan_3 = run_business_plan_pipeline(lines[2])

    # Muestra resultados en consola claramente para verificar
    print("State1 description:", business_plan_1["company_description"])
    print("State2 description:", business_plan_2["company_description"])
    print("State3 description:", business_plan_3["company_description"])

    # Puedes devolverlos claramente a la plantilla HTML también
    return templates.TemplateResponse("business_plan.html", {
        "request": request,
        "multi_results": [business_plan_1, business_plan_2, business_plan_3]
    })
