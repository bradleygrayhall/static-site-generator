import unittest

from textnode import TextNode, TextType
from delimiter import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_multiple_matches(self):
        node = TextNode("This has **bold** and **more bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("more bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_no_match(self):
        node = TextNode("This is normal text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is normal text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_invalid_markdown(self):
        node = TextNode("This has **invalid markdown", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_preserves_non_text_nodes(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("already bold", TextType.BOLD),
            ],
        )

    def test_split_nodes_delimiter_at_start(self):
        node = TextNode("**bold** text after", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text after", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_at_end(self):
        node = TextNode("text before **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("text before ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_split_nodes_delimiter_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes, [])

    def test_split_nodes_image_single_image(self):
        node = TextNode(
            "This is an image ![alt text](image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "image.png"),
            ],
        )

    def test_split_nodes_image_multiple_images(self):
        node = TextNode(
            "Images: ![first](first.png) and ![second](second.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("Images: ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "first.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "second.jpg"),
            ],
        )

    def test_split_nodes_image_at_start(self):
        node = TextNode("![alt](image.png) after image", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("alt", TextType.IMAGE, "image.png"),
                TextNode(" after image", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_at_end(self):
        node = TextNode("before image ![alt](image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("before image ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "image.png"),
            ],
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("This has no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has no images", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_does_not_split_links(self):
        node = TextNode("This is a [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a [link](https://example.com)", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_preserves_non_text_node(self):
        node = TextNode("already image", TextType.IMAGE, "image.png")
        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("already image", TextType.IMAGE, "image.png"),
            ],
        )

    def test_split_nodes_link_single_link(self):
        node = TextNode(
            "This is a [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_split_nodes_link_multiple_links(self):
        node = TextNode(
            "Links: [Google](https://google.com) and [GitHub](https://github.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
            ],
        )

    def test_split_nodes_link_at_start(self):
        node = TextNode("[link](https://example.com) after link", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" after link", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_at_end(self):
        node = TextNode("before link [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("before link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("This has no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has no links", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_does_not_split_images(self):
        node = TextNode("This is an image ![alt](image.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is an image ![alt](image.png)", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_preserves_non_text_node(self):
        node = TextNode("already link", TextType.LINK, "https://example.com")
        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("already link", TextType.LINK, "https://example.com"),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_plain_text(self):
        nodes = text_to_textnodes("This is plain text")

        self.assertEqual(
            nodes,
            [
                TextNode("This is plain text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_bold(self):
        nodes = text_to_textnodes("This is **bold** text")

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_italic(self):
        nodes = text_to_textnodes("This is _italic_ text")

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_code(self):
        nodes = text_to_textnodes("This is `code` text")

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_text_to_textnodes_image(self):
        nodes = text_to_textnodes("This is an ![image](image.png)")

        self.assertEqual(
            nodes,
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image.png"),
            ],
        )

    def test_text_to_textnodes_link(self):
        nodes = text_to_textnodes("This is a [link](https://example.com)")

        self.assertEqual(
            nodes,
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_text_to_textnodes_all_types(self):
        text = (
            "This is **bold**, _italic_, `code`, "
            "an ![image](image.png), and a [link](https://example.com)"
        )

        nodes = text_to_textnodes(text)

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(", an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image.png"),
                TextNode(", and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_text_to_textnodes_multiple_same_type(self):
        nodes = text_to_textnodes("**bold one** normal **bold two**")

        self.assertEqual(
            nodes,
            [
                TextNode("bold one", TextType.BOLD),
                TextNode(" normal ", TextType.TEXT),
                TextNode("bold two", TextType.BOLD),
            ],
        )

    def test_text_to_textnodes_image_and_link(self):
        nodes = text_to_textnodes(
            "This has ![image](image.png) and [link](https://example.com)"
        )

        self.assertEqual(
            nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
        )

    def test_text_to_textnodes_invalid_bold_markdown(self):
        with self.assertRaises(Exception):
            text_to_textnodes("This has **invalid markdown")

    def test_text_to_textnodes_invalid_italic_markdown(self):
        with self.assertRaises(Exception):
            text_to_textnodes("This has _invalid markdown")

    def test_text_to_textnodes_invalid_code_markdown(self):
        with self.assertRaises(Exception):
            text_to_textnodes("This has `invalid markdown")


if __name__ == "__main__":
    unittest.main()