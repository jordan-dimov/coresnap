import typer
import graphviz

from graph_builder import parse_text_outline, outline_to_dot

app = typer.Typer()


@app.command("convert")
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
