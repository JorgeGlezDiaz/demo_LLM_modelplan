import time
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
    start_time = time.time()

    num_lines = int(form_data.get("num_lines", 3))  # 3 if not put
    model_name = form_data.get("model", "ollama")   # ollama if not put

    lines = []
    for i in range(num_lines):
        model_data = {
            "business_line_name": f"Business Line {i + 1}",
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

    combined_plan = fs_run_business_plan_pipeline(lines, model_name)

    end_time = time.time()  
    duration = end_time - start_time
    minutes = int(duration // 60)
    seconds = int(duration % 60)

    print(f"\n⏱️ Business plan generated in {minutes}m {seconds}s using {model_name.upper()}.\n")
    
    return templates.TemplateResponse("business_plan.html", {
        "request": request,
        "multi_results": combined_plan["raw_data"],
        "combined_plan": combined_plan["final_markdown"]
    })
