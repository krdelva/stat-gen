from textnode import *

def main():
    print("hello world")
    node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(node.__repr__())

main()
