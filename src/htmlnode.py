from typing import Self, Sequence


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence[Self] | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Child classes should override this
        raise NotImplementedError("this method is not implemented")

    def props_to_html(self):
        final_str = ""
        if self.props is None:
            return final_str

        for prop, value in self.props.items():
            final_str += f' {prop}="{value}"'
        return final_str

    def __repr__(self) -> str:
        repr_str = f"HTMLNode({self.tag}, {self.value}, props={self.props})"
        if self.children is not None:
            repr_str += (
                f"\nChildren:\n{'\n'.join('  ' + str(node) for node in self.children)}"
            )

        return repr_str


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: Sequence[HTMLNode],
        props: dict | None = None,
    ):
        super().__init__(tag, None, props=props)
        self.children = children

    def to_html(self):
        if self.tag is not None and len(self.tag) == 0:
            raise ValueError(
                "attribute 'tag' cannot be empty for instances of ParentNode"
            )
        if len(self.children) == 0:
            raise ValueError(
                "attribute 'children' cannot be empty for instances of ParentNode"
            )

        children_html = "".join(child.to_html() for child in self.children)
        html_render = f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        return html_render

    def __repr__(self) -> str:
        repr_str = f"ParentNode({self.tag}, {self.value}, props={self.props})"
        repr_str += (
            f"\nChildren:\n{'\n'.join('  ' + str(node) for node in self.children)}"
        )

        return repr_str


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict | None = None,
    ):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value

        html_render = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return html_render

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, props={self.props})"
