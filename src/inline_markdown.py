from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type.value != "text":
            new_nodes.append(node)
            continue
            
        if node.text.count(delimiter) == 0:
            new_nodes.append(node)
            continue

        text_list = node.text.split(delimiter)
        if len(text_list) % 2 == 0:
            raise Exception('invalid text in TextNode. TextNode text does not have closing delimiters')

        for idx in range(len(text_list)):
            if text_list[idx] == "":
                continue
            elif idx % 2 != 0:
                new_nodes.append(TextNode(text_list[idx], text_type))
            else:
                new_nodes.append(TextNode(text_list[idx], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type.value != 'text':
            new_nodes.append(node)
            continue

        extracted_images = extract_markdown_images(node.text)
        if len(extracted_images) == 0:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text
        if remaining_text == "":
            continue

        for image in extracted_images:
            parts = remaining_text.split(f'![{image[0]}]({image[1]})')
            if len(parts) != 2:
                raise Exception('invalid markdown. Image is not closed')
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            if len(parts) > 1:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
    

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type.value != 'text':
            new_nodes.append(node)
            continue
            
        extracted_links = extract_markdown_links(node.text)
        if len(extracted_links) == 0:
            new_nodes.append(node)
            continue
        
        remaining_text = node.text
        if remaining_text == "":
            continue

        for link in extracted_links:
            parts = remaining_text.split(f'[{link[0]}]({link[1]})')
            if len(parts) != 2:
                raise Exception('invalid markdown. Link not closed')
            if parts[0] != "":
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            if len(remaining_text) > 2:
                remaining_text = parts[1]
            else:
                remaining_text = ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

