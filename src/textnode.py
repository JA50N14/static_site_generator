from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def to_html(self):
        return self.text
    
    def __eq__(self, other):
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'
    

def text_node_to_html_node(text_node):
    tag_dict = {'text': '', 'bold': 'b', 'italic': 'i', 'code': 'code', 'link': 'a', 'image': 'img'}
    if text_node.text_type.value in tag_dict:
        if text_node.text_type.value == 'text':
            return LeafNode(None, text_node.text)
        if text_node.text_type.value == 'link':
            props = {'href': text_node.url}
            return LeafNode(tag_dict[text_node.text_type.value], text_node.text, props)
        if text_node.text_type.value == 'image':
            props = {'src': text_node.url, 'alt': text_node.text}
            return LeafNode(tag_dict[text_node.text_type.value], None, props)
        return LeafNode(tag_dict[text_node.text_type.value], text_node.text)
    raise Exception('TextNode does not have a valid text_type attribute')

