# A14 - Student Web Page with CRUD

A full CRUD web application for managing student records featuring a modern HTML/CSS/JavaScript frontend powered by a FastAPI REST backend.

## Features
- **Create**: Add new students with validation (name, email, course, marks 0-100).
- **Read**: Display students in a clean table with pass/fail badges, marks progress bars, search, and summary analytics.
- **Update**: Edit existing student details via a pre-filled modal dialog.
- **Delete**: Remove students with confirmation.
- **Live Search**: Client-side / API query filtering by student name, email, or course.
- **FastAPI Backend**: Complete RESTful API endpoints at `/api/students`.

## Run
Install requirements and launch the server:

```bash
pip install -r requirements.txt
python main.py
```

Open your browser at:
`http://127.0.0.1:8000`
