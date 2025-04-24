import os, shutil
import sys
from copy_static import copy_static_to_public_recursive
from generate_page import generate_page, generate_pages_recursive

dir_path_content = './content'
dir_path_template = './template.html'
dir_path_static = './static'
dir_path_public = './docs'
basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
print(f'BASEPATH: {basepath}')

def main():
    print('Deleting public directory...')
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    print('Copying static files to public directory...')
    copy_static_to_public_recursive(dir_path_static, dir_path_public)

    print('Generating page...')
    # generate_page(
    #     os.path.join(dir_path_content, 'index.md'), 
    #     dir_path_template, 
    #     os.path.join(dir_path_public, 'index.html'),
    #     basepath
    # )

    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_public, basepath)

main()

