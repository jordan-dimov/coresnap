import re
import typer


def sanitize_title(title):
    title_sanitized = re.sub(r'[^\w\s]', '_', title).replace(' ', '_')
    return title_sanitized

def create_node(title):
    title_clean = title.lstrip().lstrip('-').strip()
    title_sanitized = sanitize_title(title_clean)
    return (title_clean, title_sanitized)

def outline_to_dot(outline):
    lines = outline.strip().split('\n')
    dot_lines = ['digraph G {', 'rankdir=TB;', 'node [shape=box];', 'splines=ortho;']

    stack = []
    for line in lines:
        indent = len(re.match(r'\s*', line).group(0))
        title_clean, title_sanitized = create_node(line)

        dot_lines.append(f'{title_sanitized} [label="{title_clean}"];')

        while len(stack) > 0 and stack[-1]["level"] >= indent:
            stack.pop()

        if len(stack) > 0:
            parent = stack[-1]
            dot_lines.append(f'{parent["title_sanitized"]} -> {title_sanitized}')

        stack.append({"title": title_clean, "title_sanitized": title_sanitized, "level": indent})

    dot_lines.append('}')
    return '\n'.join(dot_lines)


def outline_to_dot2(outline):
    lines = outline.strip().split('\n')
    dot_lines = ['digraph G {', 'rankdir=LR;', 'node [shape=box];', 'splines=ortho;', 'ranksep=1.0;', 'nodesep=0.4;']

    stack = []
    for line in lines:
        indent = len(re.match(r'\s*', line).group(0))
        title_clean, title_sanitized = create_node(line)

        dot_lines.append(f'{title_sanitized} [label="{title_clean}"];')

        while len(stack) > 0 and stack[-1]["level"] >= indent:
            stack.pop()

        if len(stack) > 0:
            parent = stack[-1]
            dot_lines.append(f'{parent["title_sanitized"]} -> {title_sanitized}')

        stack.append({"title": title_clean, "title_sanitized": title_sanitized, "level": indent})

    dot_lines.append('}')
    return '\n'.join(dot_lines)


def main(input_file: str, output_file: str = "output.dot"):
    with open(input_file, "r") as f:
        outline = f.read()

    dot_content = outline_to_dot2(outline)

    input_stem = input_file.rpartition('.')[0]

    with open(output_file, "w") as f:
        f.write(dot_content)

    typer.echo(f"DOT file saved as '{output_file}'. Use this to render: ")
    typer.echo(f"dot -Tpng {output_file} -o {input_stem}.png")


if __name__ == "__main__":
    typer.run(main)
