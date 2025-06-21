from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# In-memory databases
students = {}
classes = {}
registrations = {}

# Data models
class Student(BaseModel):
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    age: int
    city: str

class ClassInfo(BaseModel):
    class_name: str
    description: str
    start_date: date
    end_date: date
    number_of_hours: int

# Student endpoints
app = FastAPI()
@app.post("/students/{student_id}")
def add_student(student_id: str, student: Student):
    if student_id in students:
        raise HTTPException(status_code=400, detail="Student already exists")
    students[student_id] = student
    return {"message": "Student added"}

@app.put("/students/{student_id}")
def update_student(student_id: str, student: Student):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    students[student_id] = student
    return {"message": "Student updated"}

@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    del students[student_id]
    return {"message": "Student deleted"}

# Class endpoints
@app.post("/classes/{class_id}")
def add_class(class_id: str, class_info: ClassInfo):
    if class_id in classes:
        raise HTTPException(status_code=400, detail="Class already exists")
    classes[class_id] = class_info
    return {"message": "Class added"}

@app.put("/classes/{class_id}")
def update_class(class_id: str, class_info: ClassInfo):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    classes[class_id] = class_info
    return {"message": "Class updated"}

@app.delete("/classes/{class_id}")
def delete_class(class_id: str):
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    del classes[class_id]
    return {"message": "Class deleted"}

# Registration endpoints
@app.post("/register/{student_id}/{class_id}")
def register_student(student_id: str, class_id: str):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if class_id not in classes:
        raise HTTPException(status_code=404, detail="Class not found")
    if class_id not in registrations:
        registrations[class_id] = []
    if student_id in registrations[class_id]:
        raise HTTPException(status_code=400, detail="Student already registered")
    registrations[class_id].append(student_id)
    return {"message": "Student registered to class"}

@app.get("/classes/{class_id}/students")
def get_students(class_id: str):
    if class_id not in registrations:
        return {"students": []}
    return {
        "students": [students[sid] for sid in registrations[class_id]]
    }
