from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="Aniket Kumar | Resume")
resume_page = Path(__file__).with_name("Index.html")


@app.get("/", include_in_schema=False)
def get_resume() -> FileResponse:
    return FileResponse(resume_page, media_type="text/html")
