from pydantic import BaseModel
from typing import List

class TaskBreakdown(BaseModel):
    step: str
    percentage: float

class TimeAnalysis(BaseModel):
    hours_per_task: float
    times_per_month: int
    hours_per_year_before: float
    hours_per_year_after: float
    hours_saved_per_year: float

class CostProjections(BaseModel):
    average_annual_salary: float
    hourly_rate: float
    monthly_task_cost: float
    annual_task_cost: float

class ROIAnalysis(BaseModel):
    percentage: float
    calculation_basis: str

class AutomationObject(BaseModel):
    job_title: str
    location: str
    company_activity: str
    task_description: str
    found_salary_data: List[float]
    task_steps: List[TaskBreakdown]
    time_analysis: TimeAnalysis
    cost_projections: CostProjections
    roi_analysis: ROIAnalysis
