"""
Analysis Service Layer

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Project ID: AEVA-2026-LQC-dc68e33
"""

import json
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.analysis import Analysis, AnalysisType, AnalysisStatus
from app.schemas.analysis import AnalysisCreate
from app.core.llm_client import llm_client
from app.core.config import settings


class AnalysisService:
    """Service for AI-powered analysis operations"""

    @staticmethod
    def create_analysis(db: Session, analysis_create: AnalysisCreate) -> Analysis:
        """Create a new analysis"""
        analysis = Analysis(
            analysis_type=analysis_create.analysis_type,
            input_data=analysis_create.input_data,
            config=analysis_create.config,
            llm_provider=settings.LLM_PROVIDER,
            llm_model=settings.LLM_MODEL,
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis

    @staticmethod
    def get_analysis(db: Session, analysis_id: UUID) -> Optional[Analysis]:
        """Get an analysis by ID"""
        return db.query(Analysis).filter(Analysis.id == analysis_id).first()

    @staticmethod
    def list_analyses(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        analysis_type: Optional[AnalysisType] = None,
        status: Optional[AnalysisStatus] = None
    ) -> List[Analysis]:
        """List all analyses with optional filtering"""
        query = db.query(Analysis)

        if analysis_type:
            query = query.filter(Analysis.analysis_type == analysis_type)

        if status:
            query = query.filter(Analysis.status == status)

        return query.order_by(Analysis.created_at.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def count_analyses(
        db: Session,
        analysis_type: Optional[AnalysisType] = None,
        status: Optional[AnalysisStatus] = None
    ) -> int:
        """Count total analyses"""
        query = db.query(Analysis)

        if analysis_type:
            query = query.filter(Analysis.analysis_type == analysis_type)

        if status:
            query = query.filter(Analysis.status == status)

        return query.count()

    @staticmethod
    def delete_analysis(db: Session, analysis_id: UUID) -> bool:
        """Delete an analysis"""
        analysis = AnalysisService.get_analysis(db, analysis_id)
        if not analysis:
            return False

        db.delete(analysis)
        db.commit()

        return True

    @staticmethod
    async def perform_analysis(db: Session, analysis_id: UUID) -> Optional[Analysis]:
        """
        Perform AI analysis on the given data.

        Args:
            db: Database session
            analysis_id: Analysis UUID

        Returns:
            Updated analysis with results
        """
        analysis = AnalysisService.get_analysis(db, analysis_id)
        if not analysis:
            return None

        # Update status to processing
        analysis.status = AnalysisStatus.PROCESSING
        analysis.updated_at = datetime.utcnow()
        db.commit()

        start_time = time.time()

        try:
            # Build prompt based on analysis type
            prompt = AnalysisService._build_prompt(
                analysis.analysis_type,
                analysis.input_data,
                analysis.config
            )

            # Store prompt for debugging
            analysis.prompt = prompt

            # Generate analysis using LLM
            system_message = AnalysisService._get_system_message(analysis.analysis_type)
            analysis_text = await llm_client.generate_analysis(
                prompt=prompt,
                context=analysis.input_data,
                system_message=system_message
            )

            # Parse analysis results
            parsed_results = AnalysisService._parse_analysis_results(analysis_text)

            # Update analysis with results
            analysis.analysis_text = analysis_text
            analysis.findings = parsed_results.get("findings", [])
            analysis.recommendations = parsed_results.get("recommendations", [])
            analysis.confidence_score = parsed_results.get("confidence", 0.0)
            analysis.status = AnalysisStatus.COMPLETED

        except Exception as e:
            # Handle errors
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = str(e)

        # Calculate processing time
        analysis.processing_time = time.time() - start_time
        analysis.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(analysis)

        return analysis

    @staticmethod
    async def quick_analysis(
        analysis_type: AnalysisType,
        data: Dict[str, Any],
        config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Perform quick analysis without database persistence.

        Args:
            analysis_type: Type of analysis
            data: Input data
            config: Analysis configuration

        Returns:
            Analysis results
        """
        start_time = time.time()

        # Build prompt
        prompt = AnalysisService._build_prompt(analysis_type, data, config or {})

        # Generate analysis
        system_message = AnalysisService._get_system_message(analysis_type)
        analysis_text = await llm_client.generate_analysis(
            prompt=prompt,
            context=data,
            system_message=system_message
        )

        # Parse results
        parsed_results = AnalysisService._parse_analysis_results(analysis_text)

        processing_time = time.time() - start_time

        return {
            "analysis_type": analysis_type,
            "summary": parsed_results.get("summary", ""),
            "findings": parsed_results.get("findings", []),
            "recommendations": parsed_results.get("recommendations", []),
            "confidence_score": parsed_results.get("confidence", 0.0),
            "processing_time": processing_time
        }

    @staticmethod
    def _build_prompt(
        analysis_type: AnalysisType,
        input_data: Dict[str, Any],
        config: Dict[str, Any]
    ) -> str:
        """Build analysis prompt based on type and data"""
        prompts = {
            AnalysisType.BASIC: (
                "Analyze the following evaluation data and provide a brief summary of the results. "
                "Focus on key metrics and overall performance."
            ),
            AnalysisType.COMPREHENSIVE: (
                "Perform a comprehensive analysis of the evaluation data. "
                "Include detailed findings, identify patterns, assess quality, "
                "and provide actionable recommendations for improvement."
            ),
            AnalysisType.COMPARATIVE: (
                "Compare the evaluation results across different models or experiments. "
                "Identify strengths and weaknesses, highlight significant differences, "
                "and recommend the best performing option."
            ),
            AnalysisType.PREDICTIVE: (
                "Analyze the evaluation data and predict potential future performance. "
                "Identify trends, forecast outcomes, and provide confidence intervals."
            ),
            AnalysisType.DIAGNOSTIC: (
                "Diagnose issues and anomalies in the evaluation data. "
                "Identify root causes of poor performance, detect outliers, "
                "and suggest corrective actions."
            ),
        }

        base_prompt = prompts.get(analysis_type, prompts[AnalysisType.BASIC])

        # Add config-specific instructions
        if config.get("focus_areas"):
            focus = ", ".join(config["focus_areas"])
            base_prompt += f"\n\nFocus particularly on: {focus}."

        if config.get("include_recommendations", True):
            base_prompt += "\n\nProvide specific, actionable recommendations."

        base_prompt += "\n\nReturn your analysis in JSON format with the following structure:"
        base_prompt += '\n{"summary": "...", "findings": [...], "recommendations": [...], "confidence": 0.0-1.0}'

        return base_prompt

    @staticmethod
    def _get_system_message(analysis_type: AnalysisType) -> str:
        """Get system message for LLM based on analysis type"""
        return (
            "You are an expert AI system for analyzing machine learning model evaluations. "
            "You provide insightful, data-driven analysis with specific recommendations. "
            "Your responses are clear, concise, and actionable. "
            "Always return results in valid JSON format."
        )

    @staticmethod
    def _parse_analysis_results(analysis_text: str) -> Dict[str, Any]:
        """Parse LLM analysis results"""
        try:
            # Try to parse as JSON
            if "{" in analysis_text and "}" in analysis_text:
                # Extract JSON from text
                start_idx = analysis_text.find("{")
                end_idx = analysis_text.rfind("}") + 1
                json_text = analysis_text[start_idx:end_idx]
                return json.loads(json_text)
        except Exception:
            pass

        # Fallback: return text as summary
        return {
            "summary": analysis_text,
            "findings": ["Analysis completed - see summary for details"],
            "recommendations": [],
            "confidence": 0.7
        }
