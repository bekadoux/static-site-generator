from textnode import TextType, TextNode


def main():
    node = TextNode("some anchor text", TextType.LINK, "https://example.com")
    print(node)


if __name__ == "__main__":
    main()
