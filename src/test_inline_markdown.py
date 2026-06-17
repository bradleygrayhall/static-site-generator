import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links


class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images_single_image(self):
        text = "This is an image ![alt text](image.png)"
        matches = extract_markdown_images(text)

        self.assertEqual(
            matches,
            [("alt text", "image.png")]
        )

    def test_extract_markdown_images_multiple_images(self):
        text = "![first image](first.png) and ![second image](second.jpg)"
        matches = extract_markdown_images(text)

        self.assertEqual(
            matches,
            [
                ("first image", "first.png"),
                ("second image", "second.jpg"),
            ]
        )

    def test_extract_markdown_images_empty_alt_text(self):
        text = "This image has no alt text ![](image.png)"
        matches = extract_markdown_images(text)

        self.assertEqual(
            matches,
            [("", "image.png")]
        )

    def test_extract_markdown_images_with_url(self):
        text = "Here is an image ![logo](https://example.com/logo.png)"
        matches = extract_markdown_images(text)

        self.assertEqual(
            matches,
            [("logo", "https://example.com/logo.png")]
        )

    def test_extract_markdown_images_no_images(self):
        text = "This text has no markdown images."
        matches = extract_markdown_images(text)

        self.assertEqual(matches, [])

    def test_extract_markdown_links_single_link(self):
        text = "This is a [link](https://example.com)"
        matches = extract_markdown_links(text)

        self.assertEqual(
            matches,
            [("link", "https://example.com")]
        )

    def test_extract_markdown_links_multiple_links(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        matches = extract_markdown_links(text)

        self.assertEqual(
            matches,
            [
                ("Google", "https://google.com"),
                ("GitHub", "https://github.com"),
            ]
        )

    def test_extract_markdown_links_empty_link_text(self):
        text = "This has an empty link [](https://example.com)"
        matches = extract_markdown_links(text)

        self.assertEqual(
            matches,
            [("", "https://example.com")]
        )

    def test_extract_markdown_links_no_links(self):
        text = "This text has no markdown links."
        matches = extract_markdown_links(text)

        self.assertEqual(matches, [])

    def test_extract_markdown_links_does_not_extract_images(self):
        text = "This is an image ![alt text](image.png)"
        matches = extract_markdown_links(text)

        self.assertEqual(matches, [])

    def test_extract_markdown_images_does_not_extract_links(self):
        text = "This is a [link](https://example.com)"
        matches = extract_markdown_images(text)

        self.assertEqual(matches, [])

    def test_extract_links_and_images_from_same_text(self):
        text = (
            "Here is a [link](https://example.com) "
            "and here is an image ![alt](image.png)"
        )

        link_matches = extract_markdown_links(text)
        image_matches = extract_markdown_images(text)

        self.assertEqual(
            link_matches,
            [("link", "https://example.com")]
        )

        self.assertEqual(
            image_matches,
            [("alt", "image.png")]
        )

    def test_extract_markdown_link_with_spaces(self):
        text = "This is [my link](https://example.com/some page)"
        matches = extract_markdown_links(text)

        self.assertEqual(
            matches,
            [("my link", "https://example.com/some page")]
        )

    def test_extract_markdown_image_with_spaces(self):
        text = "This is ![my image](images/my image.png)"
        matches = extract_markdown_images(text)

        self.assertEqual(
            matches,
            [("my image", "images/my image.png")]
        )

    def test_invalid_nested_brackets_link(self):
        text = "This is [a [nested] link](https://example.com)"
        matches = extract_markdown_links(text)

        self.assertEqual(matches, [])

    def test_invalid_nested_brackets_image(self):
        text = "This is ![a [nested] image](image.png)"
        matches = extract_markdown_images(text)

        self.assertEqual(matches, [])

    def test_invalid_nested_parentheses_link(self):
        text = "This is [link](https://example.com/page(test))"
        matches = extract_markdown_links(text)

        self.assertEqual(matches, [])

    def test_invalid_nested_parentheses_image(self):
        text = "This is ![image](image(test).png)"
        matches = extract_markdown_images(text)

        self.assertEqual(matches, [])


if __name__ == "__main__":
    unittest.main()