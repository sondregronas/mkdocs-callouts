def parse_callout(suffix):
    """
    Returns proper syntax and title for the callout block.
    Expected results are ['!!!', title] or ['???'|'???+', title]
    """
    syntax = '!!!'
    title = suffix
    # Check if the first character of the
    # suffix defines a foldable callout.
    # Lastly remove the leading space from title
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
    # If title is empty, do nothing.
    except IndexError:
        pass
    return syntax, title
