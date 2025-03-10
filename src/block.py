from enum import Enum
import re
from inline import text_to_textnodes, text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = []
    markdown_split = markdown.split("\n\n")
    for markdown_block in markdown_split:
        if markdown_block == "":
            continue
        blocks.append(markdown_block.strip())
    return blocks

def block_to_block_type(block):
    if bool(re.match(r"^#{1,6}\s.+$", block)):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    splitted = block.split("\n")
    if splitted[0].startswith("> "):
        count = len(list(filter(lambda split: split.startswith("> "), splitted)))
        if count == len(splitted):
            return BlockType.QUOTE
    
    if splitted[0].startswith("- "):
        count = len(list(filter(lambda split: split.startswith("- "), splitted)))
        if count == len(splitted):
            return BlockType.UNORDERED_LIST
    
    if re.search(r"^\d{1,9}.\s", splitted[0]):
        count = len(list(filter(lambda split: re.search(r"^\d{1,9}.\s", split), splitted)))
        if count == len(splitted):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            children = []
            splitted = block.split("\n")
            for split in splitted:
                children.extend(text_to_children(split))
            return ParentNode("p", children)
        case BlockType.CODE:
            block = block.lstrip("```\n").rstrip("```")
            return ParentNode("pre", [text_node_to_html_node(TextNode(block, TextType.CODE))])
        case BlockType.HEADING:
            block_slice = block[block.index(" ") + 1:]
            heading = len(block) - len(block_slice) - 1
            return LeafNode("h" + heading, block_slice) 
        case BlockType.QUOTE:
            children = []
            splitted = block.split("\n")
            for split in splitted:
                split = split.lstrip("> ")
                children.extend(text_to_children(split))
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            li = []
            splitted = block.split("\n")
            for split in splitted:
                split = split.lstrip("- ")
                li.append(ParentNode("li", text_to_children(split)))
            return ParentNode("ul", li)
        case BlockType.ORDERED_LIST:
            li = []
            splitted = block.split("\n")
            for split in splitted:
                split = split[split.index(" ") + 1:]
                li.append(ParentNode("li", text_to_children(split)))
            return ParentNode("ol", li)
        case _:
            raise ValueError(f"invalid BlockType {block_type.value}")


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node)) 
    return children

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(block_to_html_node(block, block_type))

    return ParentNode("div", children)
