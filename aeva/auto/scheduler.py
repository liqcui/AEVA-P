"""
AEVA-Auto Task Scheduler
Schedules and manages evaluation tasks

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3


class TaskStatus(Enum):
    """Task status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScheduledTask:
    """Represents a scheduled evaluation task"""

    def __init__(
        self,
        task_id: str,
        pipeline_name: str,
        schedule: Optional[str] = None,  # cron-like schedule
        priority: TaskPriority = TaskPriority.NORMAL
    ):
        self.task_id = task_id
        self.pipeline_name = pipeline_name
        self.schedule = schedule
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Optional[Any] = None
        self.error: Optional[str] = None

    def start(self) -> None:
        """Mark task as started"""
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now()

    def complete(self, result: Any) -> None:
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result

    def fail(self, error: str) -> None:
        """Mark task as failed"""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now()
        self.error = error

    def cancel(self) -> None:
        """Cancel the task"""
        self.status = TaskStatus.CANCELLED
        self.completed_at = datetime.now()

    def get_duration(self) -> Optional[float]:
        """Get task duration in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class TaskScheduler:
    """
    Schedules and manages evaluation tasks

    Features:
    - Task prioritization
    - Cron-like scheduling
    - Resource management
    - Task dependencies
    """

    def __init__(self):
        self.tasks: Dict[str, ScheduledTask] = {}
        self.pending_queue: List[str] = []
        self.running_tasks: Dict[str, ScheduledTask] = {}

    def schedule_task(
        self,
        task_id: str,
        pipeline_name: str,
        schedule: Optional[str] = None,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> ScheduledTask:
        """
        Schedule a new task

        Args:
            task_id: Unique task identifier
            pipeline_name: Name of pipeline to execute
            schedule: Optional cron-like schedule
            priority: Task priority

        Returns:
            ScheduledTask object
        """
        task = ScheduledTask(
            task_id=task_id,
            pipeline_name=pipeline_name,
            schedule=schedule,
            priority=priority
        )

        self.tasks[task_id] = task
        self.pending_queue.append(task_id)

        # Sort queue by priority
        self._sort_queue()

        logger.info(f"Scheduled task {task_id} with priority {priority.name}")

        return task

    def _sort_queue(self) -> None:
        """Sort pending queue by priority"""
        self.pending_queue.sort(
            key=lambda tid: self.tasks[tid].priority.value,
            reverse=True
        )

    def get_next_task(self) -> Optional[ScheduledTask]:
        """Get next task to execute"""
        if not self.pending_queue:
            return None

        task_id = self.pending_queue.pop(0)
        task = self.tasks[task_id]

        task.start()
        self.running_tasks[task_id] = task

        logger.info(f"Starting task {task_id}")

        return task

    def complete_task(self, task_id: str, result: Any) -> None:
        """Mark a task as completed"""
        if task_id in self.running_tasks:
            task = self.running_tasks.pop(task_id)
            task.complete(result)
            logger.info(f"Completed task {task_id}")

    def fail_task(self, task_id: str, error: str) -> None:
        """Mark a task as failed"""
        if task_id in self.running_tasks:
            task = self.running_tasks.pop(task_id)
            task.fail(error)
            logger.error(f"Failed task {task_id}: {error}")

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        if task_id in self.pending_queue:
            self.pending_queue.remove(task_id)
            self.tasks[task_id].cancel()
            logger.info(f"Cancelled pending task {task_id}")
            return True

        if task_id in self.running_tasks:
            task = self.running_tasks.pop(task_id)
            task.cancel()
            logger.info(f"Cancelled running task {task_id}")
            return True

        return False

    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """Get a task by ID"""
        return self.tasks.get(task_id)

    def get_pending_tasks(self) -> List[ScheduledTask]:
        """Get all pending tasks"""
        return [self.tasks[tid] for tid in self.pending_queue]

    def get_running_tasks(self) -> List[ScheduledTask]:
        """Get all running tasks"""
        return list(self.running_tasks.values())

    def get_statistics(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        cancelled = sum(1 for t in self.tasks.values() if t.status == TaskStatus.CANCELLED)

        return {
            "total_tasks": len(self.tasks),
            "pending": len(self.pending_queue),
            "running": len(self.running_tasks),
            "completed": completed,
            "failed": failed,
            "cancelled": cancelled,
        }
