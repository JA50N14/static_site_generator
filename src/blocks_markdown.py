from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split('\n\n')
    cleaned_blocks = []

    for block in markdown_blocks:
        block = block.strip()
        if block == "":
            continue
        cleaned_blocks.append(block)
    return cleaned_blocks


def block_to_block_type(block):
    lines = block.split('\n')
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        if len(lines) > 1:
            if lines[1].startswith("#"):
                raise Exception('Two or more headers in a single block. Split headers by a line.')
        return BlockType.HEADING
    
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    
    if lines[0].startswith("> "):
        return BlockType.QUOTE

    if lines[0].startswith("- "):
        for line in lines:
            if line.startswith("- "):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    if lines[0].startswith("1. "):
        for idx, line in enumerate(lines):
            if line.startswith(f'{idx + 1}. '):
                continue
            else:
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


