"""
Code quality and formatting utilities for Device Farm v5
"""

import ast
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger


class CodeFormatter:
    """Advanced code formatting and quality checks"""

    def __init__(self):
        self.python_files_pattern = "**/*.py"
        self.ignore_patterns = [
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "node_modules",
            ".pytest_cache",
        ]

    def find_python_files(self, root_dir: str) -> List[Path]:
        """Find all Python files in directory"""
        root_path = Path(root_dir)
        python_files = []

        for file_path in root_path.rglob(self.python_files_pattern):
            # Skip ignored patterns
            if any(pattern in str(file_path) for pattern in self.ignore_patterns):
                continue

            python_files.append(file_path)

        return python_files

    def check_syntax(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """Check Python file syntax"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            ast.parse(source)
            return True, None

        except SyntaxError as e:
            return False, f"Syntax error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"Error reading file: {e}"

    def analyze_imports(self, file_path: Path) -> Dict[str, Any]:
        """Analyze import statements"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)
            imports = {
                "standard_library": [],
                "third_party": [],
                "local": [],
                "unused": [],
                "duplicate": [],
            }

            import_lines = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_lines.append((node.lineno, alias.name))
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        import_name = f"{module}.{alias.name}" if module else alias.name
                        import_lines.append((node.lineno, import_name))

            # Categorize imports (simplified)
            for line_no, import_name in import_lines:
                if import_name.startswith(".") or "src." in import_name:
                    imports["local"].append((line_no, import_name))
                elif any(
                    stdlib in import_name
                    for stdlib in ["os", "sys", "json", "time", "datetime", "asyncio", "threading"]
                ):
                    imports["standard_library"].append((line_no, import_name))
                else:
                    imports["third_party"].append((line_no, import_name))

            return imports

        except Exception as e:
            logger.error(f"Error analyzing imports in {file_path}: {e}")
            return {}

    def check_code_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Analyze code complexity"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            functions = []
            classes = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    complexity = self._calculate_cyclomatic_complexity(node)
                    functions.append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "complexity": complexity,
                            "args_count": len(node.args.args),
                            "lines_count": self._count_function_lines(node),
                        }
                    )
                elif isinstance(node, ast.ClassDef):
                    method_count = sum(
                        1 for child in node.body if isinstance(child, ast.FunctionDef)
                    )
                    classes.append(
                        {
                            "name": node.name,
                            "line": node.lineno,
                            "method_count": method_count,
                            "lines_count": self._count_class_lines(node),
                        }
                    )

            return {
                "functions": functions,
                "classes": classes,
                "total_lines": len(source.splitlines()),
                "avg_function_complexity": sum(f["complexity"] for f in functions)
                / max(len(functions), 1),
            }

        except Exception as e:
            logger.error(f"Error analyzing complexity in {file_path}: {e}")
            return {}

    def _calculate_cyclomatic_complexity(self, node) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, ast.With, ast.AsyncWith):
                complexity += 1

        return complexity

    def _count_function_lines(self, node) -> int:
        """Count lines in a function"""
        # Simplified line count
        return len(ast.dump(node).splitlines())

    def _count_class_lines(self, node) -> int:
        """Count lines in a class"""
        # Simplified line count
        return len(ast.dump(node).splitlines())

    def check_docstrings(self, file_path: Path) -> Dict[str, Any]:
        """Check for missing docstrings"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()

            tree = ast.parse(source)

            missing_docstrings = {"functions": [], "classes": [], "modules": []}

            # Check module docstring
            if not (
                tree.body
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
            ):
                missing_docstrings["modules"].append(str(file_path))

            # Check functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not self._has_docstring(node):
                        missing_docstrings["functions"].append(
                            {"name": node.name, "line": node.lineno}
                        )
                elif isinstance(node, ast.ClassDef):
                    if not self._has_docstring(node):
                        missing_docstrings["classes"].append(
                            {"name": node.name, "line": node.lineno}
                        )

            return missing_docstrings

        except Exception as e:
            logger.error(f"Error checking docstrings in {file_path}: {e}")
            return {}

    def _has_docstring(self, node) -> bool:
        """Check if node has docstring"""
        return (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        )

    def format_with_black(self, file_path: Path) -> bool:
        """Format file with Black"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "black",
                    "--line-length",
                    "100",
                    "--target-version",
                    "py39",
                    str(file_path),
                ],
                capture_output=True,
                text=True,
            )

            return result.returncode == 0

        except Exception as e:
            logger.error(f"Error formatting with Black: {e}")
            return False

    def check_with_flake8(self, file_path: Path) -> List[str]:
        """Check file with flake8"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "flake8",
                    "--max-line-length",
                    "100",
                    "--ignore",
                    "E203,W503",
                    str(file_path),
                ],
                capture_output=True,
                text=True,
            )

            if result.stdout:
                return result.stdout.strip().split("\n")
            return []

        except Exception as e:
            logger.error(f"Error running flake8: {e}")
            return [f"Error running flake8: {e}"]

    def optimize_imports(self, file_path: Path) -> bool:
        """Optimize imports with isort"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "isort",
                    "--profile",
                    "black",
                    "--line-length",
                    "100",
                    str(file_path),
                ],
                capture_output=True,
                text=True,
            )

            return result.returncode == 0

        except Exception as e:
            logger.error(f"Error optimizing imports: {e}")
            return False

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Complete file analysis"""
        logger.info(f"🔍 Analyzing {file_path}")

        analysis = {
            "file_path": str(file_path),
            "syntax_valid": True,
            "syntax_error": None,
            "imports": {},
            "complexity": {},
            "docstrings": {},
            "flake8_issues": [],
        }

        # Syntax check
        syntax_valid, syntax_error = self.check_syntax(file_path)
        analysis["syntax_valid"] = syntax_valid
        analysis["syntax_error"] = syntax_error

        if not syntax_valid:
            return analysis

        # Import analysis
        analysis["imports"] = self.analyze_imports(file_path)

        # Complexity analysis
        analysis["complexity"] = self.check_code_complexity(file_path)

        # Docstring check
        analysis["docstrings"] = self.check_docstrings(file_path)

        # Flake8 check
        analysis["flake8_issues"] = self.check_with_flake8(file_path)

        return analysis

    def format_file(self, file_path: Path) -> bool:
        """Format a single file"""
        logger.info(f"🎨 Formatting {file_path}")

        success = True

        # Optimize imports
        if not self.optimize_imports(file_path):
            logger.warning(f"⚠️ Failed to optimize imports in {file_path}")
            success = False

        # Format with Black
        if not self.format_with_black(file_path):
            logger.warning(f"⚠️ Failed to format with Black: {file_path}")
            success = False

        return success

    def analyze_directory(self, directory: str) -> Dict[str, Any]:
        """Analyze all Python files in directory"""
        logger.info(f"🔍 Analyzing directory: {directory}")

        files = self.find_python_files(directory)
        results = {
            "total_files": len(files),
            "files_analyzed": 0,
            "syntax_errors": [],
            "complexity_issues": [],
            "import_issues": [],
            "docstring_issues": [],
            "flake8_issues": [],
        }

        for file_path in files:
            try:
                analysis = self.analyze_file(file_path)
                results["files_analyzed"] += 1

                # Collect issues
                if not analysis["syntax_valid"]:
                    results["syntax_errors"].append(
                        {"file": str(file_path), "error": analysis["syntax_error"]}
                    )

                # Complexity issues
                complexity = analysis.get("complexity", {})
                for func in complexity.get("functions", []):
                    if func["complexity"] > 10:  # High complexity threshold
                        results["complexity_issues"].append(
                            {
                                "file": str(file_path),
                                "function": func["name"],
                                "complexity": func["complexity"],
                                "line": func["line"],
                            }
                        )

                # Flake8 issues
                if analysis.get("flake8_issues"):
                    results["flake8_issues"].extend(
                        [
                            {"file": str(file_path), "issue": issue}
                            for issue in analysis["flake8_issues"]
                        ]
                    )

            except Exception as e:
                logger.error(f"Error analyzing {file_path}: {e}")

        return results

    def format_directory(self, directory: str) -> Dict[str, Any]:
        """Format all Python files in directory"""
        logger.info(f"🎨 Formatting directory: {directory}")

        files = self.find_python_files(directory)
        results = {"total_files": len(files), "files_formatted": 0, "formatting_errors": []}

        for file_path in files:
            try:
                if self.format_file(file_path):
                    results["files_formatted"] += 1
                else:
                    results["formatting_errors"].append(str(file_path))

            except Exception as e:
                logger.error(f"Error formatting {file_path}: {e}")
                results["formatting_errors"].append(str(file_path))

        return results


def format_codebase(directory: str = ".") -> Dict[str, Any]:
    """Format entire codebase"""
    formatter = CodeFormatter()
    return formatter.format_directory(directory)


def analyze_codebase(directory: str = ".") -> Dict[str, Any]:
    """Analyze entire codebase"""
    formatter = CodeFormatter()
    return formatter.analyze_directory(directory)
