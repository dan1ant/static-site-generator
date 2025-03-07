import unittest

from converter import (
        text_node_to_html_node, 
        text_to_textnodes,
        split_nodes_delimiter,
        split_nodes_link,
        split_nodes_image
)
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

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_text_to_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_text_to_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_more_than_one_of_same_type(self):
        node = TextNode("This is text with **bold1** and **bold2**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with ", TextType.NORMAL),
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold2", TextType.BOLD)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_multiple_syntax(self):
        node = TextNode("This is text with _italic_ and **bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is text with ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_expect_expection(self):
        node = TextNode("This is a `malformatted** text", TextType.NORMAL)
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

class TestSplitNodesImage(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.NORMAL,
        )
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        expected = [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected)

    def test_split_images_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" ", TextType.NORMAL),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, expected)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_link(self):
        node = TextNode(
            "[link](https://www.google.com)",
            TextType.NORMAL,
        )
        expected = [
            TextNode("link", TextType.LINK, "https://www.google.com"),
        ]
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, expected)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.example.com)",
            TextType.NORMAL,
        )
        expected = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://www.google.com"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode(
                "second link", TextType.LINK, "https://www.example.com"
            ),
        ]
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, expected)

    def test_split_links_no_text(self):
        node = TextNode(
            "[link](https://www.google.com) [second link](https://www.example.com)",
            TextType.NORMAL,
        )
        expected = [
            TextNode("link", TextType.LINK, "https://www.google.com"),
            TextNode(" ", TextType.NORMAL),
            TextNode("second link", TextType.LINK, "https://www.example.com"),
        ]
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, expected)

class TestTextToTextNodes(unittest.TestCase):
    def test_test_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)" 
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        nodes = text_to_textnodes(text) 
        self.assertListEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()
