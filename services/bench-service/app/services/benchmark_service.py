"""
Benchmark Service Layer

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
import math

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.benchmark import Benchmark, BenchmarkStatus
from app.schemas.benchmark import BenchmarkCreate, BenchmarkUpdate


class BenchmarkService:
    """Service for benchmark operations"""

    @staticmethod
    def create_benchmark(db: Session, benchmark: BenchmarkCreate) -> Benchmark:
        """Create a new benchmark"""
        db_benchmark = Benchmark(
            name=benchmark.name,
            description=benchmark.description,
            model_path=benchmark.model_path,
            dataset_path=benchmark.dataset_path,
            config=benchmark.config or {},
            status=BenchmarkStatus.PENDING,
        )
        db.add(db_benchmark)
        db.commit()
        db.refresh(db_benchmark)
        return db_benchmark

    @staticmethod
    def get_benchmark(db: Session, benchmark_id: UUID) -> Optional[Benchmark]:
        """Get a benchmark by ID"""
        return db.query(Benchmark).filter(Benchmark.id == benchmark_id).first()

    @staticmethod
    def list_benchmarks(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        status: Optional[BenchmarkStatus] = None
    ) -> tuple[List[Benchmark], int]:
        """List benchmarks with pagination"""
        query = db.query(Benchmark)

        # Filter by status if provided
        if status:
            query = query.filter(Benchmark.status == status)

        # Get total count
        total = query.count()

        # Apply pagination and order
        benchmarks = (
            query.order_by(Benchmark.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

        return benchmarks, total

    @staticmethod
    def update_benchmark(
        db: Session,
        benchmark_id: UUID,
        benchmark_update: BenchmarkUpdate
    ) -> Optional[Benchmark]:
        """Update a benchmark"""
        db_benchmark = BenchmarkService.get_benchmark(db, benchmark_id)
        if not db_benchmark:
            return None

        update_data = benchmark_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_benchmark, field, value)

        db.commit()
        db.refresh(db_benchmark)
        return db_benchmark

    @staticmethod
    def delete_benchmark(db: Session, benchmark_id: UUID) -> bool:
        """Delete a benchmark"""
        db_benchmark = BenchmarkService.get_benchmark(db, benchmark_id)
        if not db_benchmark:
            return False

        db.delete(db_benchmark)
        db.commit()
        return True

    @staticmethod
    def start_benchmark_execution(db: Session, benchmark_id: UUID) -> Optional[Benchmark]:
        """Mark benchmark as running"""
        db_benchmark = BenchmarkService.get_benchmark(db, benchmark_id)
        if not db_benchmark:
            return None

        db_benchmark.status = BenchmarkStatus.RUNNING
        db_benchmark.started_at = datetime.utcnow()
        db.commit()
        db.refresh(db_benchmark)
        return db_benchmark

    @staticmethod
    def complete_benchmark_execution(
        db: Session,
        benchmark_id: UUID,
        results: dict,
        metrics: Optional[dict] = None
    ) -> Optional[Benchmark]:
        """Mark benchmark as completed with results"""
        db_benchmark = BenchmarkService.get_benchmark(db, benchmark_id)
        if not db_benchmark:
            return None

        db_benchmark.status = BenchmarkStatus.COMPLETED
        db_benchmark.completed_at = datetime.utcnow()
        db_benchmark.results = results

        # Update metrics if provided
        if metrics:
            db_benchmark.accuracy = metrics.get("accuracy")
            db_benchmark.f1_score = metrics.get("f1_score")
            db_benchmark.precision = metrics.get("precision")
            db_benchmark.recall = metrics.get("recall")
            db_benchmark.duration = metrics.get("duration")
            db_benchmark.throughput = metrics.get("throughput")

        db.commit()
        db.refresh(db_benchmark)
        return db_benchmark

    @staticmethod
    def fail_benchmark_execution(
        db: Session,
        benchmark_id: UUID,
        error_message: str
    ) -> Optional[Benchmark]:
        """Mark benchmark as failed"""
        db_benchmark = BenchmarkService.get_benchmark(db, benchmark_id)
        if not db_benchmark:
            return None

        db_benchmark.status = BenchmarkStatus.FAILED
        db_benchmark.completed_at = datetime.utcnow()
        db_benchmark.error_message = error_message

        db.commit()
        db.refresh(db_benchmark)
        return db_benchmark

    @staticmethod
    def get_benchmark_statistics(db: Session) -> dict:
        """Get overall benchmark statistics"""
        total = db.query(func.count(Benchmark.id)).scalar()

        pending = db.query(func.count(Benchmark.id)).filter(
            Benchmark.status == BenchmarkStatus.PENDING
        ).scalar()

        running = db.query(func.count(Benchmark.id)).filter(
            Benchmark.status == BenchmarkStatus.RUNNING
        ).scalar()

        completed = db.query(func.count(Benchmark.id)).filter(
            Benchmark.status == BenchmarkStatus.COMPLETED
        ).scalar()

        failed = db.query(func.count(Benchmark.id)).filter(
            Benchmark.status == BenchmarkStatus.FAILED
        ).scalar()

        return {
            "total": total or 0,
            "pending": pending or 0,
            "running": running or 0,
            "completed": completed or 0,
            "failed": failed or 0,
        }
