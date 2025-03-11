import os
import sys
import shutil
from pathlib import Path

from block import markdown_to_html_node
from extractor import extract_title

def main():
    print("argv", sys.argv)
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_folder("static", "docs")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "docs", basepath)

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

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_content = None
    template_content = None
    with open(from_path) as f:
        from_content = f.read()
    with open(template_path) as f:
        template_content = f.read()

    title = extract_title(from_content)
    html = markdown_to_html_node(from_content).to_html()
    template_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    items = os.listdir(dir_path_content)    
    for item in items:
        src_path = Path(dir_path_content, item)
        dst_path = Path(dest_dir_path, item.replace(".md", ".html"))

        if os.path.isfile(src_path):
            generate_page(src_path, template_path, dst_path, basepath) 
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            generate_pages_recursive(src_path, template_path, dst_path, basepath)

if __name__ == "__main__":
    main()
