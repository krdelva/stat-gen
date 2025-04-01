from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from internal_functions import markdown_to_blocks

def main():
    print("hello world")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node.__repr__())

    node_html = HTMLNode(tag="a", value="Google", props={"href": "www.google.com", "example": "aaaaa", "another_one": "bbb"})
    print(node_html.__repr__())
    print(node_html.props_to_html())

    leaf_node = LeafNode("p", "This is a paragraph of text.")
    print("LEAF NODE")
    print(leaf_node.to_html())

    parent_node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],)
    print("PARENT NODE")
    print(parent_node.to_html())

    text_to_html_node = TextNode("This is a text node", TextType.TEXT)
    print("TEXT TO HTML")
    print(text_to_html_node.text_node_to_html_node())

    link_to_html_node = TextNode("This is a link node", TextType.LINK, "www.bob.com")
    print("LINK TO HTML")
    print(link_to_html_node.text_node_to_html_node())

    print("MARKDOWN TEST:")
    markdown_to_blocks("""
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """)

main()
