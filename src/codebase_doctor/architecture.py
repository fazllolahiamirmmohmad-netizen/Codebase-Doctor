import ast
from collections import defaultdict

from .parser import ParseInfo


def build_architecture_map(
    parse_info: ParseInfo,
) -> dict[str, list[str]]:

    graph: dict[str, list[str]] = defaultdict(list)

    for result in parse_info.results:

        if not result.parsed or result.tree is None:
            continue

        module = str(result.path)

        for node in ast.walk(result.tree):

            if isinstance(node, ast.Import):

                graph[module].extend(
                    alias.name
                    for alias in node.names
                )

            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    graph[module].append(
                        node.module
                    )

    return {
        module: sorted(set(imports))
        for module, imports in graph.items()
    }


def find_high_fanout_modules(
    architecture: dict[str, list[str]],
    threshold: int = 10,
) -> dict[str, int]:

    counts: dict[str, int] = defaultdict(int)

    for imports in architecture.values():

        for module in imports:
            counts[module] += 1

    return {
        module: count
        for module, count in counts.items()
        if count >= threshold
    }