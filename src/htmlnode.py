from functools import reduce

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented yet")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return reduce(lambda acc, item: acc + f' {item[0]}="{item[1]}"', self.props.items(), '')
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError('all leaf nodes must have a value')
        elif self.tag is None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    

    def to_html(self):
        if self.tag is None:
            raise ValueError('tag is required to create a ParentNode')
        elif self.children is None:
            raise ValueError('children are required to create a ParentNode')
        else:
            if self.children is None:
                return self.to_html()
            html_result = f'<{self.tag}{self.props_to_html()}>'
            for child in self.children:
                html_result = html_result + child.to_html()
            return f'{html_result}</{self.tag}>'
    
    def __repr__(self):
        return f'ParentNode ({self.tag}, children: {self.children}, {self.props})'
    

