import re

T_NODE = dict[str, str | int]


def sanitize_title(title: str) -> str:
    # Replace all non-alphanumeric characters with underscores, so title can be used as a node ID
    title_sanitized = re.sub(r"[^\w\s]", "_", title).replace(" ", "_")
    return title_sanitized


def create_node(title: str) -> (str, str):
    title_clean = title.lstrip().lstrip("-").strip()
    title_sanitized = sanitize_title(title_clean)
    return title_clean, title_sanitized


def parse_text_outline(outline: str) -> list[T_NODE]:
    # Takes the input text as indented bullet list and returns a list of nodes containing the title,
    # sanitized title, and the indentation level.
    # TODO: Add parsers for other formats

    lines = outline.strip().split("\n")
    nodes = []

    for idx, line in enumerate(lines):
        indent = len(re.match(r"\s*", line).group(0))
        title_clean, title_sanitized = create_node(line)
        node = {
            "title": title_clean,
            "title_sanitized": title_sanitized,
            "level": indent,
        }
        if idx == 0:  # Root node
            node["penwidth"] = 3
        nodes.append(node)

    return nodes


def outline_to_dot(nodes: list[T_NODE]) -> str:
    dot_lines = [
        "digraph G {",
        "rankdir=LR;",
        "node [shape=box];",
        "splines=ortho;",
        "ranksep=1.0;",
        "nodesep=0.4;",
    ]

    stack = []
    for node in nodes:
        title_clean, title_sanitized = node["title"], node["title_sanitized"]
        penwidth = node.get("penwidth", 1)

        indent = node["level"]

        dot_lines.append(
            f'{title_sanitized} [label="{title_clean}", penwidth={penwidth}];'
        )

        while len(stack) > 0 and stack[-1]["level"] >= indent:
            stack.pop()

        if len(stack) > 0:
            parent = stack[-1]
            dot_lines.append(f'{parent["title_sanitized"]} -> {title_sanitized}')

        stack.append(node)

    dot_lines.append("}")
    return "\n".join(dot_lines)
