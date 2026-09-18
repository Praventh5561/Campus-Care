import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.db import init_db
from backend.routes.student import router as student_router
from backend.routes.staff import router as staff_router
from backend.routes.complaint import router as complaint_router

# Initialize database on startup
init_db()

app = FastAPI(
    title="CampusCare22 API",
    description="Backend Python API for CampusCare22 - College Complaint System",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(student_router)
app.include_router(staff_router)
app.include_router(complaint_router)

# Serve Frontend static files
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/api/health")
def health_check():
    return {"status": "online", "app": "CampusCare22 API (Python/FastAPI)"}

@app.get("/")
def read_root():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "CampusCare22 API is running. Access frontend files directly or via /static/index.html"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.server:app", host="127.0.0.1", port=8000, reload=True)
