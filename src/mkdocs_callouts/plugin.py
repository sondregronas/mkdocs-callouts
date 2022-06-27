from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

import re

from mkdocs_callouts.utils import (
    parse_callout_title,
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
        if not re.search(r'> ?\[!', markdown):
            return markdown

        # Read the markdown line for line
        lines = markdown.split('\n')

        # Then rebuild it, starting from scratch
        markdown = ''

        # isCallout keeps track of whether or not the next line is
        # part of the callout box, or if it's just regular markdown.
        is_callout = False
        for line in lines:
            contents = line
            if line.startswith('>[!') and ']' in line:  # Fix callout box syntax
                contents = line.replace('>[!', '> [!')
            if re.search(r'^( ?>*)*\[!(.*)\]', line):
                # This regex allow multiple callout in a callout
                is_callout = True
                nb_space = line.count('>')
                contents = parse_callout_title(line, nb_space)
            elif line.startswith('>') and is_callout:
                # parse callout contents
                contents = re.sub('> ?', '\t', line)
            elif is_callout:
                # no callout anymore
                is_callout = False
            markdown += contents + '\n'

        # Return the result
        return markdown
