from htmlnode import HTMLNode
import functools

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode has invalid tag")
        if self.children == None:
            raise ValueError("ParentNode must have children")

        start_html = f"<{self.tag}{self.props_to_html()}>"
        end_html = f"</{self.tag}>"

        children_html = ''

        for child in self.children:
            children_html += child.to_html()

        return start_html + children_html + end_html
