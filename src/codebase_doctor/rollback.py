from pathlib import Path
import shutil
import tempfile


class RollbackManager:
    """Backup modified files and restore them when validation fails."""

    def __init__(self) -> None:
        self._backup_dir = Path(
            tempfile.mkdtemp(
                prefix="codebase_doctor_"
            )
        )

        self._backups: dict[Path, Path] = {}

    def backup(
        self,
        path: Path,
    ) -> Path:

        backup_path = (
            self._backup_dir
            / f"{len(self._backups):06d}_{path.name}"
        )

        shutil.copy2(
            path,
            backup_path,
        )

        self._backups[path] = backup_path

        return backup_path

    def restore(
        self,
        path: Path,
    ) -> None:

        backup = self._backups.get(path)

        if backup is None:
            raise FileNotFoundError(
                f"No backup exists for {path}."
            )

        shutil.copy2(
            backup,
            path,
        )

    def clear(self) -> None:

        shutil.rmtree(
            self._backup_dir,
            ignore_errors=True,
        )

        self._backups.clear()