import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node_props = {
                "href": "https://www.example.com",
                "target": "_blank"
        }
        expected = ' href="https://www.example.com" target="_blank"'
        node = HTMLNode(props=node_props)
        self.assertEqual(node.props_to_html(), expected)

    def test_notEq(self):
        node_props = {
                "href": "https://www.example.org",
                "target": "_blank"
        }
        expected = ' href="https://www.example.com" target="_blank"'
        node = HTMLNode(props=node_props)
        self.assertNotEqual(node.props_to_html(), expected)

    def test_twoNodes_eq(self):
        node_props = {
                "href": "https://www.example.com",
                "target": "_blank"
        }
        node = HTMLNode(props=node_props)
        node2 = HTMLNode(props=node_props)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_p_eq(self):
        node = LeafNode("p", "This is a paragraph")
        expected = "<p>This is a paragraph</p>"
        self.assertEqual(node.to_html(), expected)
    
    def test_a_eq(self):
        node = LeafNode("a", "Go to Home", { "href": "https://www.boot.dev", "target": "_blank" })
        expected = '<a href="https://www.boot.dev" target="_blank">Go to Home</a>'
        self.assertEqual(node.to_html(), expected)

    def test_text_eq(self):
        node = LeafNode(None, "Plain Text")
        expected = "Plain Text"
        self.assertEqual(node.to_html(), expected)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span><b>grandchild</b></span></div>" 
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_a_tag(self):
        child_node = LeafNode("a", "Go to Home", { "href": "https://www.boot.dev", "target": "_blank" }) 
        parent_node = ParentNode("div", [child_node])
        expected = '<div><a href="https://www.boot.dev" target="_blank">Go to Home</a></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_node_raises_value_error(self):
        parent_node = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()
