from blocks_markdown import BlockType, markdown_to_blocks, block_to_block_type
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    root_parent_node = ParentNode("div", [])
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        block_parent_node = create_parent_node_for_block(block_type, block)
        children = text_to_children(block, block_type)
        block_parent_node.children.extend(children)
        root_parent_node.children.append(block_parent_node)
    return root_parent_node.to_html()


def create_parent_node_for_block(block_type, block):
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", [])
        
    if block_type == BlockType.QUOTE:
        return ParentNode("blockquote", [])
    
    if block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", [])
    
    if block_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", [])
    
    if block_type == BlockType.CODE:
        return ParentNode("pre", [])
    
    if block_type == BlockType.HEADING:
        heading_dict = {"# ": "h1", "## ": "h2", "### ": "h3", "#### ": "h4", "##### ": "h5", "###### ": "h6"}
        for k in heading_dict:
            if block.startswith(k):
                return ParentNode(f'{heading_dict[k]}', [])
        
    
def text_to_children(block, block_type):

    if block_type == BlockType.PARAGRAPH:
        return create_paragraph_list_children(block, block_type)
    
    if block_type == BlockType.UNORDERED_LIST:
        return create_unordered_list_children(block, block_type)
    
    if block_type == BlockType.ORDERED_LIST:
        return create_ordered_list_children(block, block_type)

    if block_type == BlockType.QUOTE:
        return create_quote_list_children(block, block_type)
    
    if block_type == BlockType.HEADING:
        return create_heading_children(block, block_type)
    
    if block_type == BlockType.CODE:
        return create_code_children(block, block_type)


def create_block_list(block, block_type):
    block_list = []

    for line in block.split("\n"):
        line = line.lstrip()
        if line == "":
            continue
        if block_type.value in ['quote', 'unordered_list']:
            block_list.append(line[2:])
        elif block_type.value == 'ordered_list':
            block_list.append(line[3:])
        elif block_type.value == 'heading':
            heading_dict = {"# ": 2, "## ": 3, "### ": 4, "#### ": 5, "##### ": 6, "###### ": 7}
            for k in heading_dict:
                if line.startswith(k):
                    block_list.append(line[heading_dict[k]:])
        else:
            block_list.append(line)
    return block_list


def create_paragraph_list_children(block, block_type):
    child_nodes_of_block_parent = []
    block_list = create_block_list(block, block_type)

    for text in block_list:
        text_nodes = text_to_textnodes(text)

        for text_node in text_nodes:
            if text_node.text_type == TextType.TEXT:
                child_nodes_of_block_parent.append(text_node)
                continue
            if text_node.text_type != TextType.TEXT:
                tag_dict = {'bold': 'b', 'italic': 'i', 'code': 'code', 'link': 'a', 'image': 'img', 'code': 'code'}
                if text_node.text_type.value in tag_dict:
                    props_map = {'link': lambda node: {'href': node.url}, 'image': lambda node: {'src': node.url, 'alt': node.text}}
                    props = props_map.get(text_node.text_type.value, lambda node: None)(text_node)
                    if text_node.text_type.value == 'image':
                        new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode('', TextType.TEXT)], props)
                    else:
                        new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode(text_node.text, TextType.TEXT)], props)
                child_nodes_of_block_parent.append(new_parent_node)
            else:
                raise Exception('TextNode.text_type not in tag_dict')
    return child_nodes_of_block_parent


def create_unordered_list_children(block, block_type):
    child_nodes_of_block_parent = []
    block_list = create_block_list(block, block_type)

    for text in block_list:
        parent_node = ParentNode('li',[])
        text_nodes = text_to_textnodes(text)

        for text_node in text_nodes:
            if text_node.text_type == TextType.TEXT:
                parent_node.children.append(text_node)
            if text_node.text_type != TextType.TEXT:
                tag_dict = {'bold': 'b', 'italic': 'i', 'code': 'code', 'link': 'a', 'image': 'img'}
                if text_node.text_type.value in tag_dict:
                    props_map = {'link': lambda node: {'href': node.url}, 'image': lambda node: {'src': node.url, 'alt': node.text}}
                    props = props_map.get(text_node.text_type.value, lambda node: None)(text_node)
                    if text_node.text_type.value == 'image':
                        new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode('', TextType.TEXT)], props)
                    else:
                        new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode(text_node.text, TextType.TEXT)], props)
                    parent_node.children.append(new_parent_node)
                else:
                    raise Exception('TextNode.text_type not in tag_dict')
        child_nodes_of_block_parent.append(parent_node)
    return child_nodes_of_block_parent


