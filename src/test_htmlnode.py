import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag='p', value='Test paragraph', props={"href": "https://www.google.ca", "target": "blank"})
        props_to_html_test = node.props_to_html()
        self.assertTrue(props_to_html_test == ' href="https://www.google.ca" target="blank"')

    def test_props_to_html_2(self):
        node = HTMLNode(props={'cols': 2, 'rows': 2, 'id': 'pro_123'})
        props_to_html_test = node.props_to_html()
        self.assertTrue(props_to_html_test == ' cols="2" rows="2" id="pro_123"')

    def test_html_node_args(self):
        node = HTMLNode('p', 'This is a test', ['span', 'div'], {'target': 'blank'})
        self.assertEqual(node.tag, 'p')
        self.assertEqual(node.value, 'This is a test')
        self.assertEqual(node.children, ['span', 'div'])
        self.assertEqual(node.props, {'target': 'blank'})



    def test_leaf_to_html(self):
        node = LeafNode('p', 'This is a test paragraph', {'id': '123'})
        self.assertEqual(node.to_html(), '<p id="123">This is a test paragraph</p>')

    def test_leaf_args(self):
        node = LeafNode('a', 'test', {'href': 'www.j.com'})
        self.assertEqual(node.tag, 'a')
        self.assertEqual(node.value, 'test')
        self.assertEqual(node.props, dict(href='www.j.com'))



    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("b", "child node", {'href': 'www.j.com'})
        parent_node = ParentNode("p", [child_node], {'id': '123'})
        self.assertEqual(parent_node.to_html(), '<p id="123"><b href="www.j.com">child node</b></p>')

    def test_to_html_no_children(self):
        parent_node = ParentNode("p", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "children are required to create a ParentNode")

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child node")
        parent_node = ParentNode(None, [child_node])

        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        self.assertEqual(str(context.exception), "tag is required to create a ParentNode")
        
        