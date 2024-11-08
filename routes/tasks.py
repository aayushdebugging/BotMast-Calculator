from fastapi import APIRouter
from app.models.schemas import AutomationObject
from app.services.analysis import analyze_automation

router = APIRouter()

@router.post("/analyze", response_model=AutomationObject)
def analyze_task(inputs: dict, annual_salary: float):
    return analyze_automation(inputs, annual_salary)
