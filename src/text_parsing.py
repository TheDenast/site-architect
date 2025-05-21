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
