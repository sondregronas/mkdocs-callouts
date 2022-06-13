from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

import re

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

    Also handles foldable callouts: > [!INFO]- Im foldable, closed
                                    > [!INFO]+ Im foldable, open
    """

    def on_page_markdown(self, markdown, page, config, files):
        # #save-the-cycles
        if '> [!' not in markdown:
            return markdown

        # Read the markdown line for line
        lines = markdown.split('\n')

        # Then rebuild it, starting from scratch
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

            if line.startswith('>') and isCallout:
                # find leading ">" or "> " and replace
                # with 4 spaces, defining the callout content
                regex = re.compile(r"^> {0,1}")
                c_line = re.sub(regex, '    ', line)

                markdown += f'{c_line}\n'
                continue

            # If the line is not part of a callout,
            # re-add it without modifications
            markdown += f'{line}\n'
            isCallout = False

        # Return the result
        return markdown
