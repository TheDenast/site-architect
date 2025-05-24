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
