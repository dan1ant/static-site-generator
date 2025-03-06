import unittest

from textnode import TextType, TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_notEq(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_sameType_notEq(self):
        node = TextNode("This is a text node", TextType.LINK, "www.example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
