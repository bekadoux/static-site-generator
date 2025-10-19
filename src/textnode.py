from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value) -> bool:
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node.text_type, TextType):
        raise ValueError("provided text_type is not known")

    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            url = text_node.url if text_node.url else ""
            return LeafNode("a", text_node.text, props={"href": url})
        case TextType.IMAGE:
            src = text_node.url if text_node.url else ""
            return LeafNode("img", "", props={"src": src, "alt": text_node.text})
