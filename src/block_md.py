from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered list"
    OLIST = "ordered list"


BLOCK_PATTERNS = {
    re.compile(r"^(#{1,6})\s+(.*)$"): BlockType.HEADING,
    re.compile(r"```[\s\S]*?```"): BlockType.CODE,
    re.compile(r"^(?:>.*(?:\r?\n|$))+?$", flags=re.MULTILINE): BlockType.QUOTE,
    re.compile(r"^(?:- .*(?:\r?\n|$))+$", flags=re.MULTILINE): BlockType.ULIST,
    re.compile(r"^(?:\d+\. .*(?:\r?\n|$))+$", flags=re.MULTILINE): BlockType.OLIST,
}


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [p.strip() for p in markdown.split("\n\n")]
    return [block for block in blocks if block != ""]


def block_to_block_type(block: str) -> BlockType:
    detected_type = BlockType.PARAGRAPH
    for pattern, block_type in BLOCK_PATTERNS.items():
        if pattern.fullmatch(block):
            detected_type = block_type
            break

    if detected_type == BlockType.OLIST:
        expected = 1
        for line in block.splitlines():
            num = int(line[: line.index(".")])
            if expected != num:
                detected_type = BlockType.PARAGRAPH
                break
            expected += 1
    return detected_type
