import typer
import graphviz

from gptutils import gpt_outline
from graph_builder import (
    parse_text_outline,
    outline_to_dot,
    sanitize_title,
    parse_markdown_outline,
)

app = typer.Typer()


@app.command("outline")
def outline(
    work_title: str, outline_file: str | None = None, outline_format: str = "txt"
):
    if outline_format not in ["txt", "markdown"]:
        raise NotImplementedError(
            f"Outline format '{outline_format}' not supported yet."
        )
    clean_title = sanitize_title(work_title)
    outline_file = outline_file or f"{clean_title}.txt"
    outline = gpt_outline(work_title, version=outline_format)
    with open(outline_file, "w") as f:
        f.write(outline)
    typer.echo(f"Outline saved as '{outline_file}'.")


@app.command("convert")
def notes_to_tree(
    input_file: str, output_file: str = "output.dot", outline_format: str = "txt"
):
    with open(input_file, "r") as f:
        outline = f.read()

    if outline_format == "txt":
        nodes = parse_text_outline(outline)
    elif outline_format == "markdown":
        nodes = parse_markdown_outline(outline)
    dot_content = outline_to_dot(nodes)

    input_stem = input_file.rpartition(".")[0]

    with open(output_file, "w") as f:
        f.write(dot_content)

    typer.echo(f"DOT file saved as '{output_file}'. Use this to render: ")
    typer.echo(f"coresnap.py render {output_file} {input_stem}.png --output-format=png")


@app.command("render")
def render(dot_file: str, output_file: str, output_format: str = "png"):
    with open(dot_file, "r") as f:
        dot_content = f.read()

    graph = graphviz.Source(dot_content)
    graph.format = output_format.lower()
    graph.render(output_file.rpartition(".")[0], cleanup=True)

    typer.echo(f"Image rendered as '{output_file}'.")


if __name__ == "__main__":
    app()
