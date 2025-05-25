from enum import Enum
import re


class BlockType(Enum):
    TEXT = 1
    HEADER = 2
    CODE = 3
    BLOCKQUOTE = 4
    LIST = 5
    NUMLIST = 6


def markdown_to_blocks(markdown: str) -> list[str]:
    # Split by double newlines
    raw_blocks = markdown.split("\n\n")

    # Filter out empty blocks and strip whitespace
    blocks: list[str] = []
    for b in raw_blocks:
        cleaned = b.strip()
        if cleaned:
            blocks.append(cleaned)

    return blocks


def block_to_blocktype(block: str) -> BlockType:
    lines = block.split("\n")

    # Heading: starts with 1-6 # followed by space
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADER

    # Code block: starts AND ends with ```
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote: EVERY line starts with >
    if all(line.startswith(">") for line in lines):
        return BlockType.BLOCKQUOTE

    # Unordered list: EVERY line starts with "- "
    if all(re.match(r"^-\s", line) for line in lines):
        return BlockType.LIST

    # Ordered list: EVERY line starts with number. space, incrementing from 1
    if all(re.match(rf"^{i + 1}\.\s", line) for i, line in enumerate(lines)):
        return BlockType.NUMLIST

    return BlockType.TEXT
