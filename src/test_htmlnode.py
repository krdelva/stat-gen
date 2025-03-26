import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="a", value="Google", props={"href": "www.google.com"})
        node2 = HTMLNode(tag="a", value="Google", props={"href": "www.google.com"})
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = HTMLNode(tag="a", value="Google", props={"href": "www.google.com"})
        node2 = HTMLNode(tag="a", props={"href": "www.google.com"})
        self.assertNotEqual(node, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
if __name__ == "__main__":
    unittest.main()
