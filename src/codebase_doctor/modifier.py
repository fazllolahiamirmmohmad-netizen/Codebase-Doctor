from dataclasses import dataclass
from pathlib import Path
import difflib


@dataclass
class Modification:
    path: Path
    original: str
    updated: str

    @property
    def changed(self) -> bool:
        return self.original != self.updated


class CodeModifier:
    """Modify source code only after explicit approval."""

    def preview(
        self,
        path: Path,
        updated: str,
        encoding: str = "utf-8",
    ) -> str:

        original = path.read_text(
            encoding=encoding
        )

        return "".join(
            difflib.unified_diff(
                original.splitlines(
                    keepends=True
                ),
                updated.splitlines(
                    keepends=True
                ),
                fromfile=str(path),
                tofile=str(path),
            )
        )

    def modify(
        self,
        path: Path,
        updated: str,
        *,
        approved: bool,
        encoding: str = "utf-8",
    ) -> Modification:

        if not approved:
            raise PermissionError(
                "Code modification requires "
                "explicit approval."
            )

        original = path.read_text(
            encoding=encoding
        )

        path.write_text(
            updated,
            encoding=encoding,
        )

        return Modification(
            path=path,
            original=original,
            updated=updated,
        )