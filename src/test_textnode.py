import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://www.example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_vs_none(self):
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        node2 = TextNode("Click here", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            repr(node),
            "TextNode(This is a text node,bold,None)"
        )

    def test_repr_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://www.example.com")
        self.assertEqual(
            repr(node),
            "TextNode(Click here,link,https://www.example.com)"
        )

    def test_plaintext_type_value(self):
        node = TextNode("Hello world", TextType.PLAINTEXT)
        self.assertEqual(node.text_type.value, "text")

    def test_image_node(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        node2 = TextNode("Alt text", TextType.IMAGE, "image.png")
        self.assertEqual(node, node2)
    def test_not_eq_different_object_type(self):
        node = TextNode("Hello", TextType.BOLD)
        self.assertNotEqual(node, "Hello")
if __name__ == "__main__":
    unittest.main()