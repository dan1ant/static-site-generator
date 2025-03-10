from textnode import TextType, TextNode
from htmlnode import LeafNode
from extractor import extract_markdown_links, extract_markdown_images

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
            raise ValueError("invalid TextType")

def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL) 
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        nodes = []
        old_node_text_split = old_node.text.split(delimiter)
        if len(old_node_text_split) % 2 == 0:
            raise ValueError("text is missing matching closing delimiter")
        for i in range(len(old_node_text_split)):
            text_split = old_node_text_split[i]
            if text_split == "":
                continue
            if i % 2 == 0:
                nodes.append(TextNode(text_split, TextType.NORMAL))
            else:
                nodes.append(TextNode(text_split, text_type))
        new_nodes.extend(nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        links = extract_markdown_links(old_node_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            old_node_text_split = old_node_text.split(f"[{link[0]}]({link[1]})", 1)
            if old_node_text_split[0] != "":
                new_nodes.append(TextNode(old_node_text_split[0], TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            old_node_text = old_node_text_split[1]
        if old_node_text != "":
            new_nodes.append(TextNode(old_node_text, TextType.NORMAL))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        images = extract_markdown_images(old_node_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            old_node_text_split = old_node_text.split(f"![{image[0]}]({image[1]})", 1)
            if old_node_text_split[0] != "":
                new_nodes.append(TextNode(old_node_text_split[0], TextType.NORMAL))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            old_node_text = old_node_text_split[1]
        if old_node_text != "":
            new_nodes.append(TextNode(old_node_text, TextType.NORMAL))
    return new_nodes

