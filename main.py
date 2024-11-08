from fastapi import FastAPI
from app.routes import tasks, salary

app = FastAPI(title="Automation ROI API")

# Register routers
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(salary.router, prefix="/salary", tags=["Salary"])

@app.get("/")
def root():
    return {"message": "Welcome to the Automation ROI API"}
