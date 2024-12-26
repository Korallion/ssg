import unittest

from parentnode import ParentNode
from  leafnode import LeafNode

tag1 = 'tag1'
tag2 = 'tag2'
value1 = 'value1'
value2 = 'value2'
props1 = {'test1': 'value'}
props2 = {'test2': 'value2'}
children1 = LeafNode(tag=tag1, value=value1, props=props1)
children2 = LeafNode(tag=tag2, value=value2, props=props2)


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_simple_children(self):
        parentNode = ParentNode(tag1, [children1, children2], props1)
        children_html = f"{children1.to_html()}{children2.to_html()}"
        self.assertEqual(parentNode.to_html(), f"<{tag1}{parentNode.props_to_html()}>{children_html}</{tag1}>")

    def test_to_html_with_complex_children(self):
        insideParentNode = ParentNode(tag2,[children1, children2], props2)
        parentNode = ParentNode(tag1, [insideParentNode], props1)
        children_html = insideParentNode.to_html()
        self.assertEqual(parentNode.to_html(), f"<{tag1}{parentNode.props_to_html()}>{children_html}</{tag1}>")

if __name__ == "__main__":
    unittest.main()
