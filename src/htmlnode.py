from typing import final, override


@final
class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    @override
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self) -> None:
        raise NotImplementedError

    def props_to_html(self):
        if self.props:
            all_props = ""
            for key, value in self.props.items():
                all_props += f'{key}="{value}" '
            return all_props[:-1]
        else:
            return ""
