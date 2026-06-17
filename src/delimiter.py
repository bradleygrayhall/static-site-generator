from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            nodes.append(old_node)
        else:
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise Exception("invalid markdown syntax")
            else:
                for i in range(len(sections)):
                    if i % 2 == 1 and sections[i] != "":
                        nodes.append(TextNode(sections[i],text_type))
                    elif i % 2 == 0 and sections[i] != "":
                        nodes.append(TextNode(sections[i],TextType.TEXT))
                            
    return nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            node_images = extract_markdown_images(node.text)
            if not node_images:
                split_nodes.append(node)
            else:
                remaining_text = node.text
                for images in node_images:
                    sections = remaining_text.split(f"![{images[0]}]({images[1]})",1)
                    if sections[0]:
                        split_nodes.append(TextNode(sections[0],TextType.TEXT))
                    split_nodes.append(TextNode(images[0],TextType.IMAGE,images[1]))
                    remaining_text = sections[1]
                if remaining_text:
                    split_nodes.append(TextNode(remaining_text,TextType.TEXT))
        else:
            split_nodes.append(node)
    return split_nodes

                
def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type is TextType.TEXT:
            node_links = extract_markdown_links(node.text)
            if not node_links:
                split_nodes.append(node)
            else:
                remaining_text = node.text
                for links in node_links:
                    sections = remaining_text.split(f"[{links[0]}]({links[1]})", 1)
                    if sections[0]:
                        split_nodes.append(TextNode(sections[0],TextType.TEXT))
                    split_nodes.append(TextNode(links[0],TextType.LINK,links[1]))
                    remaining_text = sections[1]
                if remaining_text:
                    split_nodes.append(TextNode(remaining_text,TextType.TEXT))
        else:
            split_nodes.append(node)
    return split_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes,"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_",TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes