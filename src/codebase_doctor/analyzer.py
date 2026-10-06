import ast
from pathlib import Path

from .issues import IssueManager
from .models import AnalysisResult, IssueCategory, Severity
from .parser import ParseInfo


class CodeAnalyzer(ast.NodeVisitor):
    """Analyze Python AST for code-quality problems."""

    def __init__(
        self,
        path: Path,
        manager: IssueManager,
    ) -> None:
        self.path = path
        self.manager = manager

    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ) -> None:
        self._check_function(node)
        self.generic_visit(node)

    def _check_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> None:

        parameter_count = len(node.args.args)

        if parameter_count > 6:
            self.manager.create(
                path=self.path,
                line=node.lineno,
                title="Too many function parameters",
                description=(
                    f"Function '{node.name}' has "
                    f"{parameter_count} parameters."
                ),
                category=IssueCategory.CODE_QUALITY,
                severity=Severity.MEDIUM,
                suggestion=(
                    "Consider grouping related parameters "
                    "into a data object."
                ),
            )

        if len(node.body) > 50:
            self.manager.create(
                path=self.path,
                line=node.lineno,
                title="Large function",
                description=(
                    f"Function '{node.name}' contains "
                    "more than 50 statements."
                ),
                category=IssueCategory.COMPLEXITY,
                severity=Severity.MEDIUM,
                suggestion=(
                    "Split the function into smaller "
                    "cohesive units."
                ),
            )

    def visit_ExceptHandler(
        self,
        node: ast.ExceptHandler,
    ) -> None:

        if node.type is None:
            self.manager.create(
                path=self.path,
                line=node.lineno,
                title="Bare except",
                description=(
                    "A bare except catches every exception."
                ),
                category=IssueCategory.CODE_QUALITY,
                severity=Severity.HIGH,
                suggestion=(
                    "Catch a specific exception type."
                ),
            )

        self.generic_visit(node)


def analyze_project(
    parse_info: ParseInfo,
) -> AnalysisResult:

    manager = IssueManager()

    for result in parse_info.results:

        if not result.parsed or result.tree is None:
            manager.create(
                path=result.path,
                line=None,
                title="Python syntax error",
                description=(
                    result.error
                    or "The file could not be parsed."
                ),
                category=IssueCategory.SYNTAX,
                severity=Severity.HIGH,
                suggestion=(
                    "Fix the syntax error before "
                    "deeper analysis."
                ),
            )
            continue

        analyzer = CodeAnalyzer(
            result.path,
            manager,
        )

        analyzer.visit(result.tree)

    return AnalysisResult(
        issues=manager.issues,
    )