import re

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
