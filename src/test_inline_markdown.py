import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class test_inline_markdown(unittest.TestCase):
    def test_text_node(self):
        node = TextNode('This is text **this is bolded** this is more text', TextType.TEXT)
        result = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(str(result), '[TextNode(This is text , text, None), TextNode(this is bolded, bold, None), TextNode( this is more text, text, None)]')

    def test_multiple_text_nodes(self):
        node = TextNode('This is some text _italic text_ more text _more italic text_ even more text', TextType.TEXT)
        node1 = TextNode('Some text _italics2_ last bit of text', TextType.TEXT)
        result = split_nodes_delimiter([node, node1], '_', TextType.ITALIC)
        self.assertEqual(str(result), '[TextNode(This is some text , text, None), TextNode(italic text, italic, None), TextNode( more text , text, None), TextNode(more italic text, italic, None), TextNode( even more text, text, None), TextNode(Some text , text, None), TextNode(italics2, italic, None), TextNode( last bit of text, text, None)]')

    def test_no_inline_types(self):
        node = TextNode('Just text', TextType.TEXT)
        result = split_nodes_delimiter([node], '**', TextType.CODE)
        self.assertEqual(str(result), '[TextNode(Just text, text, None)]')

    def test_raise_exception(self):
        node = TextNode('**not closed', TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(str(context.exception), 'invalid text in TextNode. TextNode text does not have closing delimiters')


class TestLinksAndImagesMarkdown(unittest.TestCase):
    def test_markdown_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(str(result), '''[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]''')

    def test_markdown_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(str(result), '''[('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]''')


class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode('This is text with an [link](https://www.j.com) and another [link2](www.j2.com)', TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode('This is text with an ', TextType.TEXT),
                TextNode('link', TextType.LINK, 'https://www.j.com'),
                TextNode(' and another ', TextType.TEXT),
                TextNode('link2', TextType.LINK, 'www.j2.com')
            ],
            new_nodes
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = 'This is **text** with an _italic_ word and a ```code block``` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode('This is ', TextType.TEXT, None),
                TextNode('text', TextType.BOLD, None),
                TextNode(' with an ', TextType.TEXT, None),
                TextNode('italic', TextType.ITALIC, None),
                TextNode(' word and a ', TextType.TEXT, None),
                TextNode('code block', TextType.CODE, None),
                TextNode(' and an ', TextType.TEXT, None),
                TextNode('obi wan image', TextType.IMAGE, 'https://i.imgur.com/fJRm4Vk.jpeg'),
                TextNode(' and a ', TextType.TEXT, None),
                TextNode('link', TextType.LINK, 'https://boot.dev'),
            ]
        )

    def test_text_to_nodes2(self):
        text = '_italic_ then some bold **text** followed by a link [link](www.google.ca)'
        result = text_to_textnodes(text)
        self.assertEqual(
            result,
            [
                TextNode('italic', TextType.ITALIC, None),
                TextNode(' then some bold ', TextType.TEXT, None),
                TextNode('text', TextType.BOLD, None),
                TextNode(' followed by a link ', TextType.TEXT, None),
                TextNode('link', TextType.LINK, 'www.google.ca')
            ]
        )



