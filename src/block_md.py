from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_md import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"


BLOCK_PATTERNS = {
    re.compile(r"^(#{1,6})\s+(.*)$"): BlockType.HEADING,
    re.compile(r"```[\s\S]*?```"): BlockType.CODE,
    re.compile(r"^(?:>.*(?:\r?\n|$))+?$", flags=re.MULTILINE): BlockType.QUOTE,
    re.compile(r"^(?:- .*(?:\r?\n|$))+$", flags=re.MULTILINE): BlockType.ULIST,
    re.compile(r"^(?:\d+\. .*(?:\r?\n|$))+$", flags=re.MULTILINE): BlockType.OLIST,
}


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [p.strip() for p in markdown.split("\n\n")]
    return [block for block in blocks if block != ""]


def block_to_block_type(block: str) -> BlockType:
    detected_type = BlockType.PARAGRAPH
    for pattern, block_type in BLOCK_PATTERNS.items():
        if pattern.fullmatch(block):
            detected_type = block_type
            break

    if detected_type == BlockType.OLIST:
        expected = 1
        for line in block.splitlines():
            num = int(line[: line.index(".")])
            if expected != num:
                detected_type = BlockType.PARAGRAPH
                break
            expected += 1
    return detected_type


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                nodes.append(quote_to_html_node(block))
            case BlockType.ULIST:
                nodes.append(ul_to_html_node(block))
            case BlockType.OLIST:
                nodes.append(ol_to_html_node(block))
            case _:
                nodes.append(paragraph_to_html_node(block))

    return ParentNode("div", nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def heading_to_html_node(block: str) -> HTMLNode:
    importance = block[: block.index(" ")].count("#")
    if importance not in range(1, 7) or importance + 1 >= len(block):
        raise ValueError(f"invalid heading importance level: {importance}")

    return ParentNode(f"h{importance}", text_to_children(block[importance + 1 :]))


def code_to_html_node(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")

    text_node = TextNode(block[4:-3], TextType.CODE)
    return ParentNode("pre", [text_node_to_html_node(text_node)])


def quote_to_html_node(block: str) -> HTMLNode:
    stripped_lines = []
    for line in block.splitlines():
        if not line.startswith(">"):
            raise ValueError("invalid quote block")

        stripped_lines.append(line.lstrip(">").strip())

    return ParentNode("blockquote", text_to_children(" ".join(stripped_lines)))


def ul_to_html_node(block: str) -> HTMLNode:
    children = []
    for line in block.splitlines():
        if not line.startswith("- "):
            raise ValueError("invalid unordered list block")

        children.append(ParentNode("li", text_to_children(line.lstrip("-").strip())))

    return ParentNode("ul", children)


def ol_to_html_node(block: str) -> HTMLNode:
    children = []
    expected = 1
    for line in block.splitlines():
        try:
            numeration_cutoff = line.index(".")
            num = int(line[:numeration_cutoff])
            if expected != num:
                raise ValueError(
                    f"invalid numeration in ordered list: got {num}, expected {expected}"
                )
            if numeration_cutoff + 2 >= len(line):
                raise ValueError(f"no content in ordered list element {line}")
            expected += 1
        except Exception as e:
            raise Exception(f"invalid ordered list element: {e}")

        children.append(
            ParentNode("li", text_to_children(line[numeration_cutoff + 2 :]))
        )

    return ParentNode("ol", children)


def paragraph_to_html_node(block: str) -> HTMLNode:
    block_text = " ".join(block.splitlines())
    return ParentNode("p", text_to_children(block_text))


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise Exception("title line not found in document")
