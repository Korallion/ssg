from enums import BlockType

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
        return block_text_lines[0][:2] == '- ' and block_text_lines[0][:2] == '* '

    for line in block_text_lines:
        if line[:2] != '- ' and line[:2] != '* ':
            return False

    return True

def is_o_list_block_type(block_text_lines):
    if len(block_text_lines) == 1:
        return block_text_lines[0][:2] == '1. '

    for index, line in enumerate(block_text_lines):
        if line[:3] != f"{index + 1}. ":
            return False

    return True

def get_heading_number(text):
    count = 0
    for char in text:
        if char == '#':
            count += 1
        else:
            return count

def block_to_block_type(block_text):
    if get_heading_number(block_text) > 0 and block_text[get_heading_number(block_text)] == ' ':
        return BlockType.HEADING
    elif len(block_text) >= 6 and block_text[:3] == '```' and block_text[-3:] == '```':
        return BlockType.CODE
    
    block_text_lines = block_text.split('\n')

    if is_quote_block_type(block_text_lines):
        return BlockType.QUOTE
    elif is_u_list_block_type(block_text_lines):
        return BlockType.UNORDERED_LIST
    elif is_o_list_block_type(block_text_lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


    