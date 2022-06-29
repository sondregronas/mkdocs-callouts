from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

import re

from mkdocs_callouts.utils import (
    parse_callout_syntax,
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
        # If markdown file does not contain a callout, skip it
        if not re.search(r'> ?\[!', markdown):
            return markdown

        new_markdown = ''
        is_callout = False
        for line in markdown.split('\n'):
            # Find callout box syntax and parse the
            # title/type (regex covers nested callouts)
            if re.search(r'^ ?>* *\[![^\]]*\]', line):
                is_callout = True
                line = parse_callout_syntax(line)

            # Parse the callout content, replacing > symbols with indentation
            elif re.search(r'^ ?>+', line) and is_callout:
                indent = re.search(r'^ ?(>+)', line)
                indent = '\t' * indent.group(1).count('>')
                line = re.sub(r'^ ?>+ ?', indent, line)

            # End callout block when no leading > is present
            elif is_callout:
                is_callout = False

            new_markdown += line + '\n'

        # Return the result, minus the last \n
        return new_markdown[:-1]
