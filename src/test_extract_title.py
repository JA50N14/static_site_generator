import unittest
from generate_page import extract_title

class test_extract_title(unittest.TestCase):
    def test_header_extraction(self):
        md = '''
# This is the header

Here is other text
'''
        title = extract_title(md)
        print(title)
        self.assertEqual(title, 'This is the header')
    
    def test_header_extraction_error(self):
        md = '''
## No h1 header

Some random text
'''
        with self.assertRaises(Exception) as context:
            extract_title(md)

        self.assertEqual(str(context.exception), 'There is no h1 header in the markdown file')