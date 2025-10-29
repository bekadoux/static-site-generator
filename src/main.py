import sys
from fileops import clean_copy
from generator import generate_pages_recursive

STATIC_PATH = "./static"
PUBLIC_PATH = "./docs"
CONTENT_PATH = "./content"
TEMPLATE_PATH = "./template.html"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    clean_copy(STATIC_PATH, PUBLIC_PATH)
    generate_pages_recursive(basepath, CONTENT_PATH, TEMPLATE_PATH, PUBLIC_PATH)


if __name__ == "__main__":
    main()
