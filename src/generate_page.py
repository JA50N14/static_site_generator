from blocks_markdown import markdown_to_blocks
from markdown_to_html import markdown_to_html_node
import os
from pathlib import Path

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()
    raise Exception('There is no h1 header in the markdown file')


def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as f:
        md = f.read()
    
    with open(template_path, 'r') as f:
        html_template = f.read()

    html_body = markdown_to_html_node(md)
    page_title = extract_title(md)
    
    html_template = html_template.replace('{{ Title }}', page_title)
    html_template = html_template.replace('{{ Content }}', html_body)
    html_template = html_template.replace('href="/', f'href="{basepath}')
    html_template = html_template.replace('src="/', f'src="{basepath}')

    with open(dest_path, 'w') as f:
        f.write(html_template)
    

def generate_pages_recursive(from_path, template_path, dest_path, basepath):
    from_path_dir_list = os.listdir(from_path)
    
    for dir_item in from_path_dir_list:
        dir_item_path = os.path.join(from_path, dir_item)
        if os.path.isdir(dir_item_path):
            os.mkdir(os.path.join(dest_path, dir_item))
            generate_pages_recursive(dir_item_path, template_path, os.path.join(dest_path, dir_item), basepath)
        
        if dir_item.endswith('.md'):
            with open(dir_item_path, 'r') as f:
                md = f.read()
            
            with open(template_path, 'r') as f:
                html_template = f.read()

            html_body = markdown_to_html_node(md)
            page_title = extract_title(md)

            html_template = html_template.replace('{{ Title }}', page_title)
            html_template = html_template.replace('{{ Content }}', html_body)
            html_template = html_template.replace('href="/', f'href="{basepath}')
            html_template = html_template.replace('src="/', f'src="{basepath}')


            with open(Path(dest_path, dir_item[:-3] + '.html'), 'w') as f:
                f.write(html_template)





    






