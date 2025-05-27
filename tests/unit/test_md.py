import unittest

from src.md import markdown_to_blocks, block_to_blocktype, BlockType, extract_title


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


class TestBlockToBlocktype(unittest.TestCase):
    def test_heading_single_hash(self):
        self.assertEqual(block_to_blocktype("# Heading 1"), BlockType.HEADER)

    def test_heading_multiple_hashes(self):
        self.assertEqual(block_to_blocktype("### Heading 3"), BlockType.HEADER)
        self.assertEqual(block_to_blocktype("###### Heading 6"), BlockType.HEADER)

    def test_heading_invalid_seven_hashes(self):
        self.assertEqual(block_to_blocktype("####### Not a heading"), BlockType.TEXT)

    def test_heading_no_space(self):
        self.assertEqual(block_to_blocktype("#NoSpace"), BlockType.TEXT)

    def test_code_block_simple(self):
        self.assertEqual(block_to_blocktype("```\ncode here\n```"), BlockType.CODE)

    def test_code_block_with_language(self):
        self.assertEqual(
            block_to_blocktype("```python\nprint('hello')\n```"), BlockType.CODE
        )

    def test_code_block_no_end(self):
        self.assertEqual(block_to_blocktype("```\ncode here"), BlockType.TEXT)

    def test_quote_single_line(self):
        self.assertEqual(block_to_blocktype(">This is a quote"), BlockType.BLOCKQUOTE)

    def test_quote_multiline(self):
        quote = ">First line\n>Second line\n>Third line"
        self.assertEqual(block_to_blocktype(quote), BlockType.BLOCKQUOTE)

    def test_quote_missing_one_marker(self):
        quote = ">First line\nSecond line\n>Third line"
        self.assertEqual(block_to_blocktype(quote), BlockType.TEXT)

    def test_unordered_list_single_item(self):
        self.assertEqual(block_to_blocktype("- Item 1"), BlockType.LIST)

    def test_unordered_list_multiple_items(self):
        ul = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_blocktype(ul), BlockType.LIST)

    def test_unordered_list_missing_space(self):
        self.assertEqual(block_to_blocktype("-NoSpace"), BlockType.TEXT)

    def test_unordered_list_missing_one_dash(self):
        ul = "- Item 1\nItem 2\n- Item 3"
        self.assertEqual(block_to_blocktype(ul), BlockType.TEXT)

    def test_ordered_list_single_item(self):
        self.assertEqual(block_to_blocktype("1. Item 1"), BlockType.NUMLIST)

    def test_ordered_list_sequential(self):
        ol = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_blocktype(ol), BlockType.NUMLIST)

    def test_ordered_list_wrong_sequence(self):
        ol = "1. First\n3. Third\n2. Second"
        self.assertEqual(block_to_blocktype(ol), BlockType.TEXT)

    def test_ordered_list_not_starting_at_one(self):
        ol = "2. Second\n3. Third"
        self.assertEqual(block_to_blocktype(ol), BlockType.TEXT)

    def test_ordered_list_missing_space(self):
        self.assertEqual(block_to_blocktype("1.NoSpace"), BlockType.TEXT)

    def test_paragraph_plain_text(self):
        self.assertEqual(block_to_blocktype("Just plain text"), BlockType.TEXT)

    def test_paragraph_multiline_text(self):
        para = "This is a paragraph\nwith multiple lines\nof text"
        self.assertEqual(block_to_blocktype(para), BlockType.TEXT)


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_valid(self):
        markdown = "# Hello World\nSome content here"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_whitespace(self):
        markdown = "   # My Title   \nMore content"
        self.assertEqual(extract_title(markdown), "My Title   ")

    def test_extract_title_no_title(self):
        markdown = "Just some content\nNo title here"
        with self.assertRaises(ValueError) as cm:
            _ = extract_title(markdown)
        self.assertIn("No title found", str(cm.exception))

    def test_extract_title_multiple_titles(self):
        markdown = "# First Title\nSome content\n# Second Title"
        with self.assertRaises(ValueError) as cm:
            _ = extract_title(markdown)
        self.assertIn("Multiple titles found", str(cm.exception))

    def test_extract_title_empty_string(self):
        with self.assertRaises(ValueError) as cm:
            _ = extract_title("")
        self.assertIn("No title found", str(cm.exception))

    def test_extract_title_only_hash(self):
        markdown = "# \nSome content"
        self.assertEqual(extract_title(markdown), "")
