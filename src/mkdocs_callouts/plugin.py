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


class CalloutsPlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, files):
        # Loop through every callout block, starting from index 1.
        for callout in markdown.split('> [!')[1::1]:
            callout_end = callout.split('\n')[0]

            # Store the original string, we will need to replace it later
            original = f'> [!{callout_end}'

            # Default denotation of admonitions
            denotation = '!!!'
            # Store admonition type
            type = callout_end.split(']')[0]
            # Store admonition title (and foldable identifier)
            title = callout_end.split(']')[1]

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

            # Store the new string & replace it.
            new = f'{denotation} {type.lower()} "{title}"'
            markdown = markdown.replace(original, new, 1)

        # Replace every callout indent to a 4 space admonition indent.
        markdown = markdown.replace('\n> ', '\n    ')

        # Return the result
        return markdown
