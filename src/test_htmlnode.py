import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_none(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "Click me!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        parent_node = ParentNode("", [child_node], None)
        self.assertRaises(
            ValueError,
            parent_node.to_html,
        )

        parent_node = ParentNode("div", [], None)
        self.assertRaises(
            ValueError,
            parent_node.to_html,
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        children = [
            LeafNode("a", "Click me!", {"href": "https://www.google.com"}),
            LeafNode("a", "Don't click me!", {"href": "https://www.evilgoogle.com"}),
            LeafNode(None, "something something", None),
            ParentNode(
                "a",
                [LeafNode("a", "Click me!", {"href": "https://www.google.com"})],
                {"href": "https://www.google.com"},
            ),
        ]
        node = ParentNode("div", children, None)
        self.assertEqual(
            node.to_html(),
            """<div><a href="https://www.google.com">Click me!</a><a href="https://www.evilgoogle.com">Don't click me!</a>something something<a href="https://www.google.com"><a href="https://www.google.com">Click me!</a></a></div>""",
        )


if __name__ == "__main__":
    unittest.main()
