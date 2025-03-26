import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="a", value="Google", props={"href": "www.google.com"})
        node2 = HTMLNode(tag="a", value="Google", props={"href": "www.google.com"})
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = HTMLNode(tag="a", value="Google", props={"href": "www.google.com"})
        node2 = HTMLNode(tag="a", props={"href": "www.google.com"})
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
