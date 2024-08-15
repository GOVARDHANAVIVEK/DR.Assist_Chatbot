from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Configure CORS to allow requests from the backend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Backend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent

# Define the path for static files
STATIC_DIR = BASE_DIR / "static"

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("http://127.0.0.1:8001/", response_class=HTMLResponse)
async def read_root():
    index_file = STATIC_DIR / "index.html"
    with open(index_file, "r") as file:
        content = file.read()
    return HTMLResponse(content=content)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
