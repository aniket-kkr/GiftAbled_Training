from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI(
    title="Student API",
    description="Assignment 13: Introductory FastAPI application focusing on GET routes",
    version="1.0.0",
)


class Student(BaseModel):
    id: int
    name: str
    email: str
    course: str
    marks: float = Field(ge=0, le=100)
    attendance_pct: float = Field(ge=0, le=100)


# In-memory student dataset
STUDENTS_DB: List[Student] = [
    Student(id=1, name="Aniket Kumar", email="aniket@example.com", course="Python Fullstack", marks=92.5, attendance_pct=96.0),
    Student(id=2, name="Priya Sharma", email="priya@example.com", course="Data Science", marks=88.0, attendance_pct=92.5),
    Student(id=3, name="Rahul Verma", email="rahul@example.com", course="Python Fullstack", marks=64.0, attendance_pct=81.0),
    Student(id=4, name="Sneha Patel", email="sneha@example.com", course="Web Development", marks=95.0, attendance_pct=98.0),
    Student(id=5, name="Vikram Singh", email="vikram@example.com", course="Data Science", marks=42.0, attendance_pct=72.0),
    Student(id=6, name="Aarav Gupta", email="aarav@example.com", course="Python Fullstack", marks=77.5, attendance_pct=89.0),
    Student(id=7, name="Neha Das", email="neha@example.com", course="Web Development", marks=85.0, attendance_pct=91.0),
    Student(id=8, name="Rohan Iyer", email="rohan@example.com", course="Cloud Computing", marks=38.0, attendance_pct=65.0),
]


def calculate_grade(marks: float) -> str:
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    return "F"


@app.get("/")
def read_root():
    """Welcome route providing API documentation metadata and available endpoints."""
    return {
        "message": "Welcome to Student API (Assignment 13 - GET routes)",
        "author": "Aniket Kumar",
        "documentation": "/docs",
        "endpoints": {
            "all_students": "/students",
            "single_student": "/students/{student_id}",
            "student_report": "/students/{student_id}/report",
            "class_statistics": "/stats",
            "courses_list": "/courses",
        },
    }


@app.get("/students", response_model=List[Student])
def get_students(
    search: Optional[str] = Query(None, description="Search by name or email substring"),
    course: Optional[str] = Query(None, description="Filter by enrolled course"),
    min_marks: Optional[float] = Query(None, ge=0, le=100, description="Minimum marks threshold"),
    max_marks: Optional[float] = Query(None, ge=0, le=100, description="Maximum marks threshold"),
    passed: Optional[bool] = Query(None, description="Filter by pass status (marks >= 50)"),
    sort_by: Optional[str] = Query("id", regex="^(id|name|marks|attendance_pct)$"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    limit: Optional[int] = Query(10, ge=1, le=100),
    offset: Optional[int] = Query(0, ge=0),
):
    """
    Retrieve students with optional search, course filtering, marks range, pass/fail status, and sorting.
    """
    results = STUDENTS_DB

    if search:
        s = search.lower()
        results = [st for st in results if s in st.name.lower() or s in st.email.lower()]

    if course:
        c = course.lower()
        results = [st for st in results if c in st.course.lower()]

    if min_marks is not None:
        results = [st for st in results if st.marks >= min_marks]

    if max_marks is not None:
        results = [st for st in results if st.marks <= max_marks]

    if passed is not None:
        if passed:
            results = [st for st in results if st.marks >= 50.0]
        else:
            results = [st for st in results if st.marks < 50.0]

    reverse_sort = order == "desc"
    results = sorted(results, key=lambda x: getattr(x, sort_by or "id"), reverse=reverse_sort)

    return results[offset : offset + limit]


@app.get("/students/{student_id}", response_model=Student)
def get_student_by_id(student_id: int):
    """Retrieve details of a single student by their unique ID."""
    for st in STUDENTS_DB:
        if st.id == student_id:
            return st
    raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")


@app.get("/students/{student_id}/report")
def get_student_report(student_id: int):
    """Generate a student grade and evaluation report card."""
    for st in STUDENTS_DB:
        if st.id == student_id:
            grade = calculate_grade(st.marks)
            is_passed = st.marks >= 50.0
            status_text = "Passed" if is_passed else "Failed - Needs Improvement"
            return {
                "student_id": st.id,
                "name": st.name,
                "course": st.course,
                "marks_scored": st.marks,
                "total_marks": 100,
                "percentage": f"{st.marks:.1f}%",
                "grade": grade,
                "attendance": f"{st.attendance_pct:.1f}%",
                "status": status_text,
            }
    raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found")


@app.get("/courses")
def get_courses():
    """List unique courses and count of students enrolled."""
    courses_count = {}
    for st in STUDENTS_DB:
        courses_count[st.course] = courses_count.get(st.course, 0) + 1
    return [
        {"course": course, "enrolled_students": count}
        for course, count in courses_count.items()
    ]


@app.get("/stats")
def get_class_statistics():
    """Compute overall class performance statistics."""
    if not STUDENTS_DB:
        return {"total_students": 0}

    total = len(STUDENTS_DB)
    marks_list = [st.marks for st in STUDENTS_DB]
    avg_marks = sum(marks_list) / total
    passed_count = sum(1 for m in marks_list if m >= 50.0)
    highest_student = max(STUDENTS_DB, key=lambda s: s.marks)
    lowest_student = min(STUDENTS_DB, key=lambda s: s.marks)

    return {
        "total_students": total,
        "average_marks": round(avg_marks, 2),
        "pass_percentage": f"{(passed_count / total) * 100:.1f}%",
        "passed_students": passed_count,
        "failed_students": total - passed_count,
        "highest_scorer": {
            "name": highest_student.name,
            "marks": highest_student.marks,
            "course": highest_student.course,
        },
        "lowest_scorer": {
            "name": lowest_student.name,
            "marks": lowest_student.marks,
            "course": lowest_student.course,
        },
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
