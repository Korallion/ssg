import unittest

from htmlnode import HTMLNode
from utils import markdown_to_html_node, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes, extract_title
from textnode import TextNode
from enums import TextType

class TestUtils(unittest.TestCase):
    def test_text_node_conversion_text(self):
        text_node = TextNode(text="test", text_type=TextType.NORMAL)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), f"test")

    def test_text_node_conversion_bold(self):
        text_node = TextNode(text="test", text_type=TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), f"<b>test</b>")

    def test_split_delimiter(self):
        text_node = TextNode(text="test and *bold* and *what* and who", text_type=TextType.NORMAL)
        split_nodes = split_nodes_delimiter([text_node], '*', TextType.BOLD)

        self.assertEqual(split_nodes[0], TextNode("test and ", TextType.NORMAL))
        self.assertEqual(split_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(split_nodes[2], TextNode(" and ", TextType.NORMAL))
        self.assertEqual(split_nodes[3], TextNode("what", TextType.BOLD))
        self.assertEqual(split_nodes[4], TextNode(" and who", TextType.NORMAL))


    def test_extract_markdown_images(self):
        test_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(test_text)
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected_result)

    def test_extract_markdown_links(self):
        test_text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_links(test_text)
        expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(result, expected_result)

    def test_split_nodes_image(self):
        test_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_text_node = TextNode(test_text, TextType.NORMAL)
        result = split_nodes_image([test_text_node])
        expected_result = [
            TextNode("This is text with a ", TextType.NORMAL), 
            TextNode("rick roll", TextType.IMAGES, 'https://i.imgur.com/aKaOqIh.gif'),   
            TextNode(" and ", TextType.NORMAL), 
            TextNode("obi wan", TextType.IMAGES, 'https://i.imgur.com/fJRm4Vk.jpeg')
            ]
        self.assertEqual(result, expected_result)

    def test_split_nodes_link(self):
        test_text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_text_node = TextNode(test_text, TextType.NORMAL)
        result = split_nodes_link([test_text_node])
        expected_result = [
            TextNode("This is text with a ", TextType.NORMAL), 
            TextNode("rick roll", TextType.LINKS, 'https://i.imgur.com/aKaOqIh.gif'),   
            TextNode(" and ", TextType.NORMAL), 
            TextNode("obi wan", TextType.LINKS, 'https://i.imgur.com/fJRm4Vk.jpeg')
            ]
        self.assertEqual(result, expected_result)

    def test_text_to_text_nodes(self):
        test_text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_text_nodes(test_text)
        expected_result = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD), 
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGES, 'https://i.imgur.com/fJRm4Vk.jpeg'),   
            TextNode(" and a ", TextType.NORMAL), 
            TextNode("link", TextType.LINKS, 'https://boot.dev')
        ]
        self.assertEqual(result, expected_result)

    def test_markdown_to_html_node(self):
        test_text = "paragraph\n\n# heading 1\n\n## heading 2\n\n```code\ncode```\n\n> quote\n>\n> quote\n\n* ulist\n* ulist\n\n1. olist\n2. olist\n"

        result = markdown_to_html_node(test_text)

        expected_children = [
            HTMLNode('p', 'paragraph'),
            HTMLNode('h1', 'heading 1'),
            HTMLNode('h2', 'heading 2'),
            HTMLNode('code', 'code\ncode'),
            HTMLNode('blockquote', 'quote\n\nquote'),
            HTMLNode('ul', None, [HTMLNode('li', 'ulist'), HTMLNode('li', 'ulist')]),
            HTMLNode('ol', None, [HTMLNode('li', 'olist'), HTMLNode('li', 'olist')]),
        ]
        expected_result = HTMLNode('html', None, expected_children)
        self.assertEqual(result.tag, expected_result.tag)
        self.assertEqual(result.value, expected_result.value)

        def assert_child_equality(res, exp_res):
            self.assertEqual(res.tag, exp_res.tag)
            self.assertEqual(res.value, exp_res.value)

            if res.children != None:
                for index, child in enumerate(res.children):
                    assert_child_equality(child, exp_res.children[index])

        assert_child_equality(result, expected_result)

    def test_markdown_to_html_node(self):
        mkdn_start_heading = "# heading 1\n\n## heading 2\n\n```code\ncode```\n\n> quote\n>\n> quote\n\n* ulist\n* ulist\n\n1. olist\n2. olist\n"
        mkdn_no_heading = "paragraph\n\n# heading 1\n\n```code\ncode```\n\n> quote\n>\n> quote\n\n* ulist\n* ulist\n\n1. olist\n2. olist\n"

        expected_result = 'heading 1'

        result = extract_title(mkdn_start_heading)
        self.assertEqual(result, expected_result)
        self.assertRaises(Exception, extract_title, mkdn_no_heading)

if __name__ == "__main__":
    unittest.main()
