class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        result_html = ''

        if self.props:
            for tag, value in self.props.items():
                result_html += f" {tag}='value'"
        
        return result_html

    def __repr__(self):
        print(f"HTMLNode tag={self.tag} value={self.value} children={self.children} props={props}")
