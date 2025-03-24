import re
from blocks import block_to_block_type, get_heading_number, markdown_to_blocks
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode
from enums import TextType, BlockType
from os import makedirs, path, listdir

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode(tag="a", props={"href": text_node.url}, value=text_node.text)
    elif text_node.text_type == TextType.IMAGES:
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
                if index % 2 != 1:
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
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

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

def text_to_text_nodes(text):
    text_nodes = [TextNode(text, TextType.NORMAL)]
    delimiter_text_type_pairs = [('**', TextType.BOLD), ('*', TextType.ITALIC), ('`', TextType.CODE), ('_', TextType.ITALIC)]
    
    for delimiter, text_type in delimiter_text_type_pairs:
        text_nodes = split_nodes_delimiter(text_nodes, delimiter, text_type)

    return split_nodes_link(split_nodes_image(text_nodes))

def text_to_html_node(text):
    text_nodes = text_to_text_nodes(text)
    html_nodes = []

    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))

    return html_nodes

def create_html_node(text, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_html_node(text))
        case BlockType.HEADING:
            heading_number = get_heading_number(text)
            return LeafNode(f"h{heading_number}", text[heading_number + 1:])
        case BlockType.CODE:
            return LeafNode("code", text[3:-3])
        case BlockType.QUOTE:
            quote_text = ''
            for line in text.split('\n'):
                quote_text += line[2:] + '\n'
            return LeafNode("blockquote", quote_text.strip())
        case BlockType.UNORDERED_LIST:
            children = []   

            for line in text.split('\n'):
                children.append(ParentNode("li", text_to_html_node(line[2:])))
            
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            children = []

            for line in text.split('\n'):
                children.append(ParentNode("li", text_to_html_node(line[3:])))
            
            return ParentNode("ol", children)
        case _:
            raise Exception("Invalid BlockType for htmlNode")  

def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_html_node = create_html_node(block, block_type)
        child_nodes.append(block_html_node)

    return ParentNode('html', child_nodes)

def extract_title(text):
    matches = re.findall(r"^#{1}\s*(.*)", text)
    if len(matches) == 0:
        raise Exception('No markdown title found')
    
    return matches[0]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source_mkdn_file = ''

    with open(from_path) as file:
        source_mkdn_file += file.read()
    
    page = ''
    
    with open(template_path) as file:
        page += file.read()

    title = extract_title(source_mkdn_file)
    html_node = markdown_to_html_node(source_mkdn_file)
    content = html_node.to_html()

    page = page.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", content)

    split_dest_path = dest_path.split('/')
    dir_to_file = "/".join(split_dest_path[:-1])

    if (not path.exists(dir_to_file)):
        makedirs(dir_to_file)

    with open(dest_path, 'w') as file:
        file.write(page)

def generate_pages_recursive(dir_path_content, template_path, dir_path_dest):
    # print(f"Generating pages from {dir_path_content} to {dest_dir_path}")

    list_dir = listdir(dir_path_content)

    for entry in list_dir:
        if ".md" in entry:
            file_name = entry[:-3]
            generate_page(dir_path_content + '/' + entry, template_path, dir_path_dest + '/' + file_name + '.html')
        
        else:
            new_dir_path_content = dir_path_content + '/' + entry
            new_dir_path_dest = dir_path_dest + '/' + entry
            makedirs(new_dir_path_dest)
            generate_pages_recursive(new_dir_path_content, template_path, new_dir_path_dest)
