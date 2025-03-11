import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_title(markdown):
    split = markdown.split("\n")
    splitted = split[0]
    splitted_no_hash = splitted.lstrip("#")

    diff = len(splitted) - len(splitted_no_hash) 
    if splitted_no_hash == "" or diff != 1:
        raise ValueError(f"{splitted} is not a title")
    return splitted_no_hash.strip()
    
