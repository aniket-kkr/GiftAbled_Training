# A13 - Student API (FastAPI)

A beginner-friendly FastAPI application featuring GET endpoints for student queries, filtering, reporting, and class performance analytics.

## Features
- **Root Overview Route (`/`)**: API welcome message and listing of available endpoints.
- **Student List (`/students`)**: Supports filtering by:
  - `search` (name or email)
  - `course` (e.g. Python Fullstack, Data Science)
  - `min_marks` and `max_marks`
  - `passed` (True / False)
  - `sort_by` (`name`, `marks`, `id`, `attendance_pct`) and `order` (`asc`, `desc`)
  - `limit` and `offset` pagination
- **Single Student Details (`/students/{student_id}`)**: Retrieve individual records with 404 validation.
- **Grade & Report Card (`/students/{student_id}/report`)**: Evaluates percentage, letter grades (A+, A, B, C, D, F), and pass/fail standing.
- **Analytics & Summary (`/stats`)**: Total students, class average, pass percentage, top scorer, and lowest scorer.
- **Interactive OpenAPI Documentation (`/docs`)**: Interactive Swagger UI.

## Run
Install requirements and launch the server:

```bash
pip install -r requirements.txt
python main.py
```

Then visit:
- API Home: `http://127.0.0.1:8000`
- Interactive Swagger Docs: `http://127.0.0.1:8000/docs`
- Class Statistics: `http://127.0.0.1:8000/stats`
- Student List: `http://127.0.0.1:8000/students`

## Run Tests
```bash
pytest test_api.py -v
```
