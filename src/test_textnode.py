import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        node2 = TextNode("This is a link", TextType.LINK, "https://hello.world")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, TextType.BOLD)")

    def test_repr_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://hello.world")
        self.assertEqual(
            repr(node), "TextNode(This is a link, TextType.LINK, https://hello.world)"
        )

    def test_link_without_url_raises_exception(self):
        # Use the context manager to assert that the code inside raises ValueError
        with self.assertRaises(ValueError):
            # This code should raise the exception
            _ = TextNode("This is a link", TextType.LINK)


if __name__ == "__main__":
    _ = unittest.main()
