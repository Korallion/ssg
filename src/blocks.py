from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unorderd_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown_text):
    blocks = markdown_text.strip("\n").split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped_blocks.append(block.strip())
    return stripped_blocks

def is_quote_block_type(block_text_lines):
    if len(block_text_lines) == 1:
        return block_text_lines[0] == '>'

    for line in block_text_lines:
        if line[0] != '>':
            return False
    
    return True

def is_u_list_block_type(block_text_lines):
    if len(block_text_lines) == 1:
        return line[0] == '-' | line[0] == '*'

    for line in block_text_lines:
        if line[0] != '-' | line[0] != '*':
            return False

    return True

def is_o_list_block_type(block_text_lines):
    if len(block_text_lines) == 1:
        return line[0:2] == '1. '

    for index, line in enumerate(block_text_lines):
        if line[0] != index + 1 & line[1:2] != '. ':
            return False

    return True


def block_to_block_type(block_text):
    if block_text[0] == '#':
        return BlockType.HEADING
    elif block_text[:3] == '```' & block_text[-3:] == '```':
        return BlockType.CODE
        
    block_text_lines = block_text.split('\n')

    if is_quote_block_type(block_text_lines):
        return BlockType.UNORDERED_LIST
    elif is_u_list_block_type(block_text_lines):
        return BlockType.UNORDERED_LIST
    elif is_o_list_block_type(block_text_lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


    