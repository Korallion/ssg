from textnode import TextNode
from enums import TextType

def main():
    testNode = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(testNode)

main()
