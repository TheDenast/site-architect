from typing import final, override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.value: str | None = value
        self.tag: str | None = tag
        self.children: list["HTMLNode"] | None = children
        self.props: dict[str, str] | None = props

    @override
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            all_props = ""
            for key, value in self.props.items():
                all_props += f'{key}="{value}" '
            return all_props[:-1]
        else:
            return ""


@final
class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: dict[str, str] | None = None,
    ):
        if value is None:
            raise ValueError("All leaf nodes must have a value")
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if self.tag is None and self.value is not None:
            return self.value
        elif self.tag == "img":  # Add this
            props_str = " " + self.props_to_html() if self.props_to_html() else ""
            return f"<{self.tag}{props_str}>"
        else:
            props_str = " " + self.props_to_html() if self.props_to_html() else ""
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"


@final
class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes need to be tagged")
        if self.children is None:
            raise ValueError("All parent nodes need to have children")

        props_str = " " + self.props_to_html() if self.props_to_html() else ""
        html_str = f"<{self.tag}{props_str}>"
        for child in self.children:
            html_str += child.to_html()
        html_str += f"</{self.tag}>"
        return html_str
