import unittest

from src.md_parsing import markdown_to_blocks


class TestMarkdownParsing(unittest.TestCase):
    def test_md_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_paragraph(self):
        md = "Just a single paragraph with no empty lines."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with no empty lines."])

    def test_multiple_empty_lines(self):
        md = """First paragraph


Second paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_leading_trailing_newlines(self):
        md = """

First paragraph

Second paragraph

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_whitespace_only_lines(self):
        md = """First paragraph

Second paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])
