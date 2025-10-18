import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_raise(self):
        node = HTMLNode(tag="p")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_eq(self):
        node = HTMLNode(tag="a")
        self.assertEqual(node.props_to_html(), "")

        node = HTMLNode(
            tag="a", props={"href": "https://somewhere.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://somewhere.com" target="_blank"'
        )

        node = HTMLNode(
            tag="a", props={"href": "https://somewhere.com", "target": "_blank"}
        )
        self.assertEqual(
            str(node),
            "HTMLNode(a, None, props={'href': 'https://somewhere.com', 'target': '_blank'})",
        )

        # node = HTMLNode(
        #     tag="a", props={"href": "https://somewhere.com", "target": "_blank"}
        # )
        # node.children = [
        #     HTMLNode(
        #         tag="a", props={"href": "https://somewhere.com", "target": "_blank"}
        #     ),
        #     HTMLNode(
        #         tag="a", props={"href": "https://somewhere.com", "target": "_blank"}
        #     ),
        # ]
        # self.assertEqual(
        #     str(node),
        #     "HTMLNode(a, None, props={'href': 'https://somewhere.com', 'target': '_blank'})",
        # )


if __name__ == "__main__":
    unittest.main()
