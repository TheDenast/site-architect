import unittest
from src.textnode import TextNode, TextType
from src.text_parsing import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_delimiter_middle(self):
        # Test a bold delimiter in the middle of text
        node = TextNode("This is **bold** text", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "This is ")
        self.assertEqual(result[0].text_type, TextType.NORMAL)
        self.assertEqual(result[1].text, "bold")
        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[2].text_type, TextType.NORMAL)

    def test_code_delimiter_beginning(self):
        # Test a code delimiter at the beginning
        node = TextNode("`code` at start", TextType.NORMAL)
        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "code")
        self.assertEqual(result[0].text_type, TextType.CODE)
        self.assertEqual(result[1].text, " at start")
        self.assertEqual(result[1].text_type, TextType.NORMAL)

    def test_no_delimiter(self):
        # Test when no delimiter is present in the text
        node = TextNode("No special formatting here", TextType.NORMAL)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "No special formatting here")
        self.assertEqual(result[0].text_type, TextType.NORMAL)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extraction_empty_text(self):
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_links(""), [])

    def test_extraction_no_images_or_links(self):
        text = "This is just plain text with no markdown links or images."
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_extraction_complex_urls(self):
        text = "Check out this link [complex URL](https://example.com/path?query=value&another=123#fragment)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                (
                    "complex URL",
                    "https://example.com/path?query=value&another=123#fragment",
                )
            ],
        )

    # TODO: This functionality is not yet supported
    #
    # def test_multiple_delimiters(self):
    #     # Test when multiple delimiters are present in the text
    #     node = TextNode("**bold** and **another bold**", TextType.NORMAL)
    #     result = split_nodes_delimiter([node], "**", TextType.BOLD)
    #
    #     self.assertEqual(len(result), 5)
    #     self.assertEqual(result[0].text, "")
    #     self.assertEqual(result[0].text_type, TextType.NORMAL)
    #     self.assertEqual(result[1].text, "bold")
    #     self.assertEqual(result[1].text_type, TextType.BOLD)
    #     self.assertEqual(result[2].text, " and ")
    #     self.assertEqual(result[2].text_type, TextType.NORMAL)
    #     self.assertEqual(result[3].text, "another bold")
    #     self.assertEqual(result[3].text_type, TextType.BOLD)
    #     self.assertEqual(result[4].text, "")
    #     self.assertEqual(result[4].text_type, TextType.NORMAL)
