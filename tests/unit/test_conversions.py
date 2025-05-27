import unittest

from src.textnode import TextType, TextNode
from src.conversions import text_node_to_html_node
from src.conversions import markdown_to_html_node


class TestConversions(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")

    def test_link_text(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode(
            "Image description", TextType.IMAGE, url="https://example.com/image.png"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "Image description"},
        )


class TestMDtoHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headers(self):
        md = """
# This is a h1

## This is a h2

### This is a h3 with **bold** text

#### This is a h4

##### This is a h5

###### This is a h6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a h1</h1><h2>This is a h2</h2><h3>This is a h3 with <b>bold</b> text</h3><h4>This is a h4</h4><h5>This is a h5</h5><h6>This is a h6</h6></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
> with multiple lines
> and some **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines and some <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First item
- Second item with **bold**
- Third item with _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item with <b>bold</b></li><li>Third item with <i>italic</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First numbered item
2. Second item with `code`
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First numbered item</li><li>Second item with <code>code</code></li><li>Third item</li></ol></div>",
        )

    def test_mixed_content(self):
        md = """
# Main Title

This is a paragraph with **bold** and _italic_ text.

## Subsection

> Here's a quote
> with multiple lines

### Code Example

```
def hello():
    print("world")
```

#### List of items

- Item one
- Item two with `inline code`
- Item three

##### Numbered steps

1. Do this first
2. Then do this
3. Finally this
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        # This tests the full integration - adjust expected string as needed
        self.assertIn("<h1>Main Title</h1>", html)
        self.assertIn(
            "<blockquote>Here's a quote with multiple lines</blockquote>", html
        )
        self.assertIn(
            '<pre><code>def hello():\n    print("world")\n</code></pre>', html
        )
        self.assertIn("<ul><li>Item one</li>", html)
        self.assertIn("<ol><li>Do this first</li>", html)

    def test_links_and_images(self):
        md = """
Check out [this link](https://example.com) and this image:

![Alt text](https://example.com/image.png)
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn('<a href="https://example.com">this link</a>', html)
        self.assertIn('<img src="https://example.com/image.png" alt="Alt text">', html)
