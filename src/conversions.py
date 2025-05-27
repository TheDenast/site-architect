from src.text_parsing import text_to_textnodes
from src.textnode import TextNode, TextType
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.md import BlockType, markdown_to_blocks, block_to_blocktype


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            assert text_node.url is not None
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            assert text_node.url is not None and text_node.text is not None
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text)
    leaves: list[HTMLNode] = []
    for text_node in text_nodes:
        leaf = text_node_to_html_node(text_node)
        leaves.append(leaf)
    return leaves


def strip_unordered_list_symbols(block: str) -> list[str]:
    lines = block.split("\n")
    return [line[2:] for line in lines]  # Remove "- "


def strip_ordered_list_symbols(block: str) -> list[str]:
    lines = block.split("\n")
    stripped_lines: list[str] = []
    for line in lines:
        # Find the first space after the number and dot
        space_index = line.find(" ")
        stripped_lines.append(line[space_index + 1 :])
    return stripped_lines


# TODO: This will benefit from proper comment work
def markdown_to_html_node(markdown: str) -> ParentNode:
    parent: ParentNode = ParentNode("div", [])
    assert parent.children is not None

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_blocktype(block)
        match block_type:
            case BlockType.TEXT:
                text_content = block.replace("\n", " ")
                text_leaves: list[HTMLNode] = text_to_children(text_content)
                text_html = ParentNode("p", text_leaves)
                parent.children.append(text_html)

            case BlockType.HEADER:
                value = len(block) - len(block.lstrip("#"))
                header_text = block.lstrip("#").lstrip()
                header_leaves: list[HTMLNode] = text_to_children(header_text)
                header_html = ParentNode(f"h{value}", header_leaves)
                parent.children.append(header_html)

            case BlockType.CODE:
                code_block = block[4:-3]
                code_html = ParentNode("pre", [LeafNode("code", code_block)])
                parent.children.append(code_html)

            case BlockType.BLOCKQUOTE:
                lines = block.split("\n")
                stripped_lines = [line[1:].lstrip() for line in lines]
                quote_block = "\n".join(stripped_lines).replace("\n", " ")

                quote_leaves: list[HTMLNode] = text_to_children(quote_block)
                quote_html = ParentNode("blockquote", quote_leaves)
                parent.children.append(quote_html)

            case BlockType.LIST:
                uo_ls_lines = strip_unordered_list_symbols(block)
                uo_list_leaves: list[HTMLNode] = []
                for line in uo_ls_lines:
                    uo_ls_item_leaves: list[HTMLNode] = text_to_children(line)
                    uo_ls_item_html = ParentNode("li", uo_ls_item_leaves)
                    uo_list_leaves.append(uo_ls_item_html)
                uo_list_html = ParentNode("ul", uo_list_leaves)
                parent.children.append(uo_list_html)

            case BlockType.NUMLIST:
                o_ls_lines = strip_ordered_list_symbols(block)
                o_list_leaves: list[HTMLNode] = []
                for line in o_ls_lines:
                    o_ls_item_leaves: list[HTMLNode] = text_to_children(line)
                    o_ls_item_html = ParentNode("li", o_ls_item_leaves)
                    o_list_leaves.append(o_ls_item_html)
                o_list_html = ParentNode("ol", o_list_leaves)
                parent.children.append(o_list_html)

            case _:
                raise ValueError("Unknown markdown block type")

    return parent
