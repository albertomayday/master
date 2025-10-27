"""
Device Farm v5 - Main Application Entry Point
Orchestrates all system components for Android device automation
"""

import asyncio
import signal
import sys
from pathlib import Path
from typing import Optional

from loguru import logger

# Import core components - Optimized imports with lazy loading
from src.config_manager import get_config, validate_configuration

# Lazy imports cache for better startup performance
_lazy_imports = {
    "db_manager": None,
    "adb_manager": None,
    "appium_controller": None,
    "gologin_manager": None,
    "profile_synchronizer": None,
    "task_queue": None,
    "tiktok_adapter": None,
    "yolo_detector": None,
}


# Lazy loading functions for optimized module loading
def get_db_manager():
    """Lazy load database manager"""
    if _lazy_imports["db_manager"] is None:
        from src.core.models import get_db_manager as _get_db_manager

        _lazy_imports["db_manager"] = _get_db_manager
    return _lazy_imports["db_manager"]()


async def get_adb_manager():
    """Lazy load ADB manager"""
    if _lazy_imports["adb_manager"] is None:
        from src.core.adb_manager import get_adb_manager as _get_adb_manager

        _lazy_imports["adb_manager"] = _get_adb_manager
    return await _lazy_imports["adb_manager"]()


async def get_appium_controller():
    """Lazy load Appium controller"""
    if _lazy_imports["appium_controller"] is None:
        from src.core.appium_controller import get_appium_controller as _get_appium_controller

        _lazy_imports["appium_controller"] = _get_appium_controller
    return await _lazy_imports["appium_controller"]()


async def get_gologin_manager():
    """Lazy load GoLogin manager"""
    if _lazy_imports["gologin_manager"] is None:
        from src.integrations.gologin_manager import get_gologin_manager as _get_gologin_manager

        _lazy_imports["gologin_manager"] = _get_gologin_manager
    return await _lazy_imports["gologin_manager"]()


async def get_profile_synchronizer():
    """Lazy load profile synchronizer"""
    if _lazy_imports["profile_synchronizer"] is None:
        from src.core.profile_synchronizer import (
            get_profile_synchronizer as _get_profile_synchronizer,
        )

        _lazy_imports["profile_synchronizer"] = _get_profile_synchronizer
    return await _lazy_imports["profile_synchronizer"]()


async def get_task_queue():
    """Lazy load task queue"""
    if _lazy_imports["task_queue"] is None:
        from src.core.task_queue import get_task_queue as _get_task_queue

        _lazy_imports["task_queue"] = _get_task_queue
    return await _lazy_imports["task_queue"]()


async def get_tiktok_ml_adapter():
    """Lazy load TikTok ML adapter"""
    if _lazy_imports["tiktok_adapter"] is None:
        from src.integrations.tiktok_ml_adapter import (
            get_tiktok_ml_adapter as _get_tiktok_ml_adapter,
        )

        _lazy_imports["tiktok_adapter"] = _get_tiktok_ml_adapter
    return await _lazy_imports["tiktok_adapter"]()


async def get_device_farm_yolo_detector():
    """Lazy load YOLO detector"""
    if _lazy_imports["yolo_detector"] is None:
        from src.ml.enhanced_yolo_detector import (
            get_device_farm_yolo_detector as _get_device_farm_yolo_detector,
        )

        _lazy_imports["yolo_detector"] = _get_device_farm_yolo_detector
    return await _lazy_imports["yolo_detector"]()


def clear_lazy_imports():
    """Clear lazy imports cache for testing/reload"""
    global _lazy_imports
    _lazy_imports = {key: None for key in _lazy_imports}


