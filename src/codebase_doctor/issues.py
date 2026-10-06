from dataclasses import dataclass, field
from itertools import count

from .models import Issue, IssueCategory, Severity


@dataclass
class IssueManager:
    issues: list[Issue] = field(default_factory=list)
    _counter: count = field(
        default_factory=lambda: count(1),
        init=False,
        repr=False,
    )

    def create(
        self,
        *,
        path,
        line,
        title,
        description,
        category: IssueCategory,
        severity: Severity,
        suggestion="",
        evidence="",
        fixable=False,
        metadata=None,
    ) -> Issue:
        issue = Issue(
            id=f"ISSUE-{next(self._counter):04d}",
            path=path,
            line=line,
            title=title,
            description=description,
            category=category,
            severity=severity,
            suggestion=suggestion,
            evidence=evidence,
            fixable=fixable,
            metadata=metadata or {},
        )

        self.issues.append(issue)
        return issue

    def by_severity(self, severity: Severity) -> list[Issue]:
        return [
            issue
            for issue in self.issues
            if issue.severity == severity
        ]

    def by_category(
        self,
        category: IssueCategory,
    ) -> list[Issue]:
        return [
            issue
            for issue in self.issues
            if issue.category == category
        ]