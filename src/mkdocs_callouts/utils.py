def parse_callout(title):
    """
    Returns proper syntax and title for the callout block.
    Expected results are ['!!!', title] or ['???'|'???+', title]
    """
    syntax = '!!!'
    # Foldable callouts use ???
    try:
        if title[0] == '-':
            syntax = '???'
            title = title[1:]
            pass
        if title[0] == '+':
            syntax = '???+'
            title = title[1:]
        # Remove leading space
        title = title[1:]
    # If callout has no title, keep it as is.
    except IndexError:
        pass
    return syntax, title