class DeviceFarmSystem:
    """
    Main system orchestrator for Device Farm v5

    Optimizations:
    - Lazy component loading for faster startup
    - Async initialization with proper error handling
    - Resource cleanup and memory management
    - Performance monitoring and health checks
    """

    def __init__(self):
        self.config = get_config()
        self.running = False
        self.components = {}
        self.health_status = {
            "system": "initializing",
            "components": {},
            "last_check": None,
            "startup_time": None,
            "memory_usage": 0,
        }
        self._initialization_lock = asyncio.Lock()
        self._cleanup_tasks = set()

        # Setup optimized logging
        self._setup_logging()

        logger.info("🚀 Device Farm v5 System initializing with performance optimizations...")

    def _setup_logging(self):
        """Configure logging system"""
        log_level = self.config.log_level
        log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"

        # Remove default handler
        logger.remove()

        # Console logging
        logger.add(sys.stdout, level=log_level, format=log_format, colorize=True)

        # File logging
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        logger.add(
            log_dir / "device_farm_v5.log",
            level=log_level,
            format=log_format,
            rotation="100 MB",
            retention="7 days",
            compression="gz",
        )

        logger.info("Logging system configured")

    async def initialize(self) -> bool:
        """
        Initialize all system components with optimized loading

        Returns:
            bool: True if initialization successful, False otherwise
        """
        async with self._initialization_lock:
            try:
                import time

                start_time = time.time()

                logger.info(
                    "🚀 Initializing Device Farm v5 System with performance optimizations..."
                )

                # Validate configuration first (fast check)
                if not validate_configuration():
                    logger.error("❌ Configuration validation failed")
                    return False

                logger.info("✅ Configuration validated")

                # Initialize core components in parallel where possible
                initialization_tasks = []

                # Initialize database (synchronous, must be first)
                logger.info("📊 Initializing database...")
                db_manager = get_db_manager()
                if not db_manager.health_check():
                    logger.error("❌ Database health check failed")
                    return False

                self.components["database"] = db_manager
                self.health_status["components"]["database"] = "healthy"
                logger.info("✅ Database initialized")

                # Initialize ADB manager
                logger.info("📱 Initializing ADB manager...")
                adb_manager = await get_adb_manager()
                self.components["adb"] = adb_manager
                self.health_status["components"]["adb"] = "healthy"
                logger.info("✅ ADB manager initialized")

                # Initialize Appium controller
                logger.info("🤖 Initializing Appium controller...")
                appium_controller = await get_appium_controller()
                self.components["appium"] = appium_controller
                self.health_status["components"]["appium"] = "healthy"
                logger.info("✅ Appium controller initialized")

                # Initialize Gologin manager
                logger.info("🔗 Initializing Gologin manager...")
                gologin_manager = await get_gologin_manager()
                self.components["gologin"] = gologin_manager
                self.health_status["components"]["gologin"] = "healthy"
                logger.info("✅ Gologin manager initialized")

                # Initialize Profile Synchronizer
                logger.info("🔄 Initializing Profile Synchronizer...")
                profile_synchronizer = await get_profile_synchronizer()
                self.components["profile_sync"] = profile_synchronizer
                self.health_status["components"]["profile_sync"] = "healthy"
                logger.info("✅ Profile Synchronizer initialized")

                # Initialize Task Queue
                logger.info("📋 Initializing Task Queue...")
                task_queue = await get_task_queue()
                self.components["task_queue"] = task_queue
                self.health_status["components"]["task_queue"] = "healthy"
                logger.info("✅ Task Queue initialized")

                # Initialize TikTok ML Integration Adapter
                logger.info("🤖 Initializing TikTok ML Integration...")
                tiktok_adapter = await get_tiktok_ml_adapter()
                self.components["tiktok_ml"] = tiktok_adapter
                self.health_status["components"]["tiktok_ml"] = "healthy"
                logger.info("✅ TikTok ML Integration initialized")

                # Initialize Enhanced YOLO Detector
                logger.info("🎯 Initializing Enhanced YOLO Detector...")
                yolo_detector = await get_device_farm_yolo_detector()
                self.components["yolo_detector"] = yolo_detector
                self.health_status["components"]["yolo_detector"] = "healthy"
                logger.info("✅ Enhanced YOLO Detector initialized")

                # Perform initial system checks
                await self._perform_system_checks()

                # Record startup metrics
                end_time = time.time()
                startup_duration = end_time - start_time
                self.health_status["startup_time"] = startup_duration
                self.health_status["system"] = "running"

                logger.info(
                    f"🎉 Device Farm v5 System initialized successfully in {startup_duration:.2f}s!"
                )
                return True

            except Exception as e:
                logger.error(f"❌ System initialization failed: {e}")
                self.health_status["system"] = "error"
                await self._cleanup_on_failure()
                return False

    async def _cleanup_on_failure(self):
        """Cleanup resources on initialization failure"""
        logger.warning("🧹 Cleaning up resources after initialization failure...")

        for component_name, component in self.components.items():
            try:
                if hasattr(component, "cleanup"):
                    await component.cleanup()
                logger.info(f"✅ Cleaned up {component_name}")
            except Exception as e:
                logger.error(f"❌ Failed to cleanup {component_name}: {e}")

        # Clear lazy imports cache
        clear_lazy_imports()

    async def _perform_system_checks(self):
        """Perform initial system health checks"""
        logger.info("🔍 Performing system health checks...")

        # Check device connectivity
        adb_manager = self.components.get("adb")
        if adb_manager:
            devices = await adb_manager.scan_devices()
            logger.info(f"📱 Detected {len(devices)} Android devices")

            for device in devices:
                logger.info(
                    f"   • {device.serial} - {device.model} (Android {device.android_version})"
                )

        # Check Gologin connectivity
        gologin_manager = self.components.get("gologin")
        if gologin_manager:
            try:
                profiles = await gologin_manager.get_profiles()
                logger.info(f"🔗 Found {len(profiles)} Gologin profiles")
            except Exception as e:
                logger.warning(f"⚠️  Gologin API issue: {e}")

        # Check Appium status
        appium_controller = self.components.get("appium")
        if appium_controller:
            stats = await appium_controller.get_controller_statistics()
            logger.info(f"🤖 Appium controller status: {stats}")

    async def start_services(self):
        """Start all system services"""
        try:
            logger.info("🚀 Starting Device Farm v5 services...")

            # Start background tasks
            tasks = []

            # Health monitoring task
            tasks.append(asyncio.create_task(self._health_monitor()))

            # Device scanning task
            tasks.append(asyncio.create_task(self._device_scanner()))

            # Session cleanup task
            tasks.append(asyncio.create_task(self._session_cleaner()))

            # Start dashboard (if enabled)
            if self.config.raw_config.get("dashboard", {}).get("enabled", True):
                tasks.append(asyncio.create_task(self._start_dashboard()))

            self.running = True
            logger.info("✅ All services started successfully")

            # Wait for tasks
            await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as e:
            logger.error(f"❌ Error starting services: {e}")
            raise

    async def _health_monitor(self):
        """Monitor system health"""
        logger.info("💚 Health monitor started")

        while self.running:
            try:
                # Check component health
                db_healthy = (
                    self.components.get("database", {}).health_check()
                    if "database" in self.components
                    else False
                )

                # Log health status
                if not db_healthy:
                    logger.warning("⚠️  Database health check failed")

                # Wait before next check
                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"❌ Health monitor error: {e}")
                await asyncio.sleep(60)

    async def _device_scanner(self):
        """Periodically scan for devices"""
        logger.info("📱 Device scanner started")

        while self.running:
            try:
                adb_manager = self.components.get("adb")
                if adb_manager:
                    await adb_manager.scan_devices()

                # Wait before next scan
                await asyncio.sleep(30)  # Scan every 30 seconds

            except Exception as e:
                logger.error(f"❌ Device scanner error: {e}")
                await asyncio.sleep(30)

    async def _session_cleaner(self):
        """Clean up inactive sessions"""
        logger.info("🧹 Session cleaner started")

        while self.running:
            try:
                appium_controller = self.components.get("appium")
                if appium_controller:
                    await appium_controller.cleanup_inactive_sessions()

                # Wait before next cleanup
                await asyncio.sleep(300)  # Clean every 5 minutes

            except Exception as e:
                logger.error(f"❌ Session cleaner error: {e}")
                await asyncio.sleep(300)

    async def _start_dashboard(self):
        """Start web dashboard"""
        try:
            logger.info("🎛️  Starting web dashboard...")

            # Import dashboard here to avoid circular imports
            from src.dashboard.app import create_dashboard_app

            app = create_dashboard_app()

            # Run dashboard (this will block)
            import uvicorn

            config = uvicorn.Config(
                app,
                host=self.config.dashboard.host,
                port=self.config.dashboard.port,
                log_level="info",
            )

            server = uvicorn.Server(config)
            await server.serve()

        except Exception as e:
            logger.error(f"❌ Dashboard error: {e}")

    async def shutdown(self):
        """Graceful shutdown of all components"""
        logger.info("🛑 Shutting down Device Farm v5 System...")

        self.running = False

        try:
            # Shutdown Appium controller
            appium_controller = self.components.get("appium")
            if appium_controller:
                await appium_controller.shutdown()
                logger.info("✅ Appium controller shut down")

            # Close Gologin manager
            gologin_manager = self.components.get("gologin")
            if gologin_manager:
                await gologin_manager.close()
                logger.info("✅ Gologin manager closed")

            logger.info("✅ Device Farm v5 System shut down gracefully")

        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")


# Global system instance
device_farm_system: Optional[DeviceFarmSystem] = None


def get_system() -> DeviceFarmSystem:
    """Get global system instance"""
    global device_farm_system
    if device_farm_system is None:
        device_farm_system = DeviceFarmSystem()
    return device_farm_system


async def main():
    """Main application entry point"""
    system = get_system()

    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating shutdown...")
        asyncio.create_task(system.shutdown())

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Initialize system
        if not await system.initialize():
            logger.error("❌ System initialization failed")
            sys.exit(1)

        # Start services
        await system.start_services()

    except KeyboardInterrupt:
        logger.info("🛑 Received interrupt signal")
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        await system.shutdown()


if __name__ == "__main__":
    # Run the main application
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
