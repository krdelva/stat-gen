import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.aaa.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.aaa.com")
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.aaa.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "www.bbb.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_text_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "www.google.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "www.google.com", "alt": "This is an image node"})

    def test_text_link(self):
        node = TextNode("This is a link node", TextType.LINK, "www.google.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        #node.split_nodes_delimiter("`", TextType.CODE)
        self.assertEqual(node.split_nodes_delimiter("`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("code block", TextType.CODE, None),
                TextNode(" word", TextType.TEXT, None),
            ]
        )

    def test_split_nodes_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        self.assertEqual(node.split_nodes_delimiter("**", TextType.BOLD),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ]
        )


if __name__ == "__main__":
    unittest.main()
