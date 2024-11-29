import unittest

from leafnode import LeafNode

tag1 = 'tag1'
tag2 = 'tag2'
value1 = 'value1'
value2 = 'value2'
children1 = 'children1'
children2 = 'children2'
props1 = {'test1': 'value'}
props2 = {'test2': 'value2'}

class TestLeafNode(unittest.TestCase):
    def test_eq_empty(self):
        node = LeafNode(tag1, value1, props1) 
        self.assertEqual(node.to_html(), f"<{tag1}{node.props_to_html()}>{value1}</{tag1}>")

if __name__ == "__main__":
    unittest.main()
