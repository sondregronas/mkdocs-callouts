from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

from mkdocs_callouts.utils import (
    parse_callout,
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

        # isCallout keeps track of whether or not the next line is
        # part of the callout box, or if it's just regular markdown.
        isCallout = False
        for line in lines:
            # if line starts with callout syntax, parse it
            if line.startswith('> [!') and ']' in line:
                isCallout = True

                type = line.split('> [!')[1].split(']')[0]
                suffix = line.split(f'> [!{type}]')[1]

                # Get the syntax and title based on the
                # block suffix the callout block.
                syntax, title = parse_callout(suffix)

                # Syntax for admonition, type must be lowercase
                markdown += f'{syntax} {type.lower()} "{title}"\n'
                continue

            if line.startswith('> ') and isCallout:
                markdown += f'{line.replace("> ", "    ")}\n'
                continue

            # If the line is not part of a callout,
            # add it back wihout any modifications
            markdown += f'{line}\n'
            isCallout = False

        # Return the result
        return markdown
