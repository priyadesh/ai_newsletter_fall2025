# =============================================================================
#  Filename: api_models.py
#
#  Short Description: API response models for FastAPI endpoints
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Generic API response wrapper."""
    
    success: bool = Field(..., description="Request success status")
    data: Optional[T] = Field(None, description="Response data")
    message: str = Field(..., description="Response message")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Response timestamp")
    
    model_config = {"json_schema_extra": {"example": {
        "success": True,
        "data": {},
        "message": "Request completed successfully",
        "timestamp": "2025-01-27T10:00:00Z"
    }}}


class ErrorResponse(BaseModel):
    """Error response model."""
    
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Error timestamp")
    
    model_config = {"json_schema_extra": {"example": {
        "success": False,
        "error": "ValidationError",
        "message": "Invalid input data",
        "details": {"field": "title", "issue": "required"},
        "timestamp": "2025-01-27T10:00:00Z"
    }}}


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Check timestamp")
    services: dict = Field(default_factory=dict, description="External service status")
    
    model_config = {"json_schema_extra": {"example": {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2025-01-27T10:00:00Z",
        "services": {
            "openai": "connected",
            "serpapi": "connected",
            "cache": "active"
        }
    }}}
