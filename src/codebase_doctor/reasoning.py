from dataclasses import dataclass
from typing import Any

from .models import Issue


@dataclass
class ReasoningResult:
    issue_id: str
    explanation: str
    impact: str
    recommended_action: str


class RuleBasedReasoner:
    """Provide deterministic reasoning for detected issues."""

    def reason(
        self,
        issue: Issue,
    ) -> ReasoningResult:

        impact_map = {
            "critical": (
                "The issue may cause severe "
                "security or reliability consequences."
            ),
            "high": (
                "The issue can materially affect "
                "security, correctness, or maintainability."
            ),
            "medium": (
                "The issue can increase maintenance "
                "cost or technical risk."
            ),
            "low": (
                "The issue has limited immediate impact."
            ),
            "info": (
                "The issue is informational."
            ),
        }

        return ReasoningResult(
            issue_id=issue.id,
            explanation=issue.description,
            impact=impact_map[issue.severity.value],
            recommended_action=(
                issue.suggestion
                or "Review the issue manually."
            ),
        )


class AIReasoner:
    """
    Adapter point for a future LLM reasoning implementation.
    """

    def __init__(
        self,
        client: Any = None,
    ) -> None:
        self.client = client

    def reason(
        self,
        issue: Issue,
    ) -> ReasoningResult:

        if self.client is None:
            return RuleBasedReasoner().reason(issue)

        return RuleBasedReasoner().reason(issue)