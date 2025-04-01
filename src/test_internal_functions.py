import unittest

from internal_functions import (
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)
from textnode import TextType, TextNode


class TestTextNode(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) woowow [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    # NEW Tests
    def test_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_plain_text(self):
        text = "Just plain text"
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_only_bold(self):
        text = "**Bold text**"
        expected = [TextNode("Bold text", TextType.BOLD)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_italics(self):
        text = "_Italic1_ and _Italic2_"
        expected = [
            TextNode("Italic1", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("Italic2", TextType.ITALIC),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_starts_with_image(self):
        text = "![image](url) text"
        expected = [
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_ends_with_link(self):
        text = "text [link](url)"
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    ######
    # Tests for block to block type
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Tiny Heading"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("#NoSpace"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Too Many"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("# Heading\nMore"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```\nline1\nline2\n```"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("```\ncode"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("code\n```"), BlockType.CODE)

    def test_quote(self):
        self.assertEqual(block_to_block_type("> Quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type("> Quote\nNot a quote"), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("- Item\nItem"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("-Item"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. First\n2. Second"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1. First\n3. Third"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("2. Starts high"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1.First"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Simple text"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Line 1\nLine 2"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertNotEqual(block_to_block_type("# Heading"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
