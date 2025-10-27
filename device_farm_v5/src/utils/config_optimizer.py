"""
Optimized configuration management for Device Farm v5
"""

import json
import os
import threading
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from loguru import logger


class OptimizedConfigManager:
    """
    Optimized configuration manager with caching and validation

    Features:
    - Configuration caching for performance
    - Thread-safe operations
    - Validation and error handling
    - Environment-specific configs
    - Hot reloading capabilities
    """

    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self._config_cache = {}
        self._cache_lock = threading.Lock()
        self._file_timestamps = {}
        self._watchers = {}

    @lru_cache(maxsize=32)
    def load_config_file(self, file_path: str, file_type: str = "auto") -> Dict[str, Any]:
        """
        Load configuration file with caching

        Args:
            file_path: Path to configuration file
            file_type: File type ('json', 'yaml', 'auto')

        Returns:
            Configuration dictionary
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"⚠️ Configuration file not found: {file_path}")
                return {}

            # Determine file type
            if file_type == "auto":
                if path.suffix.lower() in [".yaml", ".yml"]:
                    file_type = "yaml"
                elif path.suffix.lower() == ".json":
                    file_type = "json"
                else:
                    logger.error(f"❌ Unsupported file type: {path.suffix}")
                    return {}

            # Load configuration
            with open(path, "r", encoding="utf-8") as f:
                if file_type == "yaml":
                    config = yaml.safe_load(f)
                elif file_type == "json":
                    config = json.load(f)
                else:
                    logger.error(f"❌ Invalid file type: {file_type}")
                    return {}

            # Record timestamp for change detection
            self._file_timestamps[str(path)] = path.stat().st_mtime

            logger.debug(f"📋 Loaded configuration: {file_path}")
            return config or {}

        except Exception as e:
            logger.error(f"❌ Error loading configuration {file_path}: {e}")
            return {}

    def get_config(self, config_name: str, reload_if_changed: bool = True) -> Dict[str, Any]:
        """
        Get configuration with optional hot reloading

        Args:
            config_name: Name of configuration
            reload_if_changed: Whether to reload if file changed

        Returns:
            Configuration dictionary
        """
        with self._cache_lock:
            # Check if we need to reload
            if reload_if_changed and config_name in self._config_cache:
                config_path = self.config_dir / f"{config_name}.yaml"
                if config_path.exists():
                    current_mtime = config_path.stat().st_mtime
                    cached_mtime = self._file_timestamps.get(str(config_path), 0)

                    if current_mtime > cached_mtime:
                        logger.info(f"🔄 Configuration changed, reloading: {config_name}")
                        # Clear cache for this config
                        if config_name in self._config_cache:
                            del self._config_cache[config_name]
                        self.load_config_file.cache_clear()

            # Load from cache or file
            if config_name not in self._config_cache:
                config_paths = [
                    self.config_dir / f"{config_name}.yaml",
                    self.config_dir / f"{config_name}.json",
                ]

                config_loaded = False
                for config_path in config_paths:
                    if config_path.exists():
                        self._config_cache[config_name] = self.load_config_file(str(config_path))
                        config_loaded = True
                        break

                if not config_loaded:
                    logger.warning(f"⚠️ Configuration not found: {config_name}")
                    self._config_cache[config_name] = {}

            return self._config_cache[config_name].copy()

    def merge_configs(
        self, base_config: Dict[str, Any], override_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merge configurations with deep merge

        Args:
            base_config: Base configuration
            override_config: Configuration to override base

        Returns:
            Merged configuration
        """
        result = base_config.copy()

        for key, value in override_config.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_configs(result[key], value)
            else:
                result[key] = value

        return result

    def get_environment_config(self, config_name: str, environment: str = None) -> Dict[str, Any]:
        """
        Get environment-specific configuration

        Args:
            config_name: Base configuration name
            environment: Environment name (dev, prod, test)

        Returns:
            Environment-specific configuration
        """
        # Get environment from env var if not provided
        if environment is None:
            environment = os.getenv("ENVIRONMENT", "dev")

        # Load base configuration
        base_config = self.get_config(config_name)

        # Load environment-specific override
        env_config_name = f"{config_name}_{environment}"
        env_config = self.get_config(env_config_name)

        # Merge configurations
        if env_config:
            return self.merge_configs(base_config, env_config)

        return base_config

    def validate_config(self, config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """
        Validate configuration against schema

        Args:
            config: Configuration to validate
            schema: Validation schema

        Returns:
            True if valid, False otherwise
        """
        try:
            # Simple validation - can be extended with jsonschema
            for key, expected_type in schema.items():
                if key not in config:
                    logger.error(f"❌ Missing required config key: {key}")
                    return False

                if not isinstance(config[key], expected_type):
                    logger.error(
                        f"❌ Invalid type for {key}: expected {expected_type}, got {type(config[key])}"
                    )
                    return False

            return True

        except Exception as e:
            logger.error(f"❌ Configuration validation error: {e}")
            return False

    def clear_cache(self):
        """Clear configuration cache"""
        with self._cache_lock:
            self._config_cache.clear()
            self._file_timestamps.clear()
            self.load_config_file.cache_clear()

        logger.info("🧹 Configuration cache cleared")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._cache_lock:
            return {
                "cached_configs": list(self._config_cache.keys()),
                "cache_size": len(self._config_cache),
                "file_timestamps": len(self._file_timestamps),
                "lru_cache_info": self.load_config_file.cache_info()._asdict(),
            }


# Global optimized config manager
_optimized_config_manager = OptimizedConfigManager()


def get_optimized_config(config_name: str, environment: str = None) -> Dict[str, Any]:
    """Get optimized configuration"""
    return _optimized_config_manager.get_environment_config(config_name, environment)


def clear_config_cache():
    """Clear global configuration cache"""
    _optimized_config_manager.clear_cache()


def get_config_stats() -> Dict[str, Any]:
    """Get global configuration statistics"""
    return _optimized_config_manager.get_cache_stats()


# Pre-defined configuration schemas for validation
CONFIG_SCHEMAS = {
    "database": {"host": str, "port": int, "name": str, "user": str, "password": str},
    "adb": {"timeout": int, "max_retries": int, "screenshot_format": str},
    "ml_models": {"yolo_screenshot": dict, "anomaly_detector": dict},
    "gologin": {"api_key": str, "base_url": str, "max_profiles": int},
    "performance": {
        "monitoring_interval": (int, float),
        "memory_threshold": (int, float),
        "cleanup_interval": (int, float),
    },
}
