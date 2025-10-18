import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node = TextNode(
            "This is a text node", TextType.BOLD, url="https://someplace.com"
        )
        node2 = TextNode(
            "This is a text node", TextType.BOLD, url="https://someplace.com"
        )
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is some node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

        node = TextNode(
            "This is a text node", TextType.BOLD, url="https://someplace.com"
        )
        node2 = TextNode(
            "This is a text node", TextType.BOLD, url="https://someotherplace.com"
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
