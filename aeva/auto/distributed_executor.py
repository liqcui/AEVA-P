"""
AEVA Distributed Task Executor using Celery
Enables horizontal scaling of evaluation tasks

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, List, Optional
import logging
from celery import Celery, Task
from celery.result import AsyncResult
from kombu import Queue, Exchange

logger = logging.getLogger(__name__)

# Celery app configuration
app = Celery(
    'aeva',
    broker='pyamqp://guest@localhost:5672//',
    backend='redis://localhost:6379/0'
)

# Configure task queues
task_exchange = Exchange('aeva', type='topic')

app.conf.update(
    task_queues=(
        Queue('guard', exchange=task_exchange, routing_key='guard.#'),
        Queue('bench', exchange=task_exchange, routing_key='bench.#'),
        Queue('llm_eval', exchange=task_exchange, routing_key='llm.#'),
        Queue('brain', exchange=task_exchange, routing_key='brain.#'),
        Queue('default', exchange=task_exchange, routing_key='default.#'),
    ),
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3300,  # 55 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)


class AEVATask(Task):
    """Base task class with automatic retry and error handling"""

    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True
    retry_backoff_max = 600
    retry_jitter = True


@app.task(base=AEVATask, queue='guard', routing_key='guard.quality_gate')
def run_quality_gate_task(
    gate_config: Dict[str, Any],
    model_path: str,
    data_path: str
) -> Dict[str, Any]:
    """
    Distributed quality gate evaluation task

    Args:
        gate_config: Quality gate configuration
        model_path: Path to model file
        data_path: Path to test data

    Returns:
        Quality gate evaluation results
    """
    logger.info(f"Running quality gate task for model: {model_path}")

    try:
        from aeva.guard import QualityGate

        gate = QualityGate(**gate_config)
        results = gate.evaluate(model_path, data_path)

        logger.info(f"Quality gate completed: {results['passed']}")
        return results

    except Exception as e:
        logger.error(f"Quality gate task failed: {str(e)}")
        raise


@app.task(base=AEVATask, queue='bench', routing_key='bench.run')
def run_benchmark_task(
    benchmark_id: str,
    model_path: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Distributed benchmark evaluation task

    Args:
        benchmark_id: ID of benchmark to run
        model_path: Path to model file
        config: Optional benchmark configuration

    Returns:
        Benchmark evaluation results
    """
    logger.info(f"Running benchmark {benchmark_id} for model: {model_path}")

    try:
        from aeva.bench import BenchmarkRunner

        runner = BenchmarkRunner(config or {})
        results = runner.run(benchmark_id, model_path)

        logger.info(f"Benchmark completed with score: {results.get('score', 0)}")
        return results

    except Exception as e:
        logger.error(f"Benchmark task failed: {str(e)}")
        raise


