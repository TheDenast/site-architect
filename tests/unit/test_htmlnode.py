import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # HTML Node TESTS
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

    # Leaf Node TESTS
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

    # Parent Node TESTS
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_with_props(self):
        child_node = LeafNode("p", "text")
        parent_node = ParentNode(
            "div", [child_node], {"class": "container", "id": "main"}
        )
        self.assertEqual(
            parent_node.to_html(), '<div class="container" id="main"><p>text</p></div>'
        )

    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("span", "second")
        child3 = LeafNode("span", "third")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><span>second</span><span>third</span></div>",
        )

    def test_parent_node_with_mixed_children(self):
        leaf_child = LeafNode("span", "text")
        text_child = LeafNode(None, "plain text")
        parent_child = ParentNode("p", [LeafNode("em", "emphasized")])
        parent_node = ParentNode("div", [leaf_child, text_child, parent_child])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>text</span>plain text<p><em>emphasized</em></p></div>",
        )

    def test_parent_node_missing_tag(self):
        child_node = LeafNode("p", "text")
        parent_node = ParentNode(None, [child_node])  # pyright: ignore[reportArgumentType]
        with self.assertRaises(ValueError) as context:
            _ = parent_node.to_html()
        self.assertTrue("All parent nodes need to be tagged" in str(context.exception))

    def test_parent_node_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")


if __name__ == "__main__":
    _ = unittest.main()
