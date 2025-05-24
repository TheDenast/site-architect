import unittest
from src.textnode import TextNode, TextType
from src.text_parsing import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("Just plain text with no images", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_empty_alt_text(self):
        node = TextNode(
            "Image with ![](https://example.com/image.png) empty alt", TextType.NORMAL
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Image with ", TextType.NORMAL),
                TextNode("", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" empty alt", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode("![solo](https://example.com/solo.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("solo", TextType.IMAGE, "https://example.com/solo.png")],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        node = TextNode("![first](url1)![second](url2)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "url1"),
                TextNode("second", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )

    def test_split_images_preserves_non_normal_nodes(self):
        nodes = [
            TextNode("![image](url)", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode("Another ![img](url2)", TextType.NORMAL),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "url"),
                TextNode("bold text", TextType.BOLD),  # unchanged
                TextNode("Another ", TextType.NORMAL),
                TextNode("img", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Just plain text with no links", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_empty_text(self):
        node = TextNode("Link with [](https://example.com) empty text", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Link with ", TextType.NORMAL),
                TextNode("", TextType.LINK, "https://example.com"),
                TextNode(" empty text", TextType.NORMAL),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode("[solo link](https://example.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("solo link", TextType.LINK, "https://example.com")], new_nodes
        )

    def test_split_links_consecutive(self):
        node = TextNode("[first](url1)[second](url2)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "url1"),
                TextNode("second", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_preserves_non_normal_nodes(self):
        nodes = [
            TextNode("[link](url)", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode("Another [link](url2)", TextType.NORMAL),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode("bold text", TextType.BOLD),
                TextNode("Another ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_split_links_ignores_images(self):
        node = TextNode("![not a link](url) but [this is](url2)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![not a link](url) but ", TextType.NORMAL),
                TextNode("this is", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        testing_nodes: list[TextNode] = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result_nodes = text_to_textnodes(text)
        self.assertListEqual(testing_nodes, result_nodes)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        check = []
        result = text_to_textnodes(text)
        self.assertEqual(result, check)

    def test_text_to_textnodes_nested_delimiters(self):
        text = "This is **bold with `code` inside** text"
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold with `code` inside", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_unclosed_delimiter(self):
        text = "This has **unclosed bold"
        with self.assertRaises(ValueError):
            _ = text_to_textnodes(text)

    def test_text_to_textnodes_image_with_delimiters_in_alt(self):
        text = "![alt with **bold**](url) regular text"
        expected = [
            TextNode("alt with **bold**", TextType.IMAGE, "url"),
            TextNode(" regular text", TextType.NORMAL),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_only_delimiters(self):
        text = "**bold** _italic_ `code`"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(expected, result)

    def test_text_to_textnodes_adjacent_different_delimiters(self):
        text = "**bold**_italic_`code`"
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(expected, result)

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
