"""
AEVA API Server
FastAPI-based REST API

Copyright (c) 2024-2026 Liquan Cui. All rights reserved.
Author: Liquan Cui | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import uvicorn
import logging

from aeva import AEVA, AEVAConfig
from aeva.core.pipeline import Pipeline

logger = logging.getLogger(__name__)

# Global AEVA instance
aeva_instance: Optional[AEVA] = None


class EvaluationRequest(BaseModel):
    """Request model for evaluation"""
    pipeline_name: str
    algorithm_config: Dict[str, Any]
    context: Dict[str, Any] = {}


class PipelineCreate(BaseModel):
    """Request model for creating a pipeline"""
    name: str
    description: str = ""
    stages: List[Dict[str, Any]] = []


class StatusResponse(BaseModel):
    """Response model for status"""
    version: str
    status: str
    components: Dict[str, Any]


def create_app(config_path: Optional[str] = None) -> FastAPI:
    """
    Create FastAPI application

    Args:
        config_path: Path to AEVA configuration file

    Returns:
        FastAPI application instance
    """
    app = FastAPI(
        title="AEVA Platform API",
        description="Algorithm Evaluation & Validation Agent REST API",
        version="0.1.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize AEVA
    global aeva_instance

    @app.on_event("startup")
    async def startup_event():
        global aeva_instance
        logger.info("Starting AEVA API server...")

        if config_path:
            aeva_instance = AEVA(config_path=config_path)
        else:
            aeva_instance = AEVA()

        logger.info("AEVA instance initialized")

    @app.on_event("shutdown")
    async def shutdown_event():
        global aeva_instance
        if aeva_instance:
            logger.info("Shutting down AEVA...")
            aeva_instance.shutdown()

    # Routes
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "name": "AEVA Platform API",
            "version": "0.1.0",
            "status": "running"
        }

    @app.get("/status", response_model=StatusResponse)
    async def get_status():
        """Get platform status"""
        if not aeva_instance:
            raise HTTPException(status_code=500, detail="AEVA not initialized")

        status = aeva_instance.get_status()
        return StatusResponse(
            version=status["version"],
            status="running",
            components=status["components"]
        )

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy"}

    @app.post("/evaluate")
    async def evaluate(request: EvaluationRequest, background_tasks: BackgroundTasks):
        """
        Run an evaluation pipeline

        This is a simplified version - in production would handle
        actual algorithm loading and execution
        """
        if not aeva_instance:
            raise HTTPException(status_code=500, detail="AEVA not initialized")

        try:
            # Create a simple pipeline
            pipeline = aeva_instance.create_pipeline(name=request.pipeline_name)

            # Execute pipeline (simplified)
            # In production, this would be more sophisticated
            result = {
                "status": "queued",
                "pipeline": request.pipeline_name,
                "message": "Evaluation queued for processing"
            }

            return result

        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/benchmarks")
    async def list_benchmarks():
        """List available benchmark suites"""
        if not aeva_instance:
            raise HTTPException(status_code=500, detail="AEVA not initialized")

        suites = aeva_instance.bench.list_suites()
        return {"benchmarks": suites}

    @app.get("/gates")
    async def list_gates():
        """List configured quality gates"""
        if not aeva_instance:
            raise HTTPException(status_code=500, detail="AEVA not initialized")

        gates = [
            {"name": gate.name, "is_blocking": gate.is_blocking}
            for gate in aeva_instance.guard.gates
        ]
        return {"gates": gates}

    return app


def start_server(
    config_path: Optional[str] = None,
    host: str = "0.0.0.0",
    port: int = 8000,
    workers: int = 1
):
    """
    Start AEVA API server

    Args:
        config_path: Path to AEVA configuration file
        host: Host to bind to
        port: Port to bind to
        workers: Number of worker processes
    """
    app = create_app(config_path)

    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=workers,
        log_level="info"
    )


def main():
    """Main entry point for server"""
    import sys

    config_path = sys.argv[1] if len(sys.argv) > 1 else None
    start_server(config_path=config_path)


if __name__ == "__main__":
    main()
