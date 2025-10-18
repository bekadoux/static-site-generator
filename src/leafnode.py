from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict | None = None,
    ):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        html_render = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_render
