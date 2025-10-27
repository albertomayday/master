"""
Performance monitoring and optimization utilities
"""

import asyncio
import functools
import gc
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

import psutil
from loguru import logger


@dataclass
class PerformanceMetrics:
    """Performance metrics container"""

    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    memory_available: float = 0.0
    disk_usage: float = 0.0
    network_io: Dict[str, float] = field(default_factory=dict)
    process_count: int = 0
    thread_count: int = 0
    timestamp: float = field(default_factory=time.time)


class PerformanceMonitor:
    """Advanced performance monitoring and optimization"""

    def __init__(self, collection_interval: float = 5.0):
        self.collection_interval = collection_interval
        self.metrics_history = deque(maxlen=1000)
        self.function_timings = defaultdict(list)
        self.memory_thresholds = {
            "warning": 80.0,  # 80% memory usage warning
            "critical": 90.0,  # 90% memory usage critical
        }
        self._monitoring = False
        self._monitor_task = None

    async def start_monitoring(self):
        """Start continuous performance monitoring"""
        if self._monitoring:
            return

        self._monitoring = True
        self._monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("🔍 Performance monitoring started")

    async def stop_monitoring(self):
        """Stop performance monitoring"""
        self._monitoring = False
        if self._monitor_task:
            self._monitor_task.cancel()
            try:
                await self._monitor_task
            except asyncio.CancelledError:
                pass

        logger.info("⏹️ Performance monitoring stopped")

    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self._monitoring:
            try:
                metrics = self.collect_metrics()
                self.metrics_history.append(metrics)

                # Check thresholds and alert
                await self._check_thresholds(metrics)

                await asyncio.sleep(self.collection_interval)

            except Exception as e:
                logger.error(f"❌ Error in performance monitoring: {e}")
                await asyncio.sleep(self.collection_interval)

    def collect_metrics(self) -> PerformanceMetrics:
        """Collect current system metrics"""
        try:
            # CPU and Memory
            cpu_usage = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()

            # Disk usage
            disk = psutil.disk_usage("/")
            disk_usage = (disk.used / disk.total) * 100

            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv,
            }

            # Process info
            process = psutil.Process()

            return PerformanceMetrics(
                cpu_usage=cpu_usage,
                memory_usage=memory.percent,
                memory_available=memory.available / (1024**3),  # GB
                disk_usage=disk_usage,
                network_io=network_io,
                process_count=len(psutil.pids()),
                thread_count=process.num_threads(),
            )

        except Exception as e:
            logger.error(f"❌ Error collecting metrics: {e}")
            return PerformanceMetrics()

    async def _check_thresholds(self, metrics: PerformanceMetrics):
        """Check performance thresholds and alert if needed"""
        # Memory usage check
        if metrics.memory_usage >= self.memory_thresholds["critical"]:
            logger.critical(f"🚨 CRITICAL: Memory usage at {metrics.memory_usage:.1f}%")
            await self._trigger_memory_cleanup()
        elif metrics.memory_usage >= self.memory_thresholds["warning"]:
            logger.warning(f"⚠️ WARNING: Memory usage at {metrics.memory_usage:.1f}%")

    async def _trigger_memory_cleanup(self):
        """Trigger memory cleanup procedures"""
        logger.info("🧹 Triggering memory cleanup...")

        # Force garbage collection
        collected = gc.collect()
        logger.info(f"🗑️ Garbage collected: {collected} objects")

        # Additional cleanup can be added here
        # - Clear caches
        # - Release unused resources
        # - Compact data structures

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics_history:
            return {"status": "no_data"}

        recent_metrics = list(self.metrics_history)[-10:]  # Last 10 measurements

        avg_cpu = sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m.memory_usage for m in recent_metrics) / len(recent_metrics)
        avg_threads = sum(m.thread_count for m in recent_metrics) / len(recent_metrics)

        return {
            "status": "healthy" if avg_memory < 80 else "warning",
            "avg_cpu_usage": round(avg_cpu, 2),
            "avg_memory_usage": round(avg_memory, 2),
            "avg_thread_count": round(avg_threads, 2),
            "memory_available_gb": recent_metrics[-1].memory_available,
            "measurements_count": len(self.metrics_history),
            "function_timings": dict(self.function_timings),
        }


