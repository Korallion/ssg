import unittest

from blocks import markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, TextType

class TestUtils(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test_text = '# title\n\nparagraph\n\n\n- list\n- list\n\n\n\n'
        result = markdown_to_blocks(test_text)
        expected_result = [
            '# title',
            'paragraph',
            '- list\n- list'
        ]
        self.assertEqual(result, expected_result)

    def text_block_to_block_type(self):
        test_paragraph = 'blah blah blah\nblah blah blah'
        test_heading = '# blah'
        test_code = '```blah blah\nblah blah```'
        test_quote = '> blah\n>blah\n>blah?'
        test_u_list = '-blah\n*blah\n-blah'
        test_o_list = '1. blah\n2. blah\n3. blah'

        self.assertEqual(block_to_block_type(test_paragraph), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(test_heading), BlockType.HEADING)
        self.assertEqual(block_to_block_type(test_code), BlockType.CODE)
        self.assertEqual(block_to_block_type(test_quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(test_u_list), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(test_o_list), BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
