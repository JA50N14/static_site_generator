import os, shutil

def copy_static_to_public_recursive(src_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    src_dir_list = os.listdir(src_dir_path)
    
    for src_item in src_dir_list:
        if os.path.isfile(os.path.join(src_dir_path, src_item)):
            shutil.copy(os.path.join(src_dir_path, src_item), os.path.join(dest_dir_path, src_item))
        
        if os.path.isdir(os.path.join(src_dir_path, src_item)):
            os.mkdir(os.path.join(dest_dir_path, src_item))
            copy_static_to_public_recursive(os.path.join(src_dir_path, src_item), os.path.join(dest_dir_path, src_item))