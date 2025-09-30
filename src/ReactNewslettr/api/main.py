# =============================================================================
#  Filename: main.py
#
#  Short Description: FastAPI application main entry point
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
from ..config import settings
from .routes import router
from ..models.api_models import ErrorResponse
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI News Newsletter - Multi-agent system for collecting, summarizing, and presenting AI news",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include API routes with a prefix
app.include_router(router, prefix="/api/v1")

# Setup static files and templates
# Correctly reference the frontend build directory
frontend_build_path = Path(__file__).parent.parent.parent.parent / "frontend" / "build"

# Ensure the frontend build directory exists
if not frontend_build_path.exists():
    logger.warning(f"Frontend build directory not found: {frontend_build_path}. Serving static files might fail.")
    # Create a dummy directory or handle gracefully if React build is not present
    os.makedirs(frontend_build_path, exist_ok=True)
    # Optionally, create a dummy index.html to prevent 404 on root
    (frontend_build_path / "index.html").write_text("<h1>Frontend Not Built</h1><p>Please run `npm run build` in the frontend directory.</p>")

app.mount("/static", StaticFiles(directory=frontend_build_path / "static"), name="static")
app.mount("/assets", StaticFiles(directory=frontend_build_path / "assets"), name="assets") # For Vite/React static assets

# Templates for server-side rendering (e.g., index.html)
templates = Jinja2Templates(directory=frontend_build_path) # Point to frontend build for index.html


@app.get("/", response_class=HTMLResponse, summary="Landing Page")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "app_name": settings.app_name})


@app.get("/article/{article_id}", response_class=HTMLResponse, summary="Individual Article Page")
async def read_article(request: Request, article_id: str):
    return templates.TemplateResponse("article.html", {"request": request, "article_id": article_id})


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    # Ensure 'detail' is a dictionary for consistent error response
    detail_content = exc.detail if isinstance(exc.detail, dict) else {"message": str(exc.detail)}
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=detail_content.get("error", f"HTTPError_{exc.status_code}"), # Use existing error or default
            message=detail_content.get("message", str(exc.detail)),
            details=detail_content.get("details", {"detail": str(exc.detail)})
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="InternalServerError",
            message="An unexpected error occurred",
            details={"exception": str(exc)}
        ).model_dump()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.ReactNewslettr.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
