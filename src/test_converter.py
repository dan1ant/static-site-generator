import unittest

from converter import text_node_to_html_node
from textnode import TextType, TextNode
from htmlnode import LeafNode

class TestConverter(unittest.TestCase):
    def test_normal_text_type_to_text_leaf(self):
        node = self.__create_text_node("Hello", TextType.NORMAL)
        expected = "Hello"
        result = text_node_to_html_node(node).to_html()
        self.assertEqual(result, expected)

    def test_bold_text_type_to_bold_leaf(self):
        node = self.__create_text_node("Hello", TextType.BOLD)
        expected = "<b>Hello</b>"
        result = text_node_to_html_node(node).to_html()
        self.assertEqual(result, expected)

    def test_italic_text_type_to_italic_leaf(self):
        node = self.__create_text_node("Hello", TextType.ITALIC)
        expected = "<i>Hello</i>"
        result = text_node_to_html_node(node).to_html()
        self.assertEqual(result, expected)

    def test_code_text_type_to_code_leaf(self):
        node = self.__create_text_node("Hello", TextType.CODE)
        expected = "<code>Hello</code>"
        result = text_node_to_html_node(node).to_html()
        self.assertEqual(result, expected)

    def test_link_text_type_to_link_leaf(self):
        node = self.__create_text_node("Hello", TextType.LINK, "https://www.boot.dev")
        expected = '<a href="https://www.boot.dev">Hello</a>'
        result = text_node_to_html_node(node).to_html()
        self.assertEqual(result, expected)

    def test_image_text_type_to_image_leaf(self):
        node = self.__create_text_node("Hello", TextType.IMAGE, "https://www.example.org/image")
        expected = '<img src="https://www.example.org/image" alt="Hello"></img>'
        result = text_node_to_html_node(node).to_html()
        self.assertEqual(result, expected)

    def __create_text_node(self, text, text_type, url=None):
        return TextNode(text, text_type, url)

if __name__ == "__main__":
    unittest.main()
