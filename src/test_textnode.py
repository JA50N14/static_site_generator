import unittest
from textnode import TextType, TextNode, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('This is a test node', TextType.BOLD)
        node2 = TextNode('This is a test node', TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode('A test node', TextType.ITALIC)
        node2 = TextNode('A test node', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode('Test node', TextType.LINK, 'https://www.j.com')
        node2 = TextNode('Test node', TextType.LINK, 'https://www.j.com')
        self.assertEqual(node, node2)

    def test_url_is_none(self):
        node = TextNode('Test node', TextType.BOLD)
        self.assertIsNone(node.url)


class TestConverter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode('here is a link', TextType.LINK, 'www.google.ca')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'here is a link')
        self.assertEqual(html_node.props, {'href': 'www.google.ca'})
    
    def test_image(self):
        node = TextNode('alt text', TextType.IMAGE, 'path/to/image/')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {'src': 'path/to/image/', 'alt': 'alt text'})


if __name__ == "__main__":
    unittest.main()
