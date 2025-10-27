from block_md import extract_title, markdown_to_html_node
from fileops import write_content


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, "r") as f:
            md_content = f.read()
        with open(template_path, "r") as f:
            template_content = f.read()
    except OSError as e:
        raise OSError(f"could not read files: {e}") from e

    html_from_md = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)

    full_html = template_content.replace("{{ Title }}", title)
    full_html = template_content.replace("{{ Content }}", html_from_md)

    write_content(dest_path, full_html)
