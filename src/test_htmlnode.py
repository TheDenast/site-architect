import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("test_tag", "test_value")
        self.assertEqual(repr(node), "HTMLNode(test_tag, test_value, None, None)")

    def test_props_to_html(self):
        node = HTMLNode(props={"prop1": "val1", "prop2": "val2"})
        self.assertEqual(node.props_to_html(), 'prop1="val1" prop2="val2"')

    def test_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_special_char_props(self):
        node = HTMLNode(props={"data-test": "value", "class": "btn btn-primary"})
        self.assertEqual(
            node.props_to_html(), 'data-test="value" class="btn btn-primary"'
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_valuerr_without_value(self):
        # Use the context manager to assert that the code inside raises ValueError
        with self.assertRaises(ValueError):
            # This code should raise the exception
            _ = LeafNode()


if __name__ == "__main__":
    _ = unittest.main()
