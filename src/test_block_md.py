import unittest

from block_md import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


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

    def test_markdown_to_html_node(self):
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

        md = """
# header 1

### header three okay

okay let's type something
should work fine
hehe

> quote here
> this is quote
>this is quote too

- milk
- sugar
- candies

1. papapapapa
2. bababababa
3. yeah

```
gotta throw some `code` here too
should do nothing about it
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>header 1</h1><h3>header three okay</h3><p>okay let's type something should work fine hehe</p><blockquote>quote here this is quote this is quote too</blockquote><ul><li>milk</li><li>sugar</li><li>candies</li></ul><ol><li>papapapapa</li><li>bababababa</li><li>yeah</li></ol><pre><code>gotta throw some `code` here too\nshould do nothing about it\n</code></pre></div>",
        )

    def test_extract_title(self):
        md = """
# heading here

some other paragraph

- list
- milk
- candies
        """
        title = extract_title(md)
        self.assertEqual(title, "heading here")

        md = """
some other paragraph

### less important stuff

#   puppies and unicorns  

- list
- milk
- candies
        """
        title = extract_title(md)
        self.assertEqual(title, "puppies and unicorns")

        md = """
## not a heading
- list
- milk
- candies
        """
        with self.assertRaises(Exception):
            extract_title(md)
