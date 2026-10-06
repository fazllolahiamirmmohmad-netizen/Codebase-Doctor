from dataclasses import dataclass
from pathlib import Path
import ast

from .scanner import ProjectInfo


@dataclass
class ParseResult:
    """Store the AST parsing result of a single Python file."""

    path: Path
    tree: ast.AST | None
    parsed: bool
    error: str | None = None


@dataclass
class ParseInfo:
    """Store all parsing results of a project."""

    results: list[ParseResult]

    @property
    def successful_files(self) -> list[Path]:
        """Return successfully parsed files."""

        return [
            result.path
            for result in self.results
            if result.parsed
        ]

    @property
    def failed_files(self) -> list[Path]:
        """Return files that failed to parse."""

        return [
            result.path
            for result in self.results
            if not result.parsed
        ]

    @property
    def successful_count(self) -> int:
        """Return the number of successfully parsed files."""

        return len(self.successful_files)

    @property
    def failed_count(self) -> int:
        """Return the number of files that failed to parse."""

        return len(self.failed_files)


def parse_file(
    file_path: Path,
    encoding: str = "utf-8",
) -> ParseResult:
    """Parse one Python file into an Abstract Syntax Tree."""

    try:
        source = file_path.read_text(encoding=encoding)

        tree = ast.parse(
            source,
            filename=str(file_path),
        )

        return ParseResult(
            path=file_path,
            tree=tree,
            parsed=True,
        )

    except (SyntaxError, UnicodeDecodeError, OSError) as error:
        return ParseResult(
            path=file_path,
            tree=None,
            parsed=False,
            error=str(error),
        )


def parse_project(project: ProjectInfo) -> ParseInfo:
    """Parse all Python files discovered by the scanner."""

    results: list[ParseResult] = []

    for file_info in project.files:
        if not file_info.is_python:
            continue

        if not file_info.readable:
            results.append(
                ParseResult(
                    path=file_info.path,
                    tree=None,
                    parsed=False,
                    error="File is not readable.",
                )
            )
            continue

        encoding = file_info.encoding or "utf-8"

        result = parse_file(
            file_path=file_info.path,
            encoding=encoding,
        )

        results.append(result)

    return ParseInfo(results=results)


def display_parse_info(parse_info: ParseInfo) -> None:
    """Display parsing results."""

    print("\n========== PARSE RESULTS ==========")

    print(f"Python files: {len(parse_info.results)}")
    print(f"Successfully parsed: {parse_info.successful_count}")
    print(f"Failed to parse: {parse_info.failed_count}")

    if parse_info.failed_files:
        print("\n========== PARSE ERRORS ==========")

        for result in parse_info.results:
            if not result.parsed:
                print(f"\nFile: {result.path}")
                print(f"Error: {result.error}")


def main() -> None:
    """Run the Codebase Doctor parser."""

    from .scanner import get_project_path, scan_project

    project_path = get_project_path()
    project_info = scan_project(project_path)

    parse_info = parse_project(project_info)

    display_parse_info(parse_info)


if __name__ == "__main__":
    main()