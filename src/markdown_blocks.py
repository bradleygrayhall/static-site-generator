from enum import Enum

from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from delimiter import text_to_textnodes
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
    
def text_to_children(text):
    textnode_list = []
    textNodes = text_to_textnodes(text)
    for text_node in textNodes:
        textnode_list.append(text_node_to_html_node(text_node))
    return textnode_list
       
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_new = []
    for block in blocks:
        block = block.strip()
        if block:
            blocks_new.append(block)
    return blocks_new

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parents = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            text = block[level + 1:]
            children = text_to_children(text)
            parent = ParentNode(f"h{level}", children)
            parents.append(parent)
        elif block_type == BlockType.CODE:
            block = block[4:-3]
            raw_node = TextNode(block,TextType.TEXT)
            child = text_node_to_html_node(raw_node)
            code = ParentNode("code",[child])
            parent = ParentNode("pre", [code])
            parents.append(parent)
        elif block_type == BlockType.PARAGRAPH:
            textnodes = text_to_children(block)
            parent = ParentNode("p",textnodes)
            parents.append(parent)
        elif block_type == BlockType.QUOTE:
            block = block.split("\n")
            li_nodes = []
            for line in block:
                li_nodes.append(line.lstrip("> "))
            cleaned_block = "\n".join(li_nodes)
            parents.append(ParentNode("blockquote",text_to_children(cleaned_block)))
        elif block_type == BlockType.UNORDERED_LIST:
            block = block.split("\n")
            li_nodes = []
            for line in block:
                li_nodes.append(ParentNode("li",text_to_children(line[2:])))
            parent = ParentNode("ul",li_nodes)
            parents.append(parent)
        else:
            block = block.split("\n")
            li_nodes = []
            for line in block:
                li_nodes.append(ParentNode("li",text_to_children(line.split(". ",1)[1])))
            parent = ParentNode("ol",li_nodes)
            parents.append(parent)
    return ParentNode("div",parents)