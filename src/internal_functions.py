import re
import os

from enum import Enum
from textnode import TextType, TextNode
from htmlnode import ParentNode, LeafNode

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

##########

def text_to_children(text):
    # Convert a string with inline markdown to a list of HTMLNode objects.
    text_nodes = text_to_textnodes(text)
    return [tn.text_node_to_html_node() for tn in text_nodes]  # Returns LeafNode instances

def paragraph_to_html_node(block):
    # Convert a markdown paragraph to a ParentNode with a <p> tag.
    # Replace newline characters with a single space
    block = block.replace('\n', ' ')
    # Process the text into child nodes (e.g., handling bold, italic, code)
    children = text_to_children(block)
    # Return a ParentNode with the <p> tag and its children
    return ParentNode("p", children)

def heading_to_html_node(block):
    # Convert a markdown heading to a ParentNode with an <h1> to <h6> tag.
    level = block.count('#', 0, block.find(' '))
    if level < 1 or level + 1 >= len(block):
        raise ValueError("Invalid heading format")
    text = block[level + 1:].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    # Convert a markdown code block to a ParentNode with <pre><code> tags.
    lines = block.split('\n')
    if len(lines) < 2 or lines[0].strip() != '```' or lines[-1].strip() != '```':
        raise ValueError("Invalid code block format")
    code_lines = lines[1:-1]
    code_text = "\n".join(code_lines) + "\n"  # Add trailing newline
    text_node = LeafNode(None, code_text)
    code_node = ParentNode("code", [text_node])
    return ParentNode("pre", [code_node])

def quote_to_html_node(block):
    lines = block.split('\n')
    quote_lines = [line[2:] for line in lines if line.startswith('> ')]
    quote_text = " ".join(quote_lines).strip()  # Join with spaces instead of newlines
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)   # No <p> tag

def unordered_list_to_html_node(block):
    # Convert a markdown unordered list to a ParentNode with a <ul> tag.
    lines = block.split('\n')
    list_items = []
    for line in lines:
        if not line.startswith('- '):
            raise ValueError("Invalid unordered list item")
        item_text = line[2:]
        children = text_to_children(item_text)
        li_node = ParentNode("li", children)
        list_items.append(li_node)
    return ParentNode("ul", list_items)

def ordered_list_to_html_node(block):
    # Convert a markdown ordered list to a ParentNode with an <ol> tag.
    lines = block.split('\n')
    list_items = []
    for line in lines:
        if not re.match(r'^\d+\. ', line):
            raise ValueError("Invalid ordered list item")
        item_text = re.sub(r'^\d+\. ', '', line)
        children = text_to_children(item_text)
        li_node = ParentNode("li", children)
        list_items.append(li_node)
    return ParentNode("ol", list_items)

def markdown_to_html_node(markdown):
    # Convert a markdown document to a single ParentNode with nested elements.
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html_node(block)
        else:
            raise ValueError(f"Unknown block type: {block_type}")
        block_nodes.append(node)
    return ParentNode("div", block_nodes)

#############

def extract_title(markdown):
    match = re.search(r'^#\s(.+)', markdown, re.MULTILINE)
    if match:
        return match.group(1).strip()
    raise ValueError("No h1 header found in markdown")


def generate_page(from_path, template_path, dest_path, base_path="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown and template files
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    # Extract title
    title = extract_title(markdown)

    # Replace placeholders
    final_html = template.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    # Adjust URLs with base_path
    final_html = final_html.replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')

    # Create destination directory if needed
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the HTML file
    with open(dest_path, 'w') as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path="/"):
    # Recursively generate HTML pages from markdown files in the content directory.
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                from_path = os.path.join(root, file)
                rel_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.splitext(rel_path)[0] + '.html')
                generate_page(from_path, template_path, dest_path, base_path)
