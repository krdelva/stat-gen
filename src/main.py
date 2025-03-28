from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

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
main()
