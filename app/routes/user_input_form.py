from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from app.graph.langgraph_business_model import run_business_plan_pipeline

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/application-form")
def get_application_form(request: Request):
    return templates.TemplateResponse("application_form.html", {"request": request})

@router.post("/submit-form")
async def submit_form(
    request: Request,
    customer_segments: str = Form(...),
    value_propositions: str = Form(...),
    channels: str = Form(...),
    customer_relationships: str = Form(...),
    revenue_streams: str = Form(...),
    key_resources: str = Form(...),
    key_activities: str = Form(...),
    key_partnerships: str = Form(...),
    cost_structure: str = Form(...),
    profit: str = Form(...)
):
    data = {
        "customer_segments": customer_segments,
        "value_propositions": value_propositions,
        "channels": channels,
        "customer_relationships": customer_relationships,
        "revenue_streams": revenue_streams,
        "key_resources": key_resources,
        "key_activities": key_activities,
        "key_partnerships": key_partnerships,
        "cost_structure": cost_structure,
        "profit": profit
    }

    markdown_result = run_business_plan_pipeline(data)

    return templates.TemplateResponse("business_plan.html", {
        "request": request,
        "description": markdown_result["final_markdown"]
    })
