import unittest

from htmlnode import HTMLNode

tag1 = 'tag1'
tag2 = 'tag2'
value1 = 'value1'
value2 = 'value2'
children1 = 'children1'
children2 = 'children2'
props1 = {'test1': 'value'}
props2 = {'test2': 'value2'}

class TestHTMLNode(unittest.TestCase):
    def test_eq_empty(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_eq_all_values(self):
        node = HTMLNode(tag1, value1, children1, props1)
        node2 = HTMLNode(tag1, value1, children1, props1)
        self.assertEqual(node.props_to_html(), node2.props_to_html())

    def test_non_eq_props(self):
        node = HTMLNode(tag1, value1, children1, props1)
        node2 = HTMLNode(tag1, value1, children1, props2)
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())

if __name__ == "__main__":
    unittest.main()
