"""
Resource Monitor for CPU, GPU, and Memory usage

Copyright (c) 2024-2026 AEVA Development Team. All rights reserved.
Dual License: Free for Personal/Academic, Commercial Requires Permission | GitHub: https://github.com/liqcui/AEVA-P
Project ID: AEVA-2026-LQC-dc68e33
"""

import time
import logging
from typing import Dict, Any, Optional
import threading

logger = logging.getLogger(__name__)


class ResourceMonitor:
    """
    Monitor system resource usage during model inference

    Features:
    - CPU usage tracking
    - Memory usage tracking
    - GPU usage tracking (if available)
    - Real-time monitoring
    """

    def __init__(self, sampling_interval: float = 0.1):
        """
        Initialize resource monitor

        Args:
            sampling_interval: Sampling interval in seconds
        """
        self.sampling_interval = sampling_interval
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None

        # Measurements
        self.cpu_measurements = []
        self.memory_measurements = []
        self.gpu_measurements = []

        # Check available monitoring tools
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check if monitoring dependencies are available"""
        self.has_psutil = False
        self.has_pynvml = False

        try:
            import psutil
            self.has_psutil = True
            self.psutil = psutil
        except ImportError:
            logger.warning("psutil not installed. CPU/Memory monitoring limited.")

        try:
            import pynvml
            pynvml.nvmlInit()
            self.has_pynvml = True
            self.pynvml = pynvml
        except (ImportError, Exception):
            logger.info("pynvml not available. GPU monitoring disabled.")

    def start(self) -> None:
        """Start monitoring"""
        if self.monitoring:
            logger.warning("Monitor already running")
            return

        self.monitoring = True
        self.cpu_measurements = []
        self.memory_measurements = []
        self.gpu_measurements = []

        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()

        logger.info("Resource monitoring started")

    def stop(self) -> None:
        """Stop monitoring"""
        if not self.monitoring:
            return

        self.monitoring = False

        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)

        logger.info("Resource monitoring stopped")

    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self.monitoring:
            snapshot = self._take_snapshot()

            if snapshot:
                self.cpu_measurements.append(snapshot.get('cpu_percent', 0))
                self.memory_measurements.append(snapshot.get('memory_mb', 0))

                if snapshot.get('gpu_stats'):
                    self.gpu_measurements.append(snapshot['gpu_stats'])

            time.sleep(self.sampling_interval)

    def _take_snapshot(self) -> Optional[Dict[str, Any]]:
        """Take a resource usage snapshot"""
        snapshot = {}

        # CPU and Memory
        if self.has_psutil:
            try:
                # CPU usage
                cpu_percent = self.psutil.cpu_percent(interval=None)
                snapshot['cpu_percent'] = cpu_percent

                # Memory usage
                memory = self.psutil.virtual_memory()
                snapshot['memory_mb'] = memory.used / (1024 * 1024)
                snapshot['memory_percent'] = memory.percent

            except Exception as e:
                logger.warning(f"Failed to get CPU/Memory stats: {e}")

        # GPU
        if self.has_pynvml:
            try:
                gpu_stats = self._get_gpu_stats()
                if gpu_stats:
                    snapshot['gpu_stats'] = gpu_stats
            except Exception as e:
                logger.warning(f"Failed to get GPU stats: {e}")

        return snapshot if snapshot else None

    def _get_gpu_stats(self) -> Optional[Dict[str, float]]:
        """Get GPU statistics"""
        try:
            # Get first GPU (can be extended for multi-GPU)
            handle = self.pynvml.nvmlDeviceGetHandleByIndex(0)

            # GPU utilization
            util = self.pynvml.nvmlDeviceGetUtilizationRates(handle)

            # Memory info
            mem_info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)

            return {
                'utilization': util.gpu,
                'memory_utilization': util.memory,
                'memory_used_mb': mem_info.used / (1024 * 1024),
                'memory_total_mb': mem_info.total / (1024 * 1024),
                'memory_free_mb': mem_info.free / (1024 * 1024)
            }

        except Exception as e:
            logger.debug(f"GPU stats error: {e}")
            return None

    def get_snapshot(self) -> Optional[Dict[str, Any]]:
        """Get current resource usage snapshot"""
        return self._take_snapshot()

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of monitored resources"""
        import statistics

        summary = {}

        # CPU summary
        if self.cpu_measurements:
            summary['cpu'] = {
                'avg_percent': statistics.mean(self.cpu_measurements),
                'max_percent': max(self.cpu_measurements),
                'min_percent': min(self.cpu_measurements)
            }

        # Memory summary
        if self.memory_measurements:
            summary['memory'] = {
                'avg_mb': statistics.mean(self.memory_measurements),
                'max_mb': max(self.memory_measurements),
                'min_mb': min(self.memory_measurements)
            }

        # GPU summary
        if self.gpu_measurements:
            summary['gpu'] = {
                'avg_utilization': statistics.mean([g.get('utilization', 0) for g in self.gpu_measurements]),
                'max_utilization': max([g.get('utilization', 0) for g in self.gpu_measurements]),
                'avg_memory_mb': statistics.mean([g.get('memory_used_mb', 0) for g in self.gpu_measurements]),
                'max_memory_mb': max([g.get('memory_used_mb', 0) for g in self.gpu_measurements])
            }

        return summary


class SimpleResourceMonitor:
    """
    Simplified resource monitor without threading

    Use this if you only need periodic snapshots
    """

    def __init__(self):
        """Initialize simple monitor"""
        self._check_dependencies()

    def _check_dependencies(self) -> None:
        """Check available monitoring tools"""
        try:
            import psutil
            self.psutil = psutil
            self.has_psutil = True
        except ImportError:
            self.has_psutil = False
            logger.warning("psutil not available")

        try:
            import pynvml
            pynvml.nvmlInit()
            self.pynvml = pynvml
            self.has_pynvml = True
        except (ImportError, Exception):
            self.has_pynvml = False

    def get_current_usage(self) -> Dict[str, Any]:
        """Get current resource usage"""
        usage = {}

        if self.has_psutil:
            usage['cpu_percent'] = self.psutil.cpu_percent(interval=0.1)
            mem = self.psutil.virtual_memory()
            usage['memory_mb'] = mem.used / (1024 * 1024)
            usage['memory_percent'] = mem.percent

        if self.has_pynvml:
            try:
                handle = self.pynvml.nvmlDeviceGetHandleByIndex(0)
                util = self.pynvml.nvmlDeviceGetUtilizationRates(handle)
                mem_info = self.pynvml.nvmlDeviceGetMemoryInfo(handle)

                usage['gpu'] = {
                    'utilization': util.gpu,
                    'memory_used_mb': mem_info.used / (1024 * 1024),
                    'memory_total_mb': mem_info.total / (1024 * 1024)
                }
            except Exception as e:
                logger.debug(f"GPU monitoring error: {e}")

        return usage
