import re


def parse_callout_syntax(line: str) -> str:
    """Converts the callout syntax from obsidian into the mkdocs syntax"""
    block = re.search(r'^ ?(>*) *\[!([^\]]*)\]([\-\+]?)(.*)?', line)

    # Group 1: Leading > symbols (indentation, for nested callouts)
    indent = block.group(1).count('>')
    indent = '\t' * (indent - 1)

    # Group 2: Callout block type (note, warning, info, etc.) + inline block syntax
    type = block.group(2).lower()
    type = re.sub(r' ?\| *(inline|left) *$', ' inline', type)
    type = re.sub(r' ?\| *(inline end|right) *$', ' inline end', type)
    type = re.sub(r' ?\|.*', '', type)

    # Group 3: Foldable callouts
    syntax = {'-': '???', '+': '???+', '': '!!!'}
    syntax = syntax[block.group(3)]

    # Group 4: Title, add leading whitespace and quotation marks, if it exists
    title = block.group(4).strip()
    title = f' "{title}"' if title else ''

    # Construct the new callout syntax ({indent}!!! note "Title")
    return f'{indent}{syntax} {type}{title}'
