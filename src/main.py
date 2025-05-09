from textnode import TextNode, TextType


def main() -> None:
    text_node = TextNode("test_text", TextType.LINK, "https://www.boot.dev")
    print(text_node)


main()
