import unittest
from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_to_html_with_one_child(self):
        child = LeafNode("p", "Hello, world!")
        parent = ParentNode("div", [child])

        self.assertEqual(
            parent.to_html(),
            "<div><p>Hello, world!</p></div>"
        )

    def test_parent_to_html_with_multiple_children(self):
        child1 = LeafNode("p", "Hello")
        child2 = LeafNode("p", "World")
        parent = ParentNode("div", [child1, child2])

        self.assertEqual(
            parent.to_html(),
            "<div><p>Hello</p><p>World</p></div>"
        )

    def test_parent_to_html_with_plain_text_child(self):
        child = LeafNode(None, "Plain text")
        parent = ParentNode("p", [child])

        self.assertEqual(
            parent.to_html(),
            "<p>Plain text</p>"
        )

    def test_parent_to_html_with_props(self):
        child = LeafNode(None, "Click here")
        parent = ParentNode(
            "a",
            [child],
            {"href": "https://www.google.com"}
        )

        self.assertEqual(
            parent.to_html(),
            '<a href="https://www.google.com">Click here</a>'
        )

    def test_parent_to_html_with_multiple_props(self):
        child = LeafNode(None, "Click here")
        parent = ParentNode(
            "a",
            [child],
            {
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

        self.assertEqual(
            parent.to_html(),
            '<a href="https://www.google.com" target="_blank">Click here</a>'
        )

    def test_parent_to_html_nested_nodes(self):
        bold = LeafNode("b", "bold text")
        paragraph = ParentNode("p", [bold])
        div = ParentNode("div", [paragraph])

        self.assertEqual(
            div.to_html(),
            "<div><p><b>bold text</b></p></div>"
        )

    def test_parent_to_html_deeply_nested_nodes(self):
        text = LeafNode(None, "This is text")
        italic = ParentNode("i", [text])
        bold = ParentNode("b", [italic])
        div = ParentNode("div", [bold])

        self.assertEqual(
            div.to_html(),
            "<div><b><i>This is text</i></b></div>"
        )

    def test_parent_to_html_tag_none_raises_value_error(self):
        child = LeafNode(None, "Text")
        parent = ParentNode(None, [child])

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_to_html_children_none_raises_value_error(self):
        parent = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_to_html_empty_children(self):
        parent = ParentNode("div", [])

        self.assertEqual(
            parent.to_html(),
            "<div></div>"
        )

    def test_parent_node_stores_tag_children_and_props(self):
        child = LeafNode("p", "Hello")
        parent = ParentNode(
            "div",
            [child],
            {"class": "container"}
        )

        self.assertEqual(parent.tag, "div")
        self.assertIsNone(parent.value)
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, {"class": "container"})

    def test_parent_to_html_list_items(self):
        item1 = LeafNode("li", "Item 1")
        item2 = LeafNode("li", "Item 2")
        parent = ParentNode("ul", [item1, item2])

        self.assertEqual(
            parent.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li></ul>"
        )


if __name__ == "__main__":
    unittest.main()