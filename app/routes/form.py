from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from graph.business_graph import run_business_plan_pipeline


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/application-form")
def get_application_form(request: Request):
    return templates.TemplateResponse("application_form.html", {"request": request})

@router.post("/submit-form")
async def submit_form(
    request: Request,
    product_service: str = Form(...),
    problem_solved: str = Form(...),
    unique_value: str = Form(...),
    target_customer: str = Form(...),
    location: str = Form(...),
    competitors: str = Form(...),
    competitive_advantage: str = Form(...),
    revenue_model: str = Form(...),
    pricing_strategy: str = Form(...),
    key_resources: str = Form(...),
    key_partners: str = Form(...),
    marketing_strategy: str = Form(...),
    sales_channels: str = Form(...),
    initial_costs: str = Form(...),
    expected_revenue: str = Form(...),
    goals: str = Form(...)
):
    data = {
        "product_service": product_service,
        "problem_solved": problem_solved,
        "unique_value": unique_value,
        "target_customer": target_customer,
        "location": location,
        "competitors": competitors,
        "competitive_advantage": competitive_advantage,
        "revenue_model": revenue_model,
        "pricing_strategy": pricing_strategy,
        "key_resources": key_resources,
        "key_partners": key_partners,
        "marketing_strategy": marketing_strategy,
        "sales_channels": sales_channels,
        "initial_costs": initial_costs,
        "expected_revenue": expected_revenue,
        "goals": goals
    }

    markdown_result = run_business_plan_pipeline(data)

    return templates.TemplateResponse("description.html", {
        "request": request,
        "description": markdown_result  
    })
