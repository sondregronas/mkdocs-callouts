from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

from mkdocs_callouts.utils import (
    ParseBlockType,
)


class CalloutsPlugin(BasePlugin):
    """
    Reads your markdown docs for the following style of callout block:
       > [!INFO] Title
       > An information callout from Obsidian
       > inspired by the syntax from the Microsoft Docs

     and converts it into a mkdocs supported admonition:
       !!! info "Title"
           An admonition block for MkDocs.
           Allowing you to edit your notes
           with confidence using Obsidian.

     Also Supports foldable callouts (> [!INFO]- and > [!INFO]+)
    """

    def on_page_markdown(self, markdown, page, config, files):
        # #save-the-cycles
        if '> [!' not in markdown:
            return markdown

        # Read the markdown line for line
        lines = markdown.split('\n')

        # Then we rebuild it, starting from scratch
        markdown = ''

        # calloutBlock keeps track of whether or not the next line is
        # part of the calloutBlock, or just a regular block.
        calloutBlock = False
        for line in lines:
            # if line starts with callout syntax, parse it
            if line.startswith('> [!') and ']' in line:
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
