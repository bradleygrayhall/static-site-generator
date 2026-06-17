import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("Different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        node2 = TextNode("Click me", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_other_object_type(self):
        node = TextNode("Hello", TextType.TEXT)
        self.assertNotEqual(node, "Hello")

    def test_repr(self):
        node = TextNode("Hello", TextType.BOLD)
        self.assertEqual(
            repr(node),
            "TextNode(Hello,bold,None)"
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_node_to_html_text(self):
        text_node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Plain text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "Plain text")

    def test_text_node_to_html_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_to_html_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_to_html_code(self):
        text_node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hello')")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.to_html(), "<code>print('hello')</code>")

    def test_text_node_to_html_link(self):
        text_node = TextNode(
            "Click here",
            TextType.LINK,
            "https://www.google.com"
        )
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertEqual(
            html_node.to_html(),
            '<a href="https://www.google.com">Click here</a>'
        )

    def test_text_node_to_html_image(self):
        text_node = TextNode(
            "This is alt text",
            TextType.IMAGE,
            "image.png"
        )
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "image.png",
                "alt": "This is alt text",
            }
        )
        self.assertEqual(
            html_node.to_html(),
            '<img src="image.png" alt="This is alt text"></img>'
        )

    def test_text_node_to_html_returns_leafnode(self):
        text_node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)

    def test_text_node_to_html_invalid_type_raises_exception(self):
        text_node = TextNode("Hello", "invalid_type")

        with self.assertRaises(Exception):
            text_node_to_html_node(text_node)


if __name__ == "__main__":
    unittest.main()