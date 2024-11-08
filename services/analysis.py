from app.models.schemas import CostProjections, TimeAnalysis, ROIAnalysis, AutomationObject, TaskBreakdown
from app.utils.parse_utils import parse_task_steps, parse_roi_response
from typing import Dict, List
import os
from groq import Groq

def calculate_task_costs(annual_salary: float, hours_per_task: float, times_per_month: int) -> CostProjections:
    hourly_rate = annual_salary / 2080
    monthly_task_hours = hours_per_task * times_per_month
    monthly_task_cost = hourly_rate * monthly_task_hours
    annual_task_cost = monthly_task_cost * 12
    return CostProjections(
        average_annual_salary=annual_salary,
        hourly_rate=hourly_rate,
        monthly_task_cost=monthly_task_cost,
        annual_task_cost=annual_task_cost
    )

def analyze_automation(inputs: Dict[str, any], annual_salary: float) -> AutomationObject:
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))

    # Task Breakdown Prompt
    task_breakdown_prompt = f"""
    Analyze the following task and break it down into component steps.

    BUSINESS CONTEXT:
    Role: {inputs['job_query']}
    Company Activity: {inputs['company_activity']}
    Task Description: {inputs['task_description']}
    Time Investment: {inputs['hours_per_task']} hours/task, {inputs['times_per_month']} times/month
    Annual Cost: ${annual_salary:,.2f}

    TASK STEPS (Breakdown):
    Step 1: [specific step name] | [percentage]%
    Ensure total equals 100% and provide 3-5 steps.
    """

    breakdown_response = client.chat.completions.create(
        messages=[{"role": "user", "content": task_breakdown_prompt}],
        model="llama3-70b-8192",
        temperature=0.7,
    )
    task_steps = parse_task_steps(breakdown_response.choices[0].message.content)

    # Time Analysis
    time_analysis = TimeAnalysis(
        hours_per_task=inputs['hours_per_task'],
        times_per_month=inputs['times_per_month'],
        hours_per_year_before=inputs['hours_per_task'] * inputs['times_per_month'] * 12,
        hours_per_year_after=(inputs['hours_per_task'] * inputs['times_per_month'] * 12) * 0.5,
        hours_saved_per_year=(inputs['hours_per_task'] * inputs['times_per_month'] * 12) * 0.5
    )

    # ROI Prompt
    roi_prompt = f"""
    Based on the task breakdown above, calculate the ROI in percentage terms.
    - Cost reduction: ${time_analysis.hours_saved_per_year * (annual_salary / 2080):,.2f}
    - Time saved: {time_analysis.hours_saved_per_year} hours

    Respond with:
    ROI: [percentage]%
    Calculation Basis: [brief basis]
    """

    roi_response = client.chat.completions.create(
        messages=[{"role": "user", "content": roi_prompt}],
        model="llama3-70b-8192",
        temperature=0.7,
    )
    roi_analysis = parse_roi_response(roi_response.choices[0].message.content)

    cost_projections = calculate_task_costs(
        annual_salary, inputs['hours_per_task'], inputs['times_per_month']
    )

    return AutomationObject(
        job_title=inputs['job_query'],
        location=inputs['location'],
        company_activity=inputs['company_activity'],
        task_description=inputs['task_description'],
        found_salary_data=[annual_salary],
        task_steps=task_steps,
        time_analysis=time_analysis,
        cost_projections=cost_projections,
        roi_analysis=roi_analysis
    )
