from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.graph.langgraph_business_model import run_business_plan_pipeline, fs_run_business_plan_pipeline

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/application-form")
def get_application_form(request: Request):
    return templates.TemplateResponse("application_form.html", {"request": request})

@router.post("/submit-form")
async def submit_form(request: Request):
    form_data = await request.form()

    # Extrae datos del formulario para cada línea de negocio (A, B, C)
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

    # Procesa cada línea por separado con el grafo individual
    state_1 = run_business_plan_pipeline(lines[0])
    state_2 = run_business_plan_pipeline(lines[1])
    state_3 = run_business_plan_pipeline(lines[2])

    # Procesa el plan de negocio combinado usando los 3 resultados anteriores
    combined_plan = fs_run_business_plan_pipeline([state_1, state_2, state_3])

    return templates.TemplateResponse("business_plan.html", {
        "request": request,
        "multi_results": [state_1, state_2, state_3],
        "combined_plan": combined_plan["final_markdown"]
    })
