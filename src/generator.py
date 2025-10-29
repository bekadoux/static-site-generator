import os
from block_md import extract_title, markdown_to_html_node
from fileops import write_content


def generate_pages_recursive(
    basepath: str, dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for content in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, content)
        new_dest_dir_path = os.path.join(dest_dir_path, content)
        if os.path.isdir(content_path):
            generate_pages_recursive(
                basepath, content_path, template_path, new_dest_dir_path
            )
        elif os.path.isfile(content_path) and content.endswith(".md"):
            html_file_name = content.replace(".md", ".html")
            generate_page(
                basepath,
                content_path,
                template_path,
                os.path.join(dest_dir_path, html_file_name),
            )


def generate_page(
    basepath: str, from_path: str, template_path: str, dest_path: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, "r") as f:
            md_content = f.read()
        with open(template_path, "r") as f:
            template_content = f.read()
    except OSError as e:
        raise OSError(f"could not read files: {e}") from e

    title = extract_title(md_content)
    html_from_md = markdown_to_html_node(md_content).to_html()

    full_html = template_content.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_from_md)

    full_html.replace('href="/', f'href="{basepath}')
    full_html.replace('src="/', f'src="{basepath}')

    write_content(dest_path, full_html)
