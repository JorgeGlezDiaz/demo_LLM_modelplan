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

    # Leer número de líneas desde el formulario
    num_lines = int(form_data.get("num_lines", 3))  # Por defecto 3 si no se recibe

    # Leer el modelo seleccionado desde el formulario
    model_name = form_data.get("model", "ollama")

    # Recoger datos de cada línea de negocio
    lines = []
    for i in range(num_lines):
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

    # Ejecutar los grafos por cada línea de negocio (de forma dinámica)
    states = [run_business_plan_pipeline(line, model_name) for line in lines]

    # Combinar los resultados en un plan unificado
    combined_plan = fs_run_business_plan_pipeline(states, model_name)

    return templates.TemplateResponse("business_plan.html", {
        "request": request,
        "multi_results": states,
        "combined_plan": combined_plan["final_markdown"]
    })
