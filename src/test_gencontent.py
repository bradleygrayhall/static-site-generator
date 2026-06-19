import unittest

from leafnode import LeafNode
from markdown_blocks import text_to_children, markdown_to_html_node


class TestTextToChildren(unittest.TestCase):
    def test_text_to_children_plain_text(self):
        children = text_to_children("plain text")

        self.assertEqual(
            children,
            [
                LeafNode(None, "plain text"),
            ],
        )

    def test_text_to_children_bold(self):
        children = text_to_children("This is **bold** text")

        self.assertEqual(
            [child.to_html() for child in children],
            [
                "This is ",
                "<b>bold</b>",
                " text",
            ],
        )

    def test_text_to_children_italic(self):
        children = text_to_children("This is _italic_ text")

        self.assertEqual(
            [child.to_html() for child in children],
            [
                "This is ",
                "<i>italic</i>",
                " text",
            ],
        )

    def test_text_to_children_code(self):
        children = text_to_children("This is `code` text")

        self.assertEqual(
            [child.to_html() for child in children],
            [
                "This is ",
                "<code>code</code>",
                " text",
            ],
        )

    def test_text_to_children_link(self):
        children = text_to_children("This is a [link](https://example.com)")

        self.assertEqual(
            [child.to_html() for child in children],
            [
                "This is a ",
                '<a href="https://example.com">link</a>',
            ],
        )

    def test_text_to_children_image(self):
        children = text_to_children("This is an ![image](image.png)")

        self.assertEqual(
            [child.to_html() for child in children],
            [
                "This is an ",
                '<img src="image.png" alt="image"></img>',
            ],
        )

    def test_text_to_children_all_inline_types(self):
        children = text_to_children(
            "This is **bold**, _italic_, `code`, "
            "![image](image.png), and [link](https://example.com)"
        )

        self.assertEqual(
            [child.to_html() for child in children],
            [
                "This is ",
                "<b>bold</b>",
                ", ",
                "<i>italic</i>",
                ", ",
                "<code>code</code>",
                ", ",
                '<img src="image.png" alt="image"></img>',
                ", and ",
                '<a href="https://example.com">link</a>',
            ],
        )


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_to_html_node_paragraph(self):
        markdown = "This is a paragraph."

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><p>This is a paragraph.</p></div>",
        )

    def test_markdown_to_html_node_bold_paragraph(self):
        markdown = "This is **bold** text."

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bold</b> text.</p></div>",
        )

    def test_markdown_to_html_node_heading_h1(self):
        markdown = "# Heading 1"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading 1</h1></div>",
        )

    def test_markdown_to_html_node_heading_h3(self):
        markdown = "### Heading 3"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h3>Heading 3</h3></div>",
        )

    def test_markdown_to_html_node_code_block(self):
        markdown = "```\nprint('hello')\n```"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><pre><code>print('hello')\n</code></pre></div>",
        )

    def test_markdown_to_html_node_quote(self):
        markdown = "> This is a quote"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><blockquote>> This is a quote</blockquote></div>",
        )

    def test_markdown_to_html_node_unordered_list(self):
        markdown = "- Item one\n- Item two\n- Item three"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><ul><li>Item one</li><li>Item two</li><li>Item three</li></ul></div>",
        )

    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. Item one\n2. Item two\n3. Item three"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><ol><li>Item one</li><li>Item two</li><li>Item three</li></ol></div>",
        )

    def test_markdown_to_html_node_multiple_blocks(self):
        markdown = "# Heading\n\nThis is a paragraph.\n\n- Item one\n- Item two"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading</h1><p>This is a paragraph.</p><ul><li>Item one</li><li>Item two</li></ul></div>",
        )

    def test_markdown_to_html_node_paragraph_with_link_and_image(self):
        markdown = "This has a [link](https://example.com) and ![image](image.png)"

        node = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            '<div><p>This has a <a href="https://example.com">link</a> and <img src="image.png" alt="image"></img></p></div>',
        )


if __name__ == "__main__":
    unittest.main()