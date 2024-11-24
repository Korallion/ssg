from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode():
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL

    def __eq__(self, otherNode):
        return self.text == otherNode.text and self.text_type == otherNode.text_type and self.url == otherNode.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
