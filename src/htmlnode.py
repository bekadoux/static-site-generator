from typing import Self


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[Self] | None = None,
        props: dict | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        # Child classes should override this
        raise NotImplementedError

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
