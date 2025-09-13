# main.py
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime, date
from database import employees_collection
from models import Employee, UpdateEmployee

app = FastAPI(title="Employee Assessment API - FastAPI + MongoDB")


# 🔹 Helper function for consistent date formatting
def serialize_employee(emp):
    if "joining_date" in emp:
        if isinstance(emp["joining_date"], (datetime, date)):
            emp["joining_date"] = emp["joining_date"].isoformat()
        elif isinstance(emp["joining_date"], str):
            try:
                # Normalize any valid string date into ISO format
                parsed_date = datetime.fromisoformat(emp["joining_date"])
                emp["joining_date"] = parsed_date.date().isoformat()
            except Exception:
                pass  # leave as-is if it's not ISO-compatible
    return emp


# 1. Create Employee
@app.post("/employees")
def create_employee(employee: Employee):
    emp_dict = employee.dict()

    # Convert date to string before saving
    if isinstance(emp_dict.get("joining_date"), (date, datetime)):
        emp_dict["joining_date"] = emp_dict["joining_date"].isoformat()

    employees_collection.insert_one(emp_dict)
    return {"message": "Employee added successfully"}


# 5. List Employees by Department
@app.get("/employees")
def list_employees_by_department(department: str = None):
    query = {}
    if department:
        query["department"] = department
    employees = list(
        employees_collection.find(query, {"_id": 0}).sort("joining_date", -1)
    )
    return [serialize_employee(e) for e in employees]


# 6. Average Salary by Department
@app.get("/employees/avg-salary")
def average_salary():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}}
    ]
    results = list(employees_collection.aggregate(pipeline))
    return [{"department": r["_id"], "avg_salary": r["avg_salary"]} for r in results]


# 7. Search Employees by Skill
@app.get("/employees/search")
def search_employees(skill: str):
    employees = list(employees_collection.find({"skills": skill}, {"_id": 0}))
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found with that skill")
    return [serialize_employee(e) for e in employees]


# 2. Get Employee by ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    employee = employees_collection.find_one({"employee_id": employee_id}, {"_id": 0})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return serialize_employee(employee)


# 3. Update Employee
@app.put("/employees/{employee_id}")
def update_employee(employee_id: str, employee: UpdateEmployee):
    update_data = {k: v for k, v in employee.dict().items() if v is not None}

    # Convert datetime.date to ISO string before saving
    if "joining_date" in update_data and isinstance(update_data["joining_date"], (date, datetime)):
        update_data["joining_date"] = update_data["joining_date"].isoformat()

    result = employees_collection.update_one(
        {"employee_id": employee_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {"message": "Employee updated successfully"}


# 4. Delete Employee
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    result = employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}
