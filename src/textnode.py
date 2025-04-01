from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "normal"
    BOLD = "b"
    ITALIC = "i"
    CODE = "code"
    LINK = "a"
    IMAGE = "img"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, obj):
        return (
            self.text == obj.text and
            self.text_type == obj.text_type and
            self.url == obj.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(self):
        if self.text_type not in TextType:
            raise Exception("not a valid TextType")
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, self.text)
            case TextType.BOLD | TextType.ITALIC | TextType.CODE:
                return LeafNode(self.text_type.value, self.text)
            case TextType.LINK:
                return  LeafNode(self.text_type.value, self.text, {"href": self.url})
            case TextType.IMAGE:
                return  LeafNode(self.text_type.value, "", {"src": self.url, "alt": self.text})
            case _:
                raise ValueError("no matching case")
