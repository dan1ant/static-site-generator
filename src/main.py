import os
import shutil

def main():
    copy_folder("static", "public")

def copy_folder(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    os.mkdir(dst_dir)
    items = os.listdir(src_dir)
    for item in items:
        src_item = os.path.join(src_dir, item)
        dst_item = os.path.join(dst_dir, item)
        
        if os.path.isfile(src_item):
            print(f"Copying file: {src_item} to {dst_item}")
            shutil.copy(src_item, dst_item)
        else:
            print(f"Creating directory: {dst_item}")
            os.mkdir(dst_item)
            copy_folder(src_item, dst_item)
   
if __name__ == "__main__":
    main()
