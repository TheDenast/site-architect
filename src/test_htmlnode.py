import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    _ = unittest.main()
