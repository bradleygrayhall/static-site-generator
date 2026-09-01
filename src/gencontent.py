import os
import pathlib

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    markdown = markdown.split("\n")
    for line in markdown:
        if line.startswith("# "):
            return line[2:].strip(" ")
    raise Exception("No header found")

def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as f:
        from_contents = f.read()
    with open(template_path,"r") as f:
        template_contents = f.read()
    htmlified = markdown_to_html_node(from_contents).to_html()
    title = extract_title(from_contents)
    template_contents = template_contents.replace("{{ Title }}",title).replace("{{ Content }}",htmlified).replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir,exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_contents)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content,filename)
        dest_path = os.path.join(dest_dir_path,filename)
        if os.path.isfile(from_path)and dest_path.endswith(".md"):
            new_path = pathlib.Path(dest_path).with_suffix(".html")
            generate_page(from_path,template_path,new_path,basepath)
        elif not os.path.isfile(from_path):
            generate_pages_recursive(from_path,template_path,dest_path,basepath)
        else:
            continue