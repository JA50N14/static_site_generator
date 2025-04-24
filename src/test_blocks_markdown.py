import unittest
from blocks_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks2(self):
        md = """
This is **bold**
This is another sentence

This is a second paragraph




            
This is a third paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bold**\nThis is another sentence",
                "This is a second paragraph",
                "This is a third paragraph"
            ]
        )


class TestBlockToBlockType(unittest.TestCase):

    def test_code_block(self):
        md = "```\nhere is some code\n```"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.CODE)


    def test_heading_block(self):
        md = "##### this is heading text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_ordered_list(self):
        md = "1. this is an ordered list"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        md = "this is a paragraph"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_ordered_list(self):
        md = '1. line 1\n2. line 2\n3. line 3'
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ORDERED_LIST)