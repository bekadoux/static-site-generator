def markdown_to_blocks(markdown):
    blocks = [p.strip() for p in markdown.split("\n\n")]
    return [block for block in blocks if block != ""]
