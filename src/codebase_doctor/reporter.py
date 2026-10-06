from dataclasses import asdict
from pathlib import Path
import json

from .models import AnalysisResult


class ReportEngine:
    """Generate human-readable and machine-readable reports."""

    def text(
        self,
        analysis: AnalysisResult,
    ) -> str:

        lines = [
            "========== CODEBASE DOCTOR REPORT =========="
        ]

        if not analysis.issues:
            lines.append("No issues detected.")
            return "\n".join(lines)

        for issue in analysis.issues:

            lines.extend(
                [
                    "",
                    f"[{issue.id}] "
                    f"{issue.severity.value.upper()}",
                    f"File: {issue.path}",
                    f"Line: {issue.line}",
                    f"Category: "
                    f"{issue.category.value}",
                    f"Title: {issue.title}",
                    f"Description: "
                    f"{issue.description}",
                    f"Suggestion: "
                    f"{issue.suggestion}",
                ]
            )

        return "\n".join(lines)

    def json(
        self,
        analysis: AnalysisResult,
    ) -> str:

        payload = [
            asdict(issue)
            for issue in analysis.issues
        ]

        for item in payload:
            item["path"] = str(item["path"])
            item["category"] = item[
                "category"
            ].value
            item["severity"] = item[
                "severity"
            ].value

        return json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        )

    def save_text(
        self,
        analysis: AnalysisResult,
        path: Path,
    ) -> None:

        path.write_text(
            self.text(analysis),
            encoding="utf-8",
        )

    def save_json(
        self,
        analysis: AnalysisResult,
        path: Path,
    ) -> None:

        path.write_text(
            self.json(analysis),
            encoding="utf-8",
        )