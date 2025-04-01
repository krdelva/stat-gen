import re

from enum import Enum
from textnode import TextType, TextNode

def extract_markdown_images(text):
   return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        # Pattern to match image markdown: ![alt](url)
        pattern = r"(\!\[.*?\]\(.*?\))"
        split_list = re.split(pattern, text)
        for i, part in enumerate(split_list):
            if i % 2 == 0:  # Text part
                if part:  # Only append non-empty text
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:  # Image markdown part
                match = re.match(r"\!\[(.*?)\]\((.*?)\)", part)
                if match:
                    alt = match.group(1)
                    url = match.group(2)
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                else:
                    # Fallback: treat as text if match fails (shouldn't happen with proper split)
                    new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        # Pattern to match link markdown [text](url), but not preceded by !
        pattern = r"((?<!\!)\[.*?\]\(.*?\))"
        split_list = re.split(pattern, text)
        for i, part in enumerate(split_list):
            if i % 2 == 0:  # Text part
                if part:  # Only append non-empty text
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:  # Link markdown part
                match = re.match(r"\[(.*?)\]\((.*?)\)", part)
                if match:
                    link_text = match.group(1)
                    link_url = match.group(2)
                    new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                else:
                    # Fallback: treat as text if match fails
                    new_nodes.append(TextNode(part, TextType.TEXT))
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part:
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                if part:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    return nodes

def markdown_to_blocks(markdown):
    m = markdown.split("\n\n")
    result = []
    t = ""
    for i in m:
        t = i.strip()
        result.append(t)
    i = 0
    for  r in result:
        t = r.replace("  ", "")
        result[i] = t
        i += 1
    return result


class BlockType(Enum):
    PARAGRAPH = ""
    HEADING = "#"
    CODE = "```"
    QUOTE = ">"
    UNORDERED_LIST = "-"
    ORDERED_LIST = "."

def block_to_block_type(block):
    lines = block.split('\n')
    if len(lines) >= 2 and lines[0] == '```' and lines[-1] == '```':
        return BlockType.CODE
    if len(lines) == 1 and re.match(r'^#{1,6} .+', lines[0]):
        return BlockType.HEADING
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    is_ordered = True
    expected_num = 1
    for line in lines:
        match = re.match(r'^(\d+)\. ', line)
        if not match or int(match.group(1)) != expected_num:
            is_ordered = False
            break
        expected_num += 1
    if is_ordered and lines:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
