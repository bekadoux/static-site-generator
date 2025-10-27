from fileops import clean_copy
from generator import generate_page


def main():
    clean_copy("./static", "./public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")


if __name__ == "__main__":
    main()
