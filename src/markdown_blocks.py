from enum import Enum

class BlockType(Enum):
    PARAGRAPH="paragraph"
    HEADING="heading"
    CODE="code"
    QUOTE="quote"
    UNORDERED_LIST="unordered_list"
    ORDERED_LIST="ordered_list"

def block_to_block_type(markdown) -> BlockType:
    lines = markdown.split("\n")
    expected_num = 1
    
    
    if markdown.startswith(("# ","## ","### ","#### ","##### ","###### ")):
        return BlockType.HEADING
    elif markdown[0:4] == "```\n" and markdown.endswith("```"):
        return BlockType.CODE
    elif markdown[0:2] == "> " or markdown[0:1] == ">":
        for line in lines:
            prefix=">"
            if not line.startswith(prefix):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif markdown[0:2] == "- ":
        for line in lines:
            prefix="- "
            if not line.startswith(prefix):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    else:
        for line in lines:
            prefix=f"{expected_num}. "
            if not line.startswith(prefix):
                return BlockType.PARAGRAPH
            expected_num += 1
        return BlockType.ORDERED_LIST
    
    

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_new = []
    for block in blocks:
        block = block.strip()
        if block:
            blocks_new.append(block)
    return blocks_new