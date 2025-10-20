import re

from textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\]]*?)\]\(([^)]+?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!\!)\[([^\]]*?)\]\(([^)]+?)\)"
    return re.findall(pattern, text)


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


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        split_sections = []
        new_nodes_extension = []
        for i in range(len(matches)):
            alt, url = matches[i]
            full_pattern_match = f"![{alt}]({url})"

            if len(split_sections) > 0:
                split_sections = split_sections[-1].split(
                    full_pattern_match, maxsplit=1
                )
            else:
                split_sections = node.text.split(full_pattern_match, maxsplit=1)

            new_nodes_extension.append(TextNode(split_sections[0], TextType.PLAIN))
            new_nodes_extension.append(TextNode(alt, TextType.IMAGE, url))
            if i == len(matches) - 1:
                if split_sections[-1] != "":
                    new_nodes_extension.append(
                        TextNode(split_sections[-1], TextType.PLAIN)
                    )

        new_nodes.extend(new_nodes_extension)
    return new_nodes


def split_nodes_link(old_nodes):
    pass


if __name__ == "__main__":
    node = TextNode(
        "This is text with three ![image](https://i.imgur.com/zjjcJKZ.png) images ![image](https://i.imgur.com/3elNhQu.png) yes ![image](https://i.imgur.com/3elNhQu.png)",
        TextType.PLAIN,
    )
    new_nodes = split_nodes_image([node])
    print(new_nodes)
