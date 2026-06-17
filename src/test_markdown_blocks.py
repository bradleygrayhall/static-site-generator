import unittest

from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_single_block(self):
        markdown = "This is a single block of text."

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is a single block of text.",
            ],
        )

    def test_markdown_to_blocks_multiple_blocks(self):
        markdown = "This is block one.\n\nThis is block two.\n\nThis is block three."

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is block one.",
                "This is block two.",
                "This is block three.",
            ],
        )

    def test_markdown_to_blocks_removes_extra_whitespace(self):
        markdown = "   This is block one.   \n\n   This is block two.   "

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is block one.",
                "This is block two.",
            ],
        )

    def test_markdown_to_blocks_ignores_empty_blocks(self):
        markdown = "This is block one.\n\n\n\nThis is block two."

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is block one.",
                "This is block two.",
            ],
        )

    def test_markdown_to_blocks_with_leading_and_trailing_newlines(self):
        markdown = "\n\nThis is block one.\n\nThis is block two.\n\n"

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "This is block one.",
                "This is block two.",
            ],
        )

    def test_markdown_to_blocks_with_multiline_block(self):
        markdown = "Line one\nLine two\nLine three\n\nSecond block"

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "Line one\nLine two\nLine three",
                "Second block",
            ],
        )

    def test_markdown_to_blocks_heading_and_paragraph(self):
        markdown = "# Heading\n\nThis is a paragraph."

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph.",
            ],
        )

    def test_markdown_to_blocks_lists(self):
        markdown = "- Item one\n- Item two\n- Item three\n\nAnother block"

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(
            blocks,
            [
                "- Item one\n- Item two\n- Item three",
                "Another block",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        markdown = ""

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        markdown = "   \n\n   \n\n   "

        blocks = markdown_to_blocks(markdown)

        self.assertEqual(blocks, [])


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is a normal paragraph of text."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_multiline_paragraph(self):
        block = "This is a paragraph\nthat spans multiple lines."

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_heading_h1(self):
        block = "# Heading 1"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_block_to_block_type_heading_h2(self):
        block = "## Heading 2"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_block_to_block_type_heading_h6(self):
        block = "###### Heading 6"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING,
        )

    def test_block_to_block_type_not_heading_without_space(self):
        block = "#Heading without space"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_not_heading_too_many_hashes(self):
        block = "####### Too many hashes"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_code_block(self):
        block = "```\nprint('hello')\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_block_to_block_type_code_block_multiple_lines(self):
        block = "```\ndef hello():\n    return 'world'\n```"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_block_to_block_type_not_code_missing_closing_backticks(self):
        block = "```\nprint('hello')"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_quote_single_line(self):
        block = "> This is a quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_block_to_block_type_quote_without_space(self):
        block = ">This is also a quote"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_block_to_block_type_quote_multiple_lines(self):
        block = "> This is line one\n> This is line two\n> This is line three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_block_to_block_type_not_quote_if_one_line_missing_prefix(self):
        block = "> This is line one\nThis line is missing the quote marker"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_unordered_list_single_item(self):
        block = "- Item one"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_block_to_block_type_unordered_list_multiple_items(self):
        block = "- Item one\n- Item two\n- Item three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_block_to_block_type_not_unordered_list_missing_space(self):
        block = "-Item one"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_not_unordered_list_if_one_line_missing_prefix(self):
        block = "- Item one\nItem two"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_ordered_list_single_item(self):
        block = "1. Item one"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_block_to_block_type_ordered_list_multiple_items(self):
        block = "1. Item one\n2. Item two\n3. Item three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_block_to_block_type_not_ordered_list_wrong_start_number(self):
        block = "2. Item two\n3. Item three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_not_ordered_list_skips_number(self):
        block = "1. Item one\n3. Item three"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_not_ordered_list_missing_space(self):
        block = "1.Item one"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_not_ordered_list_if_one_line_missing_prefix(self):
        block = "1. Item one\nItem two"

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()