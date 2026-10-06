import ast

from .models import DependencyInfo
from .parser import ParseInfo


def analyze_dependencies(
    parse_info: ParseInfo,
) -> list[DependencyInfo]:

    results: list[DependencyInfo] = []

    for result in parse_info.results:

        if not result.parsed or result.tree is None:
            continue

        imports: list[str] = []

        for node in ast.walk(result.tree):

            if isinstance(node, ast.Import):
                imports.extend(
                    alias.name
                    for alias in node.names
                )

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        results.append(
            DependencyInfo(
                path=result.path,
                imports=sorted(set(imports)),
                external_modules=sorted(set(imports)),
            )
        )

    return results