def create_ordered_list_children(block, block_type):
    child_nodes_of_block_parent = []
    block_list = create_block_list(block, block_type)

    for text in block_list:
        parent_node = ParentNode('li', [])
        text_nodes = text_to_textnodes(text)

        for text_node in text_nodes:
            if text_node.text_type == TextType.TEXT:
                parent_node.children.append(text_node)
            if text_node.text_type != TextType.TEXT:
                tag_dict = {'bold': 'b', 'italic': 'i', 'code': 'code', 'link': 'a', 'image': 'img'}
                if text_node.text_type.value in tag_dict:
                    props_map = {'link': lambda node: {'href': node.url}, 'image': lambda node: {'src': node.url, 'alt': text_node.text}}
                    props = props_map.get(text_node.text_type.value, lambda node: None)(text_node)
                    if text_node.text_type.value == 'image':
                        new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode('', TextType.TEXT)], props)
                    else:
                        new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode(text_node.text, TextType.TEXT)], props)
                    parent_node.children.append(new_parent_node)
                else:
                    raise Exception('TextNode.text_type not in tag_dict')
        child_nodes_of_block_parent.append(parent_node)
    return child_nodes_of_block_parent


def create_quote_list_children(block, block_type):
    child_nodes_of_block_parent = []
    block_list = create_block_list(block, block_type)
    text_nodes = text_to_textnodes(" ".join(block_list))

    for text_node in text_nodes:
        if text_node.text_type == TextType.TEXT:
            child_nodes_of_block_parent.append(text_node)
        if text_node.text_type != TextType.TEXT:
            tag_dict = {'bold': 'b', 'italic': 'i', 'code': 'code', 'link': 'a', 'image': 'img'}
            if text_node.text_type.value in tag_dict:
                props_map = {'link': lambda node: {'href': node.url}, 'image': lambda node: {'src': node.url, 'alt': text_node.text}}
                props = props_map.get(text_node.text_type.value, lambda node: None)(text_node)
                if text_node.text_type.value == 'image':
                    new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode('', TextType.TEXT)], props)
                else:
                    new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode(text_node.text, TextType.TEXT)], props)
                child_nodes_of_block_parent.append(new_parent_node)
            else:
                raise Exception('TextNode.text_type not in tag_dict')
    return child_nodes_of_block_parent


def create_heading_children(block, block_type):
    child_nodes_of_block_parent = []
    block_list = create_block_list(block, block_type)
    text_nodes = text_to_textnodes(" ".join(block_list))

    for text_node in text_nodes:
        if text_node.text_type == TextType.TEXT:
            child_nodes_of_block_parent.append(text_node)
        if text_node.text_type != TextType.TEXT:
            tag_dict = {'bold': 'b', 'italic': 'i', 'code': 'code', 'link': 'a', 'image': 'img'}
            if text_node.text_type.value in tag_dict:
                props_map = {'link': lambda node: {'href': node.url}, 'image': lambda node: {'src': node.url, 'alt': text_node.text}}
                props = props_map.get(text_node.text_type.value, lambda node: None)(text_node)
                if text_node.text_type.value == 'image':
                    new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode('', TextType.TEXT)], props)
                else:
                    new_parent_node = ParentNode(tag_dict[text_node.text_type.value], [TextNode(text_node.text, TextType.TEXT)], props)
                child_nodes_of_block_parent.append(new_parent_node)
            else:
                raise Exception('TextNode.text_type not in tag_dict')
    return child_nodes_of_block_parent


def create_code_children(block, block_type):
    block_list = create_block_list(block, block_type)
    code_text_list = []

    for text in block_list:
        if text == "" or text.startswith('```'):
            continue
        code_text_list.append(text + "\n")
    
    text_node = TextNode("".join(code_text_list), TextType.TEXT)
    return [ParentNode('code', [text_node])]



