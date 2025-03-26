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

if __name__ == "__main__":
    unittest.main()
