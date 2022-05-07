from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

# Callouts converts the following obsidian callout block:
#   > [!INFO] Title
#   > An information callout from Obsidian
#   > inspired by the syntax from the Microsoft Docs
#
# and turns it into a mkdocs supported admonition:
#   !!! info "Title"
#       An admonition block for MkDocs.
#       Allowing you to edit your notes
#       with confidence using Obsidian.
# Supports >[!INFO]- and >[!INFO]+ foldable callouts.


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


class CalloutsPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files):
        # Read the markdown line for line
        lines = markdown.split('\n')

        # Then we rebuild it, starting from scratch
        markdown = ''

        # calloutBlock keeps track of whether or not the next line is
        # part of the calloutBlock, or just a regular block.
        calloutBlock = False
        for line in lines:
            # if line starts with callout syntax, parse it
            if line.startswith('> [!'):
                calloutBlock = True

                type = line.split('> [!')[1].split(']')[0]
                after = line.split(f'> [!{type}]')[1]

                # Get proper denotation and title based on the text
                # after the callout block.
                denotation, title = ParseBlockType(after)

                # Syntax for admonition
                new = f'{denotation} {type.lower()} "{title}"'
                markdown += f'{new}\n'
                continue

            if line.startswith('> ') and calloutBlock:
                markdown += f'{line.replace("> ", "    ")}\n'
                continue

            # If line is not part of a callout, render it like normal
            markdown += f'{line}\n'
            calloutBlock = False

        # Return the result
        return markdown
