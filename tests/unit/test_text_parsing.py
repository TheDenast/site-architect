import unittest
from src.textnode import TextNode, TextType
from src.text_parsing import (
    split_nodes_delimiter,
)  # Replace with your actual module name


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
