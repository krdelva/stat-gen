
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, obj):
        return (
            self.tag == obj.tag and
            self.value == obj.value and
            self.children == obj.children and
            self.props == obj.props
        )

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props == None:
            #return None
            return ""
        s = ""
        for p in self.props:
            s += f' {p}="{self.props[p]}"'

        return s


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value == None:
            raise ValueError()
        elif self.tag == None:
            return f"{self.value}"
        #elif self.props == None:
            #return f"<{self.tag}>{self.value}</{self.tag}>"
        p = self.props_to_html()
        return f"<{self.tag}{p}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required for ParentNode")
        if self.children is None:
            raise ValueError("Children are required for ParentNode")
        children_html = "".join(child.to_html() for child in self.children)
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        return opening_tag + children_html + closing_tag
