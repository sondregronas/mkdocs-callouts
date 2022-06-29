import re


# Convert callout syntax from obsidian to mkdocs
def parse_callout_syntax(line: str):
    block = re.search(r'^ ?(>*) *\[!([^\]]*)\]([\-\+]?)(.*)?', line)

    # Group 1: Leading > symbols (indentation, for nested callouts)
    indent = block.group(1).count('>')
    indent = '\t' * (indent - 1)

    # Group 2: Callout block type (note, warning, info, etc.)
    type = block.group(2).lower()

    # Group 3: Foldable callouts
    foldable = block.group(3)
    if foldable == '-':
        syntax = '???'
    elif foldable == '+':
        syntax = '???+'
    else:
        syntax = '!!!'

    # Group 4: Title, add leading whitespace and quotation marks, if it exists
    title = block.group(4).strip()
    if title:
        title = f' "{title}"'

    # Construct the new callout syntax ({indent}!!! note "Title")
    return f'{indent}{syntax} {type}{title}'
