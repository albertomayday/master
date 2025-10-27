#!/usr/bin/env python3
"""
Automated code cleanup and optimization script for Device Farm v5
Run this script to perform comprehensive code cleanup and optimization
"""

import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path

from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.utils.code_quality import CodeFormatter, analyze_codebase, format_codebase
    from src.utils.config_optimizer import clear_config_cache, get_config_stats
    from src.utils.performance import (
        MemoryOptimizer,
        start_performance_monitoring,
        stop_performance_monitoring,
    )
except ImportError as e:
    logger.error(f"❌ Failed to import utilities: {e}")
    sys.exit(1)


class AutoCleanup:
    """Automated cleanup and optimization"""

    def __init__(self):
        self.start_time = time.time()
        self.results = {
            "code_analysis": {},
            "code_formatting": {},
            "performance_optimization": {},
            "config_optimization": {},
            "errors": [],
        }

    async def run_comprehensive_cleanup(self, target_dir: str = None) -> Dict[str, Any]:
        """Run comprehensive cleanup process"""
        logger.info("🧹 Starting comprehensive code cleanup and optimization...")

        target_dir = target_dir or str(project_root)

        try:
            # Step 1: Start performance monitoring
            await self.start_monitoring()

            # Step 2: Code analysis
            await self.analyze_code(target_dir)

            # Step 3: Code formatting
            await self.format_code(target_dir)

            # Step 4: Performance optimization
            await self.optimize_performance()

            # Step 5: Configuration optimization
            await self.optimize_configuration()

            # Step 6: Generate report
            report = self.generate_report()

            # Step 7: Stop monitoring
            await self.stop_monitoring()

            logger.info("✅ Comprehensive cleanup completed successfully!")
            return report

        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
            self.results["errors"].append(str(e))
            return self.results

    async def start_monitoring(self):
        """Start performance monitoring"""
        try:
            await start_performance_monitoring()
            logger.info("📊 Performance monitoring started")
        except Exception as e:
            logger.error(f"❌ Failed to start monitoring: {e}")
            self.results["errors"].append(f"Monitoring error: {e}")

    async def stop_monitoring(self):
        """Stop performance monitoring"""
        try:
            await stop_performance_monitoring()
            logger.info("⏹️ Performance monitoring stopped")
        except Exception as e:
            logger.error(f"❌ Failed to stop monitoring: {e}")

    async def analyze_code(self, target_dir: str):
        """Analyze code quality"""
        logger.info("🔍 Analyzing code quality...")

        try:
            self.results["code_analysis"] = analyze_codebase(target_dir)

            # Log analysis summary
            analysis = self.results["code_analysis"]
            logger.info(f"📋 Code Analysis Summary:")
            logger.info(f"   • Files analyzed: {analysis.get('files_analyzed', 0)}")
            logger.info(f"   • Syntax errors: {len(analysis.get('syntax_errors', []))}")
            logger.info(f"   • Complexity issues: {len(analysis.get('complexity_issues', []))}")
            logger.info(f"   • Flake8 issues: {len(analysis.get('flake8_issues', []))}")

        except Exception as e:
            logger.error(f"❌ Code analysis failed: {e}")
            self.results["errors"].append(f"Code analysis error: {e}")

    async def format_code(self, target_dir: str):
        """Format code for consistency"""
        logger.info("🎨 Formatting code...")

        try:
            self.results["code_formatting"] = format_codebase(target_dir)

            # Log formatting summary
            formatting = self.results["code_formatting"]
            logger.info(f"📋 Code Formatting Summary:")
            logger.info(f"   • Files formatted: {formatting.get('files_formatted', 0)}")
            logger.info(f"   • Formatting errors: {len(formatting.get('formatting_errors', []))}")

        except Exception as e:
            logger.error(f"❌ Code formatting failed: {e}")
            self.results["errors"].append(f"Code formatting error: {e}")

    async def optimize_performance(self):
        """Optimize system performance"""
        logger.info("🚀 Optimizing performance...")

        try:
            # Memory optimization
            memory_results = MemoryOptimizer.optimize_memory()

            self.results["performance_optimization"] = {
                "memory_optimization": memory_results,
                "cleanup_completed": True,
            }

            logger.info("✅ Performance optimization completed")

        except Exception as e:
            logger.error(f"❌ Performance optimization failed: {e}")
            self.results["errors"].append(f"Performance optimization error: {e}")

    async def optimize_configuration(self):
        """Optimize configuration management"""
        logger.info("⚙️ Optimizing configuration...")

        try:
            # Clear config cache
            clear_config_cache()

            # Get config stats
            config_stats = get_config_stats()

            self.results["config_optimization"] = {
                "cache_cleared": True,
                "config_stats": config_stats,
            }

            logger.info("✅ Configuration optimization completed")

        except Exception as e:
            logger.error(f"❌ Configuration optimization failed: {e}")
            self.results["errors"].append(f"Configuration optimization error: {e}")

    def generate_report(self) -> Dict[str, Any]:
        """Generate cleanup report"""
        duration = time.time() - self.start_time

        report = {
            "cleanup_completed": True,
            "duration_seconds": round(duration, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": self.results,
            "summary": self._generate_summary(),
        }

        # Save report to file
        report_path = project_root / "cleanup_report.json"
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

            logger.info(f"📊 Cleanup report saved: {report_path}")

        except Exception as e:
            logger.error(f"❌ Failed to save report: {e}")

        return report

    def _generate_summary(self) -> Dict[str, Any]:
        """Generate cleanup summary"""
        analysis = self.results.get("code_analysis", {})
        formatting = self.results.get("code_formatting", {})

        return {
            "total_files_processed": analysis.get("files_analyzed", 0),
            "files_formatted": formatting.get("files_formatted", 0),
            "syntax_errors_found": len(analysis.get("syntax_errors", [])),
            "complexity_issues_found": len(analysis.get("complexity_issues", [])),
            "flake8_issues_found": len(analysis.get("flake8_issues", [])),
            "total_errors": len(self.results.get("errors", [])),
            "optimization_successful": len(self.results.get("errors", [])) == 0,
        }


def print_banner():
    """Print cleanup banner"""
    banner = """
╔════════════════════════════════════════════════════════════════════════════════╗
║                     🧹 DEVICE FARM V5 CODE CLEANUP                           ║
║                                                                                ║
║  Automated code cleanup and optimization system                                ║
║  • Code analysis and quality checks                                            ║
║  • Automatic formatting with Black & isort                                     ║
║  • Performance optimization                                                     ║
║  • Configuration management                                                     ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


async def main():
    """Main cleanup function"""
    parser = argparse.ArgumentParser(description="Device Farm v5 Code Cleanup")
    parser.add_argument("--target", "-t", default=None, help="Target directory to clean")
    parser.add_argument("--analysis-only", "-a", action="store_true", help="Run analysis only")
    parser.add_argument("--format-only", "-f", action="store_true", help="Run formatting only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Configure logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger.remove()
    logger.add(sys.stdout, level=log_level, format="{time:HH:mm:ss} | {level} | {message}")

    print_banner()

    # Initialize cleanup
    cleanup = AutoCleanup()

    try:
        if args.analysis_only:
            logger.info("🔍 Running code analysis only...")
            target_dir = args.target or str(project_root)
            await cleanup.analyze_code(target_dir)
            report = cleanup.generate_report()

        elif args.format_only:
            logger.info("🎨 Running code formatting only...")
            target_dir = args.target or str(project_root)
            await cleanup.format_code(target_dir)
            report = cleanup.generate_report()

        else:
            # Full cleanup
            report = await cleanup.run_comprehensive_cleanup(args.target)

        # Print summary
        summary = report.get("summary", {})
        print("\n" + "=" * 80)
        print("📊 CLEANUP SUMMARY")
        print("=" * 80)
        print(f"✅ Total files processed: {summary.get('total_files_processed', 0)}")
        print(f"🎨 Files formatted: {summary.get('files_formatted', 0)}")
        print(f"🐛 Syntax errors found: {summary.get('syntax_errors_found', 0)}")
        print(f"🔍 Complexity issues: {summary.get('complexity_issues_found', 0)}")
        print(f"📋 Style issues: {summary.get('flake8_issues_found', 0)}")
        print(f"⚠️ Total errors: {summary.get('total_errors', 0)}")
        print(
            f"🚀 Optimization successful: {'Yes' if summary.get('optimization_successful') else 'No'}"
        )
        print(f"⏱️ Duration: {report.get('duration_seconds', 0):.2f} seconds")
        print("=" * 80)

        if summary.get("optimization_successful"):
            print("🎉 Cleanup completed successfully!")
            sys.exit(0)
        else:
            print("⚠️ Cleanup completed with errors. Check the report for details.")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("🛑 Cleanup interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"❌ Cleanup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
