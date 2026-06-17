import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_leaf_to_html_with_props(self):
        node = LeafNode(
            "a",
            "Click here",
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click here</a>'
        )

    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode(
            "a",
            "Click here",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">Click here</a>'
        )

    def test_leaf_to_html_with_class_prop(self):
        node = LeafNode(
            "p",
            "This is a paragraph",
            {"class": "paragraph-text"}
        )
        self.assertEqual(
            node.to_html(),
            '<p class="paragraph-text">This is a paragraph</p>'
        )

    def test_leaf_to_html_value_none_raises_value_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            repr(node),
            "LeafNode(p, Hello, world!, None)"
        )

    def test_repr_with_props(self):
        node = LeafNode(
            "a",
            "Click here",
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            repr(node),
            "LeafNode(a, Click here, {'href': 'https://www.google.com'})"
        )

    def test_leaf_node_has_no_children(self):
        node = LeafNode("p", "Hello")
        self.assertIsNone(node.children)

    def test_leaf_node_stores_tag_value_and_props(self):
        node = LeafNode(
            "img",
            "Image alt text",
            {"src": "image.png"}
        )

        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "Image alt text")
        self.assertEqual(node.props, {"src": "image.png"})


if __name__ == "__main__":
    unittest.main()