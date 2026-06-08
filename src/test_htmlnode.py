import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_one_prop(self):
        node = HTMLNode(
            props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"'
        )

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_raises_not_implemented_error(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode(
            "a",
            "Click me",
            None,
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(a, Click me, None, {'href': 'https://www.google.com'})"
        )

    def test_init_with_tag_and_value(self):
        node = HTMLNode("p", "Hello world")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello world")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_children(self):
        child_node = HTMLNode("span", "child")
        parent_node = HTMLNode("div", None, [child_node])

        self.assertEqual(parent_node.tag, "div")
        self.assertEqual(parent_node.children, [child_node])

    def test_init_with_all_fields(self):
        child_node = HTMLNode("b", "bold text")
        node = HTMLNode(
            "div",
            "parent",
            [child_node],
            {"class": "container"}
        )

        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "parent")
        self.assertEqual(node.children, [child_node])
        self.assertEqual(node.props, {"class": "container"})


if __name__ == "__main__":
    unittest.main()