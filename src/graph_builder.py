import re
import mistune

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

    for idx, line in enumerate([l for l in lines if l.strip()]):
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


def parse_markdown_outline(outline: str) -> list[T_NODE]:
    # Takes the input text as a Markdown string and returns a list of nodes containing the title,
    # sanitized title, and the indentation level. The Markdown string is parsed using the mistune
    # library. Only the various levels of headings are used to create the nodes.

    nodes = []

    renderer = mistune.renderers.AstRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    tokens = markdown.parse(outline)
    # Tokens are a list of dictionaries, each representing a token in the Markdown string. They
    # look like this:
    # [
    #   {'type': 'heading', 'children': [{'type': 'text', 'text': 'Focusing on the Present Moment'}], 'level': 3},
    #   {'type': 'heading', 'children': [{'type': 'text', 'text': 'Managing Pressure and Stress'}], 'level': 2},
    #   {'type': 'block_quote', 'children': [{'type': 'paragraph', 'children': [{'type': 'text', 'text': '"Focus your mind on the process of learning and playing, not on the desired result."'}]}]},
    #  ]

    for token in tokens:
        if token["type"] == "heading":
            level = token["level"]
            token_text = token["children"][0]["text"]
            title_clean, title_sanitized = create_node(token_text)
            node = {
                "title": title_clean,
                "title_sanitized": title_sanitized,
                "level": level,
            }
            if level == 1:
                node["penwidth"] = 3
            nodes.append(node)
        elif token["type"] == "block_quote":
            last_node = nodes[-1]
            quote_text = token["children"][0]["children"][0]["text"]
            last_node["quote"] = quote_text

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

        dot_line_props = f'label="{title_clean}", penwidth={penwidth}'
        if "quote" in node:
            quote = node["quote"].replace('"', '\\"')
            dot_line_props += f', tooltip="{quote}"'
        # TODO: Add support for setting the URL property to a suitable link
        dot_line = f"{title_sanitized} [{dot_line_props}];"
        dot_lines.append(dot_line)

        while len(stack) > 0 and stack[-1]["level"] >= indent:
            stack.pop()

        if len(stack) > 0:
            parent = stack[-1]
            dot_lines.append(f'{parent["title_sanitized"]} -> {title_sanitized}')

        stack.append(node)

    dot_lines.append("}")
    return "\n".join(dot_lines)
