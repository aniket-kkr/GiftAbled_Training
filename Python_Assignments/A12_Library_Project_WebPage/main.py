from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(
    title="Library Management System | Project Webpage",
    description="Web page explaining the Python & CSV Library Management System project",
    version="1.0.0",
)

webpage_file = Path(__file__).with_name("index.html")


@app.get("/", include_in_schema=False)
def get_project_webpage() -> FileResponse:
    return FileResponse(webpage_file, media_type="text/html")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
