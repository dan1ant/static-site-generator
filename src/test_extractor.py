import unittest

from extractor import extract_markdown_images, extract_markdown_links

class TestExtractor(unittest.TestCase):
    def test_markdown_images_extractor(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(matches, expected)

    def test_markdown_link_extractor(self):
        matches = extract_markdown_links(
                "This is text with a [boot.dev](https://www.boot.dev)"
        )
        expected = [("boot.dev", "https://www.boot.dev")]
        self.assertListEqual(matches, expected)

    def test_markdown_double_image_extractor(self):
        matches = extract_markdown_images(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(matches, expected)

    def test_markdown_double_link_extractor(self):
        matches = extract_markdown_links(
                "This is text with a [boot.dev](https://www.boot.dev) [example.com](https://www.example.com)"
        )
        expected = [
                ("boot.dev", "https://www.boot.dev"),
                ("example.com", "https://www.example.com")
        ]
        self.assertListEqual(matches, expected)

    def test_markdown_link_image_extract_link(self):
        matches =  extract_markdown_links(
                "This is text with a [boot.dev](https://www.boot.dev) ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [
                ("boot.dev", "https://www.boot.dev")
        ]
        self.assertListEqual(matches, expected)

if __name__ == "__main__":
    unittest.main()
