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

        # is_callout keeps track of whether or not the next line is
        # part of a callout box, or if it's just regular markdown.
        is_callout = False
        for line in lines:
            new_line = line

            # Find callout box denotation(s) and parse the
            # title/type (regex covers nested callouts)
            if re.search(r'^( ?>*)*\[!(.*)\]', line):
                # start of callout
                is_callout = True
                # count the number of > symbols at start of line
                c = re.findall('^>+', line)
                nb_space = len(c[0])
                new_line = parse_callout_title(line, nb_space)

            # parse callout contents
            elif line.startswith('>') and is_callout:
                # count the number of > symbols at start of line
                c = re.findall('^>+', line)
                spaces = '\t' * len(c[0])
                # replace all leading > symbols 1:1 with tabs
                new_line = re.sub('^>+ ?', spaces, line)

            # end of callout
            elif is_callout:
                is_callout = False

            markdown += new_line + '\n'

        # Return the result
        return markdown
