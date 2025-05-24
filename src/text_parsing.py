from src.textnode import TextNode, TextType
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
        else:
            if delimiter not in old_node.text:
                new_nodes.append(old_node)
            else:
                parts = old_node.text.split(delimiter, 2)

                # Handle the case where we don't have a closing delimiter
                if len(parts) != 3:
                    raise ValueError(f"Closing delimiter not found for {delimiter}")

                if parts[0]:  # If there's text before the delimiter
                    new_nodes.append(TextNode(parts[0], TextType.NORMAL))

                new_nodes.append(TextNode(parts[1], text_type))

                if parts[2]:  # If there's text after the delimiter
                    new_nodes.append(TextNode(parts[2], TextType.NORMAL))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_generic(
    old_nodes: list[TextNode],
    pattern: str,
    text_type: TextType,
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        while remaining_text:
            match = re.search(pattern, remaining_text)
            if not match:
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
                break

            # Add text before match
            if match.start() > 0:
                new_nodes.append(
                    TextNode(remaining_text[: match.start()], TextType.NORMAL)
                )

            # Add the match
            alt_text, url = match.groups()
            new_nodes.append(TextNode(alt_text, text_type, url))

            remaining_text = remaining_text[match.end() :]

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_generic(
        old_nodes, r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", TextType.IMAGE
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_generic(
        old_nodes, r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", TextType.LINK
    )


def text_to_textnodes(text: str) -> list[TextNode]:
    result: list[TextNode] = [TextNode(text, TextType.NORMAL)]
    delimiter_type_pairs = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    ]

    # First, go through images, since
    # link regex will trigger on images regex
    result = split_nodes_image(result)

    # then links
    result = split_nodes_link(result)

    # we tackle delimeters last in case if
    # there are any of them inside of alt text of an image/link
    for delimiter, text_type in delimiter_type_pairs:
        result = split_nodes_delimiter(result, delimiter, text_type)

    return result
