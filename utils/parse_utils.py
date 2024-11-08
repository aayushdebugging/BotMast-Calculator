from app.models.schemas import TaskBreakdown, ROIAnalysis
from typing import List

def parse_task_steps(response_text: str) -> List[TaskBreakdown]:
    steps = []
    for line in response_text.splitlines():
        if '|' in line:
            step_name, percentage = line.split('|')
            steps.append(TaskBreakdown(step=step_name.strip(), percentage=float(percentage.strip('% '))))
    return steps

def parse_roi_response(response_text: str) -> ROIAnalysis:
    lines = response_text.splitlines()
    percentage = float(lines[0].split(':')[1].strip('% '))
    basis = lines[1].split(':', 1)[1].strip()
    return ROIAnalysis(percentage=percentage, calculation_basis=basis)
