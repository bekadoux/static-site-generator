import unittest

from md_ops import split_nodes_delimiter
from textnode import TextNode, TextType


class TestMarkdownOperations(unittest.TestCase):
    def test_correct_split(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.PLAIN),
            ],
        )

        node = TextNode("This is text with a `code block`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
            ],
        )

        node = TextNode("This is text with a **bold** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.PLAIN),
            ],
        )

        node = TextNode("This is text with a **bold**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
            ],
        )

        node = TextNode("This is *text* **with** an *italic* word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is *text* ", TextType.PLAIN),
                TextNode("with", TextType.BOLD),
                TextNode(" an *italic* word", TextType.PLAIN),
            ],
        )
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.ITALIC),
                TextNode(" ", TextType.PLAIN),
                TextNode("with", TextType.BOLD),
                TextNode(" an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.PLAIN),
            ],
        )
