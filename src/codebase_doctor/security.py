import ast
from pathlib import Path

from .issues import IssueManager
from .models import AnalysisResult, IssueCategory, Severity
from .parser import ParseInfo


DANGEROUS_CALLS = {
    "eval": (
        "Dynamic code execution via eval().",
        Severity.CRITICAL,
    ),
    "exec": (
        "Dynamic code execution via exec().",
        Severity.CRITICAL,
    ),
    "compile": (
        "Dynamic compilation can be dangerous.",
        Severity.HIGH,
    ),
}


class SecurityVisitor(ast.NodeVisitor):

    def __init__(
        self,
        path: Path,
        manager: IssueManager,
    ) -> None:
        self.path = path
        self.manager = manager

    def visit_Call(
        self,
        node: ast.Call,
    ) -> None:

        if (
            isinstance(node.func, ast.Name)
            and node.func.id in DANGEROUS_CALLS
        ):
            description, severity = DANGEROUS_CALLS[
                node.func.id
            ]

            self.manager.create(
                path=self.path,
                line=node.lineno,
                title=(
                    f"Dangerous call: "
                    f"{node.func.id}()"
                ),
                description=description,
                category=IssueCategory.SECURITY,
                severity=severity,
                suggestion=(
                    "Replace dynamic execution with "
                    "a safe alternative."
                ),
            )

        self.generic_visit(node)


def analyze_security(
    parse_info: ParseInfo,
) -> AnalysisResult:

    manager = IssueManager()

    for result in parse_info.results:

        if (
            result.parsed
            and result.tree is not None
        ):
            SecurityVisitor(
                result.path,
                manager,
            ).visit(result.tree)

    return AnalysisResult(
        issues=manager.issues,
    )