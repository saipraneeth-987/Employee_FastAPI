Employee Management API (FastAPI + MongoDB)

This project is an implementation of the Python + MongoDB Assessment using FastAPI.
It provides CRUD APIs and aggregation endpoints for managing employee records.

📌 Tech Stack

FastAPI – for building the RESTful APIs

MongoDB (Local) – as the database

PyMongo – for database interactions

Pydantic – for request validation and schema enforcement

⚙️ Setup Instructions
1. Clone the repository
```
git clone https://github.com/saipraneeth-987/Employee_FastAPI.git
cd Employee_FastAPI
``` 

2. Install dependencies

Make sure you are using Python 3.9+.
```
pip install fastapi uvicorn pymongo python-dateutil
```

3. Start MongoDB

Ensure MongoDB is installed and running locally on port 27017.
By default, the database used is:

Database: assessment_db

Collection: employees

4. Run the FastAPI server
```
uvicorn main:app --reload
```

The API will be available at:
👉 http://127.0.0.1:8000

Swagger UI docs:
👉 http://127.0.0.1:8000/docs

📂 Project Structure
```
├── database.py   # MongoDB connection & collection setup
├── models.py     # Pydantic models for validation
├── main.py       # FastAPI routes & CRUD operations
```

🚀 API Endpoints
1. Create Employee

POST /employees
Request body:
```
{
  "employee_id": "E123",
  "name": "John Doe",
  "department": "Engineering",
  "salary": 75000,
  "joining_date": "2023-01-15",
  "skills": ["Python", "MongoDB", "APIs"]
}
```

2. Get Employee by ID

GET /employees/{employee_id}

3. Update Employee (Partial Updates Allowed)

PUT /employees/{employee_id}
Request body (any field optional):
```
{
  "salary": 85000,
  "department": "R&D"
}
```

4. Delete Employee

DELETE /employees/{employee_id}

5. List Employees by Department

GET /employees?department=Engineering
Returns employees sorted by joining_date (newest first).

6. Average Salary by Department

GET /employees/avg-salary
Response example:
```
[
  { "department": "Engineering", "avg_salary": 80000 },
  { "department": "HR", "avg_salary": 60000 }
]
```
7. Search Employees by Skill

GET /employees/search?skill=Python

⭐ Bonus Features

✅ Unique index on employee_id enforced in MongoDB

✅ Consistent joining_date formatting in all responses