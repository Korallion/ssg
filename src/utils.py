import re
from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", props={"href": text_node.url}, value=text_node.text)
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", props={"src": text_node.url, "alt": text_node.text}, value='')
    else:
        raise Exception("TextNode is not of a valid TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        default_text_type = old_node.text_type
        new_text_parts = old_node.text.split(delimiter)
                
        if len(new_text_parts) == 2:
            raise Exception('Matching closing delimiter not found')
        elif len(new_text_parts) == 1:
            new_nodes.append(old_node)
        else:
            for index, text in enumerate(new_text_parts):
                if index != 1:
                    new_node = TextNode(text, default_text_type)
                    new_nodes.append(new_node)
                else:
                    new_node = TextNode(text, text_type)
                    new_nodes.append(new_node)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"[^\!]\[(.*?)\]\((.*?)\)", text)
    return matches

# "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        node_text = old_node.text
        image_segments = extract_markdown_images(old_node.text)

        if (len(image_segments) == 0):
            new_nodes.append(old_node)
            continue
        
        for index, (text, url) in enumerate(image_segments):
            split_text = node_text.split(f"![{text}]({url})", 1)
            new_nodes.append(TextNode(split_text[0], TextType.NORMAL))
            new_nodes.append(TextNode(text, TextType.IMAGES, url))

            if len(split_text) == 2:
                if split_text[1] != "":
                    if index == len(image_segments) - 1:
                        new_nodes.append(TextNode(split_text[1], TextType.NORMAL))
                    else:
                        node_text = split_text[1]
                
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        node_text = old_node.text
        image_segments = extract_markdown_links(old_node.text)

        if (len(image_segments) == 0):
            new_nodes.append(old_node)
            continue
        
        for index, (text, url) in enumerate(image_segments):
            split_text = node_text.split(f"[{text}]({url})", 1)
            new_nodes.append(TextNode(split_text[0], TextType.NORMAL))
            new_nodes.append(TextNode(text, TextType.LINKS, url))

            if len(split_text) == 2:
                if split_text[1] != "":
                    if index == len(image_segments) - 1:
                        new_nodes.append(TextNode(split_text[1], TextType.NORMAL))
                    else:
                        node_text = split_text[1]
    
    return new_nodes