def performance_monitor(func_name: Optional[str] = None):
    """Decorator for monitoring function performance"""

    def decorator(func: Callable) -> Callable:
        name = func_name or f"{func.__module__}.{func.__name__}"

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                _global_monitor.function_timings[name].append(duration)
                # Keep only last 100 measurements
                if len(_global_monitor.function_timings[name]) > 100:
                    _global_monitor.function_timings[name] = _global_monitor.function_timings[name][
                        -100:
                    ]

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration = time.time() - start_time
                _global_monitor.function_timings[name].append(duration)
                # Keep only last 100 measurements
                if len(_global_monitor.function_timings[name]) > 100:
                    _global_monitor.function_timings[name] = _global_monitor.function_timings[name][
                        -100:
                    ]

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


class ResourceManager:
    """Advanced resource management and cleanup"""

    def __init__(self):
        self.managed_resources = {}
        self._cleanup_handlers = []
        self._lock = threading.Lock()

    def register_resource(self, name: str, resource: Any, cleanup_func: Callable = None):
        """Register a resource for management"""
        with self._lock:
            self.managed_resources[name] = {
                "resource": resource,
                "cleanup_func": cleanup_func,
                "created_at": time.time(),
            }

    def unregister_resource(self, name: str):
        """Unregister and cleanup a resource"""
        with self._lock:
            if name in self.managed_resources:
                resource_info = self.managed_resources.pop(name)
                if resource_info["cleanup_func"]:
                    try:
                        resource_info["cleanup_func"](resource_info["resource"])
                    except Exception as e:
                        logger.error(f"❌ Error cleaning up resource {name}: {e}")

    async def cleanup_all(self):
        """Cleanup all managed resources"""
        logger.info("🧹 Cleaning up all managed resources...")

        with self._lock:
            resources_to_cleanup = list(self.managed_resources.items())

        for name, resource_info in resources_to_cleanup:
            try:
                if resource_info["cleanup_func"]:
                    if asyncio.iscoroutinefunction(resource_info["cleanup_func"]):
                        await resource_info["cleanup_func"](resource_info["resource"])
                    else:
                        resource_info["cleanup_func"](resource_info["resource"])

                logger.info(f"✅ Cleaned up resource: {name}")
            except Exception as e:
                logger.error(f"❌ Error cleaning up resource {name}: {e}")

        with self._lock:
            self.managed_resources.clear()


class MemoryOptimizer:
    """Memory optimization utilities"""

    @staticmethod
    def optimize_memory():
        """Perform memory optimization"""
        logger.info("🧠 Starting memory optimization...")

        # Force garbage collection
        collected = gc.collect()

        # Get memory info before optimization
        memory_before = psutil.virtual_memory().percent

        # Additional optimization techniques
        gc.set_threshold(700, 10, 10)  # Optimize GC thresholds

        memory_after = psutil.virtual_memory().percent

        logger.info(f"✅ Memory optimization completed:")
        logger.info(f"   • Collected {collected} objects")
        logger.info(f"   • Memory usage: {memory_before:.1f}% → {memory_after:.1f}%")

        return {
            "objects_collected": collected,
            "memory_before": memory_before,
            "memory_after": memory_after,
            "improvement": memory_before - memory_after,
        }


# Global instances
_global_monitor = PerformanceMonitor()
_global_resource_manager = ResourceManager()


# Export functions
async def start_performance_monitoring():
    """Start global performance monitoring"""
    await _global_monitor.start_monitoring()


async def stop_performance_monitoring():
    """Stop global performance monitoring"""
    await _global_monitor.stop_monitoring()


def get_performance_summary():
    """Get global performance summary"""
    return _global_monitor.get_performance_summary()


def register_resource(name: str, resource: Any, cleanup_func: Callable = None):
    """Register a global resource"""
    _global_resource_manager.register_resource(name, resource, cleanup_func)


async def cleanup_all_resources():
    """Cleanup all global resources"""
    await _global_resource_manager.cleanup_all()
