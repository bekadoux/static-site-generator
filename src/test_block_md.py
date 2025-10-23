import unittest

from block_md import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockMarkdownOperations(unittest.TestCase):
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

        # Tests for input with excessive newlines
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

    def test_block_to_block_type(self):
        block = "paragraph of text"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "```code block here```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = ">quote\n>other quote\n> some other quote\n"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "- milk\n- honey\n- cookies"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

        block = "- milk\n-honey\n- cookies"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

        block = "1. one\n2. two\n5. five"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        block = "1. one\n2. two\n5 five"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
