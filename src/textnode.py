from enum import Enum
from typing import override


class TextType(Enum):
    NORMAL = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

        if self.text_type == TextType.LINK and self.url is None:
            raise ValueError(f"{TextType.LINK} requires url to be not None!")

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    @override
    def __repr__(self):
        if self.text_type is not TextType.LINK:
            return f"TextNode({self.text}, {self.text_type})"
        else:
            return f"TextNode({self.text}, {self.text_type}, {self.url})"
