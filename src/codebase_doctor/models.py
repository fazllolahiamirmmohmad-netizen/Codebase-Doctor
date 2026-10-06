from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IssueCategory(str, Enum):
    CODE_QUALITY = "code_quality"
    COMPLEXITY = "complexity"
    SECURITY = "security"
    DEPENDENCY = "dependency"
    ARCHITECTURE = "architecture"
    SYNTAX = "syntax"
    TEST = "test"


@dataclass
class Issue:
    id: str
    path: Path
    line: int | None
    title: str
    description: str
    category: IssueCategory
    severity: Severity
    suggestion: str = ""
    evidence: str = ""
    fixable: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DependencyInfo:
    path: Path
    imports: list[str] = field(default_factory=list)
    local_modules: list[str] = field(default_factory=list)
    external_modules: list[str] = field(default_factory=list)
    unresolved_imports: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    success: bool
    command: list[str]
    return_code: int
    stdout: str = ""
    stderr: str = ""


@dataclass
class RepairPlan:
    issue_id: str
    path: Path
    description: str
    changes: list[str] = field(default_factory=list)
    replacement: str | None = None
    approved: bool = False


@dataclass
class AnalysisResult:
    issues: list[Issue] = field(default_factory=list)

    def add(self, issue: Issue) -> None:
        self.issues.append(issue)