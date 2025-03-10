import unittest

from block import (
        BlockType,
        markdown_to_blocks, 
        block_to_block_type,
        markdown_to_html_node
)

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, expected)

    def test_markdown_to_blocks_two(self):
        md = """
This is **bolded** paragraph with
_italic_ row

- This is a list
- with items 

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph with\n_italic_ row",
            "- This is a list\n- with items",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        blocks = markdown_to_blocks(md)
        self.assertListEqual(blocks, expected)

    def test_block_to_block_type_heading(self):
        md_heading1 = "# Heading1"
        md_heading2 = "## Heading2"
        md_heading6 = "###### Heading 6"
        md_headingFail = "####### Heading Fail"
        
        self.assertEqual(block_to_block_type(md_heading1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md_heading2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md_heading6), BlockType.HEADING)
        self.assertEqual(block_to_block_type(md_headingFail), BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        md_code = "```def main():\n\tprint('Hello World!')```"
        md_codeFail = "```def main():\n\tprint('Hello World!')"

        self.assertEqual(block_to_block_type(md_code), BlockType.CODE)
        self.assertEqual(block_to_block_type(md_codeFail), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        md_quote = "> first line\n> second line\n> third line"
        md_quoteFail = "> first line\n> second line\n third line"

        self.assertEqual(block_to_block_type(md_quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(md_quoteFail), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_list(self):
        md_ord_list = "1. first\n2. second\n3. third"
        md_uord_list = "- firs\n- second\n- third"
        md_ord_listFail = "firs\n2. second\n3. third"
        md_uord_listFail = "- first\n second\n- third"

        self.assertEqual(block_to_block_type(md_ord_list), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(md_uord_list), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(md_ord_listFail), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(md_uord_listFail), BlockType.PARAGRAPH)
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph 
text in a p 
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
