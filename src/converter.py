from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    text = text_node.text
    url = text_node.url
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text)
        case TextType.BOLD:
            return LeafNode("b", text)
        case TextType.ITALIC:
            return LeafNode("i", text)
        case TextType.CODE:
            return LeafNode("code", text)
        case TextType.LINK:
            return LeafNode("a", text, { "href": url })
        case TextType.IMAGE:
            return LeafNode("img", "", { "src": url, "alt": text })
        case _:
            raise Exception("invalid TextType")

