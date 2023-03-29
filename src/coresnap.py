import re
import typer
import graphviz


def sanitize_title(title: str) -> str:
    # Replace all non-alphanumeric characters with underscores, so title can be used as a node ID
    title_sanitized = re.sub(r"[^\w\s]", "_", title).replace(" ", "_")
    return title_sanitized


def create_node(title: str) -> (str, str):
    title_clean = title.lstrip().lstrip("-").strip()
    title_sanitized = sanitize_title(title_clean)
    return title_clean, title_sanitized


T_NODE = dict[str, str | int]


def parse_text_outline(outline: str) -> list[T_NODE]:
    # Takes the input text as indented bullet list and returns a list of nodes containing the title,
    # sanitized title, and the indentation level.
    # TODO: Add parsers for other formats

    lines = outline.strip().split("\n")
    nodes = []

    for line in lines:
        indent = len(re.match(r"\s*", line).group(0))
        title_clean, title_sanitized = create_node(line)
        nodes.append(
            {"title": title_clean, "title_sanitized": title_sanitized, "level": indent}
        )

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
        indent = node["level"]

        dot_lines.append(f'{title_sanitized} [label="{title_clean}"];')

        while len(stack) > 0 and stack[-1]["level"] >= indent:
            stack.pop()

        if len(stack) > 0:
            parent = stack[-1]
            dot_lines.append(f'{parent["title_sanitized"]} -> {title_sanitized}')

        stack.append(node)

    dot_lines.append("}")
    return "\n".join(dot_lines)


def render(dot_file: str, output_file: str, output_format: str = "png"):
    with open(dot_file, "r") as f:
        dot_content = f.read()

    graph = graphviz.Source(dot_content)
    graph.format = output_format.lower()
    graph.render(output_file.rpartition(".")[0], cleanup=True)

    typer.echo(f"Image rendered as '{output_file}'.")


def notes_to_tree(input_file: str, output_file: str = "output.dot"):
    with open(input_file, "r") as f:
        outline = f.read()

    nodes = parse_text_outline(outline)
    dot_content = outline_to_dot(nodes)

    input_stem = input_file.rpartition(".")[0]

    with open(output_file, "w") as f:
        f.write(dot_content)

    typer.echo(f"DOT file saved as '{output_file}'. Use this to render: ")
    typer.echo(f"coresnap.py render {output_file} {input_stem}.png --output-format=png")


if __name__ == "__main__":
    app = typer.Typer()
    app.command("convert")(notes_to_tree)
    app.command("render")(render)
    app()
