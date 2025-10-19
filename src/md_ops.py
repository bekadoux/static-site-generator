from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not node.text_type == TextType.PLAIN:
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