@app.task(base=AEVATask, queue='llm_eval', routing_key='llm.correctness')
def run_llm_correctness_task(
    output: str,
    context: Optional[str] = None,
    reference: Optional[str] = None,
    instructions: Optional[str] = None,
    ground_truth: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Distributed LLM correctness evaluation task

    Args:
        output: LLM output to evaluate
        context: Input context
        reference: Reference text
        instructions: Task instructions
        ground_truth: Known facts
        config: Evaluator configuration

    Returns:
        Correctness evaluation results
    """
    logger.info("Running LLM correctness evaluation")

    try:
        from aeva.llm_evaluation import CorrectnessEvaluator

        evaluator = CorrectnessEvaluator(**(config or {}))
        results = evaluator.evaluate(
            output=output,
            context=context,
            reference=reference,
            instructions=instructions,
            ground_truth=ground_truth
        )

        logger.info(f"Correctness evaluation completed: {results['overall_correctness']:.2f}")
        return {
            'overall_correctness': results['overall_correctness'],
            'hallucination': {
                'is_hallucinated': results['hallucination'].is_hallucinated,
                'confidence_score': results['hallucination'].confidence_score,
                'hallucination_type': results['hallucination'].hallucination_type,
            },
            'factuality': {
                'is_factual': results.get('factuality', {}).is_factual if 'factuality' in results else None,
                'accuracy_score': results.get('factuality', {}).accuracy_score if 'factuality' in results else None,
            } if 'factuality' in results else None,
            'task_completion': {
                'completion_score': results.get('task_completion', {}).completion_score if 'task_completion' in results else None,
            } if 'task_completion' in results else None,
        }

    except Exception as e:
        logger.error(f"LLM correctness task failed: {str(e)}")
        raise


@app.task(base=AEVATask, queue='llm_eval', routing_key='llm.safety')
def run_llm_safety_task(
    text: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Distributed LLM safety evaluation task

    Args:
        text: Text to evaluate for safety
        config: Safety evaluator configuration

    Returns:
        Safety evaluation results
    """
    logger.info("Running LLM safety evaluation")

    try:
        from aeva.llm_evaluation import SafetyEvaluator

        evaluator = SafetyEvaluator(**(config or {}))
        results = evaluator.evaluate(text)

        logger.info(f"Safety evaluation completed: safe={results.is_safe}")
        return {
            'is_safe': results.is_safe,
            'overall_safety_score': results.overall_safety_score,
            'harmful_content': {
                'is_harmful': results.harmful_content.is_harmful,
                'severity_score': results.harmful_content.severity_score,
                'harm_categories': results.harmful_content.harm_categories,
            },
            'jailbreak': {
                'is_jailbreak_attempt': results.jailbreak.is_jailbreak_attempt,
                'confidence': results.jailbreak.confidence,
                'jailbreak_type': results.jailbreak.jailbreak_type,
            },
            'pii': {
                'has_pii': results.pii.has_pii,
                'pii_types': results.pii.pii_types,
                'redacted_text': results.pii.redacted_text,
            },
        }

    except Exception as e:
        logger.error(f"LLM safety task failed: {str(e)}")
        raise


@app.task(base=AEVATask, queue='brain', routing_key='brain.analyze')
def run_brain_analysis_task(
    results: Dict[str, Any],
    model_info: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Distributed AEVA-Brain intelligent analysis task

    Args:
        results: Evaluation results to analyze
        model_info: Model metadata
        config: Brain configuration

    Returns:
        Intelligent analysis and recommendations
    """
    logger.info("Running AEVA-Brain analysis")

    try:
        from aeva.brain import QualityLLM

        brain = QualityLLM(**(config or {}))
        analysis = brain.analyze(results, model_info)

        logger.info(f"Brain analysis completed")
        return analysis

    except Exception as e:
        logger.error(f"Brain analysis task failed: {str(e)}")
        raise


class DistributedPipelineExecutor:
    """
    Executes evaluation pipelines using distributed task queue

    Features:
    - Automatic task distribution
    - Parallel execution
    - Result aggregation
    - Fault tolerance
    """

    def __init__(self):
        self.app = app

    def execute_pipeline_async(
        self,
        pipeline_config: Dict[str, Any]
    ) -> List[AsyncResult]:
        """
        Execute pipeline asynchronously using task queue

        Args:
            pipeline_config: Pipeline configuration with stages

        Returns:
            List of AsyncResult objects for tracking
        """
        logger.info(f"Executing pipeline asynchronously: {pipeline_config.get('name', 'unnamed')}")

        tasks = []

        for stage in pipeline_config.get('stages', []):
            stage_type = stage.get('type')
            stage_params = stage.get('params', {})

            # Route to appropriate task
            if stage_type == 'guard':
                task = run_quality_gate_task.apply_async(
                    kwargs=stage_params,
                    routing_key='guard.quality_gate'
                )
            elif stage_type == 'bench':
                task = run_benchmark_task.apply_async(
                    kwargs=stage_params,
                    routing_key='bench.run'
                )
            elif stage_type == 'llm_correctness':
                task = run_llm_correctness_task.apply_async(
                    kwargs=stage_params,
                    routing_key='llm.correctness'
                )
            elif stage_type == 'llm_safety':
                task = run_llm_safety_task.apply_async(
                    kwargs=stage_params,
                    routing_key='llm.safety'
                )
            elif stage_type == 'brain':
                task = run_brain_analysis_task.apply_async(
                    kwargs=stage_params,
                    routing_key='brain.analyze'
                )
            else:
                logger.warning(f"Unknown stage type: {stage_type}")
                continue

            tasks.append(task)

        logger.info(f"Dispatched {len(tasks)} tasks to queue")
        return tasks

    def get_results(
        self,
        task_ids: List[str],
        timeout: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Get results from async tasks

        Args:
            task_ids: List of task IDs
            timeout: Optional timeout in seconds

        Returns:
            List of task results
        """
        results = []

        for task_id in task_ids:
            async_result = AsyncResult(task_id, app=self.app)

            try:
                result = async_result.get(timeout=timeout)
                results.append({
                    'task_id': task_id,
                    'status': 'completed',
                    'result': result
                })
            except Exception as e:
                logger.error(f"Task {task_id} failed: {str(e)}")
                results.append({
                    'task_id': task_id,
                    'status': 'failed',
                    'error': str(e)
                })

        return results

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a task"""
        async_result = AsyncResult(task_id, app=self.app)

        return {
            'task_id': task_id,
            'status': async_result.state,
            'ready': async_result.ready(),
            'successful': async_result.successful() if async_result.ready() else None,
            'result': async_result.result if async_result.ready() and async_result.successful() else None,
        }


# Export for use in worker
__all__ = [
    'app',
    'run_quality_gate_task',
    'run_benchmark_task',
    'run_llm_correctness_task',
    'run_llm_safety_task',
    'run_brain_analysis_task',
    'DistributedPipelineExecutor',
]
