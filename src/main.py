from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    print("hello world")
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node.__repr__())

    node_html = HTMLNode(tag="a", value="Google", props={"href": "www.google.com", "example": "aaaaa", "another_one": "bbb"})
    print(node_html.__repr__())
    print(node_html.props_to_html())
main()
