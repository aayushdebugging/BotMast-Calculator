from fastapi import APIRouter
from app.services.data_fetch import fetch_salary_data
from typing import Dict

router = APIRouter()

@router.get("/fetch", response_model=Dict)
def fetch_salary(query: str, location: str):
    return fetch_salary_data(query, location)
