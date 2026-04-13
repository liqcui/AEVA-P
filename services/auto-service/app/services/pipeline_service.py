"""
Pipeline Service Layer

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.pipeline import Pipeline, PipelineStatus, PipelineStep, StepStatus
from app.schemas.pipeline import PipelineCreate, PipelineUpdate


class PipelineService:
    """Service for pipeline operations"""

    @staticmethod
    def create_pipeline(db: Session, pipeline_create: PipelineCreate) -> Pipeline:
        """Create a new pipeline"""
        pipeline = Pipeline(
            name=pipeline_create.name,
            description=pipeline_create.description,
            config=pipeline_create.config,
        )

        db.add(pipeline)
        db.commit()
        db.refresh(pipeline)

        # Create pipeline steps from config
        if "steps" in pipeline_create.config:
            for idx, step_config in enumerate(pipeline_create.config["steps"]):
                step = PipelineStep(
                    pipeline_id=pipeline.id,
                    name=step_config.get("name", f"step_{idx}"),
                    step_type=step_config.get("type", "unknown"),
                    order=idx,
                    config=step_config.get("config", {}),
                )
                db.add(step)

            db.commit()
            db.refresh(pipeline)

        return pipeline

    @staticmethod
    def get_pipeline(db: Session, pipeline_id: UUID) -> Optional[Pipeline]:
        """Get a pipeline by ID"""
        return db.query(Pipeline).filter(Pipeline.id == pipeline_id).first()

    @staticmethod
    def list_pipelines(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[PipelineStatus] = None
    ) -> List[Pipeline]:
        """List all pipelines with optional filtering"""
        query = db.query(Pipeline)

        if status:
            query = query.filter(Pipeline.status == status)

        return query.order_by(Pipeline.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def count_pipelines(db: Session, status: Optional[PipelineStatus] = None) -> int:
        """Count total pipelines"""
        query = db.query(Pipeline)

        if status:
            query = query.filter(Pipeline.status == status)

        return query.count()

    @staticmethod
    def update_pipeline(
        db: Session,
        pipeline_id: UUID,
        pipeline_update: PipelineUpdate
    ) -> Optional[Pipeline]:
        """Update a pipeline"""
        pipeline = PipelineService.get_pipeline(db, pipeline_id)
        if not pipeline:
            return None

        # Update fields
        update_data = pipeline_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(pipeline, field, value)

        pipeline.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(pipeline)

        return pipeline

    @staticmethod
    def delete_pipeline(db: Session, pipeline_id: UUID) -> bool:
        """Delete a pipeline"""
        pipeline = PipelineService.get_pipeline(db, pipeline_id)
        if not pipeline:
            return False

        db.delete(pipeline)
        db.commit()

        return True

    @staticmethod
    def update_pipeline_status(
        db: Session,
        pipeline_id: UUID,
        status: PipelineStatus,
        error_message: Optional[str] = None,
        results: Optional[dict] = None
    ) -> Optional[Pipeline]:
        """Update pipeline status and related fields"""
        pipeline = PipelineService.get_pipeline(db, pipeline_id)
        if not pipeline:
            return None

        pipeline.status = status
        pipeline.updated_at = datetime.utcnow()

        if status == PipelineStatus.RUNNING and not pipeline.started_at:
            pipeline.started_at = datetime.utcnow()

        if status in [PipelineStatus.COMPLETED, PipelineStatus.FAILED, PipelineStatus.CANCELLED]:
            pipeline.completed_at = datetime.utcnow()
            if pipeline.started_at:
                pipeline.duration = (pipeline.completed_at - pipeline.started_at).total_seconds()

        if error_message:
            pipeline.error_message = error_message

        if results:
            pipeline.results = results

        db.commit()
        db.refresh(pipeline)

        return pipeline

    @staticmethod
    def get_pipeline_steps(db: Session, pipeline_id: UUID) -> List[PipelineStep]:
        """Get all steps for a pipeline"""
        return db.query(PipelineStep).filter(
            PipelineStep.pipeline_id == pipeline_id
        ).order_by(PipelineStep.order).all()

    @staticmethod
    def update_step_status(
        db: Session,
        step_id: UUID,
        status: StepStatus,
        error_message: Optional[str] = None,
        results: Optional[dict] = None,
        service_request_id: Optional[str] = None
    ) -> Optional[PipelineStep]:
        """Update pipeline step status"""
        step = db.query(PipelineStep).filter(PipelineStep.id == step_id).first()
        if not step:
            return None

        step.status = status
        step.updated_at = datetime.utcnow()

        if status == StepStatus.RUNNING and not step.started_at:
            step.started_at = datetime.utcnow()

        if status in [StepStatus.COMPLETED, StepStatus.FAILED, StepStatus.SKIPPED]:
            step.completed_at = datetime.utcnow()
            if step.started_at:
                step.duration = (step.completed_at - step.started_at).total_seconds()

        if error_message:
            step.error_message = error_message

        if results:
            step.results = results

        if service_request_id:
            step.service_request_id = service_request_id

        db.commit()
        db.refresh(step)

        return step
