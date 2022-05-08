def ParseBlockType(title):
    """
    Returns proper denotation and title for the callout block.
    Expected results are [!!!, title] or [???|???+, title]
    """
    denotation = '!!!'
    # Foldable callouts require a different denotation
    try:
        if title[0] == '-':
            denotation = '???'
            title = title[1:]
            pass
        if title[0] == '+':
            denotation = '???+'
            title = title[1:]
        # Remove leading space
        title = title[1:]
    # If callout is untitled, pass.
    except IndexError:
        pass
    return denotation, title
