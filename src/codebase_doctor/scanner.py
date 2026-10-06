
from dataclasses import dataclass, field
from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
}

PYTHON_EXTENSIONS = {".py", ".pyw"}

TEST_DIRECTORY_NAMES = {
    "test",
    "tests",
}

CONFIG_FILES = {
    ".env",
    ".env.example",
    "config.py",
    "settings.py",
    "settings.yaml",
    "settings.yml",
    "settings.json",
    "config.yaml",
    "config.yml",
    "config.json",
}

DEPENDENCY_FILES = {
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "Pipfile",
    "Pipfile.lock",
    "poetry.lock",
    "uv.lock",
    "setup.py",
    "setup.cfg",
}


@dataclass
class FileInfo:
    """Store information about a single file."""

    path: Path
    relative_path: Path
    name: str
    suffix: str
    size: int
    is_python: bool = False
    is_test: bool = False
    is_config: bool = False
    is_dependency_file: bool = False
    readable: bool = False
    encoding: str | None = None


@dataclass
class ProjectInfo:
    """Store the complete inventory of a scanned project."""

    project_path: Path

    files: list[FileInfo] = field(default_factory=list)
    directories: list[Path] = field(default_factory=list)

    python_files: list[Path] = field(default_factory=list)
    test_files: list[Path] = field(default_factory=list)
    config_files: list[Path] = field(default_factory=list)
    dependency_files: list[Path] = field(default_factory=list)

    readable_files: list[Path] = field(default_factory=list)
    unreadable_files: list[Path] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    @property
    def file_count(self) -> int:
        return len(self.files)

    @property
    def directory_count(self) -> int:
        return len(self.directories)

    @property
    def python_file_count(self) -> int:
        return len(self.python_files)

    @property
    def test_file_count(self) -> int:
        return len(self.test_files)


def get_project_path() -> Path:
    """Get a valid project directory from the user."""

    while True:
        raw_path = input("Enter project path: ").strip()

        if not raw_path:
            print("Error: Project path cannot be empty.")
            continue

        project_path = Path(raw_path).expanduser()

        if not project_path.exists():
            print("Error: Project path does not exist.")
            continue

        if not project_path.is_dir():
            print("Error: The path is not a directory.")
            continue

        return project_path.resolve()


def should_ignore(path: Path) -> bool:
    """Return True when a path belongs to an ignored directory."""

    return any(part in IGNORED_DIRECTORIES for part in path.parts)


def is_python_file(path: Path) -> bool:
    """Return True when the file is a Python source file."""

    return path.suffix.lower() in PYTHON_EXTENSIONS


def is_test_file(path: Path) -> bool:
    """Return True when the file appears to be a test file."""

    return (
        path.name.startswith("test_")
        or path.name.endswith("_test.py")
        or any(
            part.lower() in TEST_DIRECTORY_NAMES
            for part in path.parts
        )
    )


def is_config_file(path: Path) -> bool:
    """Return True when the file is a known configuration file."""

    return path.name in CONFIG_FILES


def is_dependency_file(path: Path) -> bool:
    """Return True when the file contains project dependencies."""

    return path.name in DEPENDENCY_FILES


def detect_encoding(path: Path) -> str | None:
    """Try to determine whether a file can be decoded as UTF-8."""

    try:
        path.read_text(encoding="utf-8")
        return "utf-8"

    except UnicodeDecodeError:
        return None

    except OSError:
        return None


def build_file_info(
    project_path: Path,
    file_path: Path,
) -> FileInfo:
    """Build metadata for a single file."""

    relative_path = file_path.relative_to(project_path)
    encoding = detect_encoding(file_path)

    return FileInfo(
        path=file_path,
        relative_path=relative_path,
        name=file_path.name,
        suffix=file_path.suffix.lower(),
        size=file_path.stat().st_size,
        is_python=is_python_file(file_path),
        is_test=is_test_file(file_path),
        is_config=is_config_file(file_path),
        is_dependency_file=is_dependency_file(file_path),
        readable=encoding is not None,
        encoding=encoding,
    )


def scan_project(project_path: Path) -> ProjectInfo:
    """Scan the complete project filesystem."""

    project_info = ProjectInfo(project_path=project_path)

    try:
        for current_path in project_path.rglob("*"):
            if should_ignore(current_path):
                continue

            try:
                if current_path.is_dir():
                    project_info.directories.append(current_path)
                    continue

                if not current_path.is_file():
                    continue

                file_info = build_file_info(
                    project_path,
                    current_path,
                )

                project_info.files.append(file_info)

                if file_info.is_python:
                    project_info.python_files.append(file_info.path)

                if file_info.is_test:
                    project_info.test_files.append(file_info.path)

                if file_info.is_config:
                    project_info.config_files.append(file_info.path)

                if file_info.is_dependency_file:
                    project_info.dependency_files.append(file_info.path)

                if file_info.readable:
                    project_info.readable_files.append(file_info.path)
                else:
                    project_info.unreadable_files.append(file_info.path)

            except (OSError, ValueError) as error:
                project_info.errors.append(
                    f"{current_path}: {error}"
                )

    except OSError as error:
        project_info.errors.append(
            f"Project scan failed: {error}"
        )

    return project_info


def display_project_info(project: ProjectInfo) -> None:
    """Display the scanner results."""

    print("\n========== PROJECT INFORMATION ==========")
    print(f"Project: {project.project_path}")

    print("\n========== COUNTS ==========")
    print(f"Files: {project.file_count}")
    print(f"Directories: {project.directory_count}")
    print(f"Python files: {project.python_file_count}")
    print(f"Test files: {project.test_file_count}")
    print(f"Config files: {len(project.config_files)}")
    print(f"Dependency files: {len(project.dependency_files)}")
    print(f"Readable files: {len(project.readable_files)}")
    print(f"Unreadable files: {len(project.unreadable_files)}")

    print("\n========== PYTHON FILES ==========")
    for path in project.python_files:
        print(path)

    print("\n========== TEST FILES ==========")
    for path in project.test_files:
        print(path)

    print("\n========== CONFIG FILES ==========")
    for path in project.config_files:
        print(path)

    print("\n========== DEPENDENCY FILES ==========")
    for path in project.dependency_files:
        print(path)

    if project.errors:
        print("\n========== SCAN ERRORS ==========")

        for error in project.errors:
            print(error)


def main() -> None:
    """Run Codebase Doctor Scanner."""

    project_path = get_project_path()
    project_info = scan_project(project_path)

    display_project_info(project_info)


if __name__ == "__main__":
    main()
