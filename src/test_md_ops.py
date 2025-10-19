import unittest

from md_ops import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images(
            "This is text with two ![image 1](https://i.imgur.com/zjjcJKZ.png) pics: ![image 2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image 1", "https://i.imgur.com/zjjcJKZ.png"),
                ("image 2", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

        matches = extract_markdown_images("This is text with no images")
        self.assertListEqual(
            [],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")],
            matches,
        )

        matches = extract_markdown_links(
            "This is text with two links [link](https://example.com) [link 2](https://example.com)"
        )
        self.assertListEqual(
            [
                ("link", "https://example.com"),
                ("link 2", "https://example.com"),
            ],
            matches,
        )

        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual(
            [],
            matches,
        )
