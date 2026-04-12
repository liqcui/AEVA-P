"""
Evaluation Scheduler for automated periodic evaluations

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Open Source with Attribution Required | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import logging
import time
import threading
from typing import Callable, Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class ScheduleType(Enum):
    """Schedule types"""
    INTERVAL = "interval"  # Run every N seconds
    CRON = "cron"  # Cron-style schedule
    ONCE = "once"  # Run once at specific time


@dataclass
class ScheduledTask:
    """Scheduled evaluation task"""
    task_id: str
    name: str
    function: Callable
    schedule_type: ScheduleType
    interval_seconds: Optional[int] = None
    cron_expression: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    run_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def should_run(self) -> bool:
        """Check if task should run now"""
        if not self.enabled:
            return False

        now = datetime.now()

        if self.schedule_type == ScheduleType.ONCE:
            if self.scheduled_time and now >= self.scheduled_time and self.run_count == 0:
                return True

        elif self.schedule_type == ScheduleType.INTERVAL:
            if self.last_run is None:
                return True
            if self.interval_seconds:
                elapsed = (now - self.last_run).total_seconds()
                if elapsed >= self.interval_seconds:
                    return True

        return False

    def update_next_run(self) -> None:
        """Update next run time"""
        if self.schedule_type == ScheduleType.INTERVAL and self.interval_seconds:
            self.next_run = datetime.now() + timedelta(seconds=self.interval_seconds)
        elif self.schedule_type == ScheduleType.ONCE:
            self.next_run = None  # One-time task

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'task_id': self.task_id,
            'name': self.name,
            'schedule_type': self.schedule_type.value,
            'interval_seconds': self.interval_seconds,
            'enabled': self.enabled,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'run_count': self.run_count,
            'metadata': self.metadata
        }


class EvaluationScheduler:
    """
    Scheduler for automated periodic evaluations

    Features:
    - Interval-based scheduling
    - One-time scheduled tasks
    - Task enable/disable
    - Execution history
    - Thread-safe operation
    """

    def __init__(self):
        """Initialize evaluation scheduler"""
        self.tasks: Dict[str, ScheduledTask] = {}
        self.running = False
        self.scheduler_thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

        logger.info("Evaluation scheduler initialized")

    def schedule_interval_task(
        self,
        task_id: str,
        name: str,
        function: Callable,
        interval_seconds: int,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ScheduledTask:
        """
        Schedule a task to run at fixed intervals

        Args:
            task_id: Unique task identifier
            name: Task name
            function: Function to execute
            interval_seconds: Interval between runs
            metadata: Optional metadata

        Returns:
            ScheduledTask
        """
        with self.lock:
            task = ScheduledTask(
                task_id=task_id,
                name=name,
                function=function,
                schedule_type=ScheduleType.INTERVAL,
                interval_seconds=interval_seconds,
                metadata=metadata or {}
            )

            task.update_next_run()
            self.tasks[task_id] = task

            logger.info(f"Scheduled interval task: {name} (every {interval_seconds}s)")

            return task

    def schedule_once(
        self,
        task_id: str,
        name: str,
        function: Callable,
        scheduled_time: datetime,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ScheduledTask:
        """
        Schedule a task to run once at a specific time

        Args:
            task_id: Unique task identifier
            name: Task name
            function: Function to execute
            scheduled_time: When to run
            metadata: Optional metadata

        Returns:
            ScheduledTask
        """
        with self.lock:
            task = ScheduledTask(
                task_id=task_id,
                name=name,
                function=function,
                schedule_type=ScheduleType.ONCE,
                scheduled_time=scheduled_time,
                metadata=metadata or {}
            )

            self.tasks[task_id] = task

            logger.info(f"Scheduled one-time task: {name} at {scheduled_time.isoformat()}")

            return task

    def enable_task(self, task_id: str) -> None:
        """Enable a task"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].enabled = True
                logger.info(f"Enabled task: {task_id}")

    def disable_task(self, task_id: str) -> None:
        """Disable a task"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].enabled = False
                logger.info(f"Disabled task: {task_id}")

    def remove_task(self, task_id: str) -> None:
        """Remove a task"""
        with self.lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
                logger.info(f"Removed task: {task_id}")

    def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """Get task by ID"""
        with self.lock:
            return self.tasks.get(task_id)

    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks"""
        with self.lock:
            return [task.to_dict() for task in self.tasks.values()]

    def start(self, check_interval: float = 1.0) -> None:
        """
        Start the scheduler

        Args:
            check_interval: How often to check for tasks (seconds)
        """
        if self.running:
            logger.warning("Scheduler already running")
            return

        self.running = True

        def scheduler_loop():
            logger.info(f"Scheduler started (check interval: {check_interval}s)")

            while self.running:
                try:
                    self._check_and_run_tasks()
                    time.sleep(check_interval)
                except Exception as e:
                    logger.error(f"Error in scheduler loop: {e}", exc_info=True)

            logger.info("Scheduler stopped")

        self.scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        self.scheduler_thread.start()

    def stop(self) -> None:
        """Stop the scheduler"""
        if not self.running:
            logger.warning("Scheduler not running")
            return

        logger.info("Stopping scheduler...")
        self.running = False

        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5.0)

    def _check_and_run_tasks(self) -> None:
        """Check for tasks that should run and execute them"""
        tasks_to_run = []

        with self.lock:
            for task in self.tasks.values():
                if task.should_run():
                    tasks_to_run.append(task)

        # Run tasks outside of lock
        for task in tasks_to_run:
            self._execute_task(task)

    def _execute_task(self, task: ScheduledTask) -> None:
        """Execute a scheduled task"""
        logger.info(f"Executing task: {task.name}")

        try:
            # Run the function
            start_time = time.time()
            result = task.function()
            duration = time.time() - start_time

            # Update task state
            with self.lock:
                task.last_run = datetime.now()
                task.run_count += 1
                task.update_next_run()

            logger.info(
                f"Task completed: {task.name} "
                f"(duration: {duration:.2f}s, run_count: {task.run_count})"
            )

            # Store result in metadata
            if result is not None:
                task.metadata['last_result'] = result

        except Exception as e:
            logger.error(f"Task execution failed: {task.name} - {e}", exc_info=True)

            with self.lock:
                task.metadata['last_error'] = str(e)
                task.metadata['last_error_time'] = datetime.now().isoformat()

    def get_stats(self) -> Dict[str, Any]:
        """Get scheduler statistics"""
        with self.lock:
            total_tasks = len(self.tasks)
            enabled_tasks = sum(1 for t in self.tasks.values() if t.enabled)
            total_runs = sum(t.run_count for t in self.tasks.values())

            return {
                'running': self.running,
                'total_tasks': total_tasks,
                'enabled_tasks': enabled_tasks,
                'disabled_tasks': total_tasks - enabled_tasks,
                'total_runs': total_runs
            }


# Helper functions

def every(seconds: int) -> int:
    """Helper to create interval in seconds"""
    return seconds


def minutes(n: int) -> int:
    """Helper to create interval in minutes"""
    return n * 60


def hours(n: int) -> int:
    """Helper to create interval in hours"""
    return n * 3600


def days(n: int) -> int:
    """Helper to create interval in days"""
    return n * 86400
