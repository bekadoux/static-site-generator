import re

from textnode import TextNode, TextType

IMAGE_PATTERN = r"!\[([^\]]*?)\]\(([^)]+?)\)"
LINK_PATTERN = r"(?<!\!)\[([^\]]*?)\]\(([^)]+?)\)"


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(IMAGE_PATTERN, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(LINK_PATTERN, text)


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        split_sections = node.text.split(delimiter)
        if len(split_sections) % 2 == 0:
            raise Exception("invalid markdown, could not find closing delimiter")

        for i in range(len(split_sections)):
            if split_sections[i] == "":
                continue

            new_node_text_type = TextType.PLAIN
            if i % 2 != 0:
                new_node_text_type = text_type
            new_nodes.append(TextNode(split_sections[i], new_node_text_type))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)

        # Pattern here is non-capturing
        pattern_split = re.split(r"!\[(?:[^\]]*?)\]\((?:[^)]+?)\)", node.text)
        match_index = 0

        for node_text in pattern_split:
            if node_text != "":
                new_nodes.append(TextNode(node_text, TextType.PLAIN))
            if match_index < len(matches):
                alt, url = matches[match_index]
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                match_index += 1
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)

        # Pattern here is non-capturing
        pattern_split = re.split(r"(?<!\!)\[(?:[^\]]*?)\]\((?:[^)]+?)\)", node.text)
        match_index = 0

        for node_text in pattern_split:
            if node_text != "":
                new_nodes.append(TextNode(node_text, TextType.PLAIN))
            if match_index < len(matches):
                anchor, url = matches[match_index]
                new_nodes.append(TextNode(anchor, TextType.LINK, url))
                match_index += 1
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    delimiters = [
        ("**", TextType.BOLD),
        ("*", TextType.ITALIC),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
    ]

    nodes = [TextNode(text, TextType.PLAIN)]
    for delim, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delim, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
