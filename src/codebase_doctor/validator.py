from pathlib import Path
import subprocess

from .models import ValidationResult


class Validator:
    """Run validation commands against a project."""

    def run(
        self,
        project_path: Path,
        command: list[str],
        *,
        timeout: int = 120,
    ) -> ValidationResult:

        try:
            completed = subprocess.run(
                command,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )

            return ValidationResult(
                success=completed.returncode == 0,
                command=command,
                return_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )

        except (
            OSError,
            subprocess.TimeoutExpired,
        ) as error:

            return ValidationResult(
                success=False,
                command=command,
                return_code=-1,
                stderr=str(error),
            )

    def run_pytest(
        self,
        project_path: Path,
    ) -> ValidationResult:

        return self.run(
            project_path,
            ["python", "-m", "pytest"],
        )

    def run_compile_check(
        self,
        project_path: Path,
    ) -> ValidationResult:

        return self.run(
            project_path,
            [
                "python",
                "-m",
                "compileall",
                "-q",
                ".",
            ],
        )