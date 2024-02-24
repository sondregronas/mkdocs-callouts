import pytest

from mkdocs_callouts.plugin import CalloutsPlugin
from mkdocs_callouts.utils import CalloutParser


def convert(input: str) -> str:
    """For readability: Parse the input string using the plugin"""
    return CalloutsPlugin().on_page_markdown(input, None, None, None)


def test_regular_blocks():
    # Untitled block
    mkdown = '> [!INFO]\n> Unitled block'
    result = '!!! info\n\tUnitled block'
    assert (convert(mkdown) == result)

    # Titled block
    mkdown = '> [!INFO] Title\n> Titled block\n> Two lines'
    result = '!!! info "Title"\n\tTitled block\n\tTwo lines'
    assert (convert(mkdown) == result)

    # Multi-word titled blocks
    mkdown = '> [!INFO] This title has spaces\n> And text'
    result = '!!! info "This title has spaces"\n\tAnd text'
    assert (convert(mkdown) == result)

    # Test callout paragraphs (empty callout line)
    mkdown = '> [!INFO] Title\n> Paragraph 1\n>\n> Paragraph 2'
    result = '!!! info "Title"\n\tParagraph 1\n\t\n\tParagraph 2'
    assert (convert(mkdown) == result)


def test_false_positives():
    # Test link in regular block (not a callout)
    mkdown = '> [[Wikilink]] in a block\n> [Link](https://example.com)'
    result = '> [[Wikilink]] in a block\n> [Link](https://example.com)'
    assert (convert(mkdown) == result)

    # Test non-callout blocks
    mkdown = '> [!custom] Callout\n> Callout Text\nSome text\n> Block'
    result = '!!! custom "Callout"\n\tCallout Text\nSome text\n> Block'
    assert (convert(mkdown) == result)


def test_edgecases():
    # Test titles with > symbols
    mkdown = '> [!INFO] > in title >\n> text'
    result = '!!! info "> in title >"\n\ttext'
    assert (convert(mkdown) == result)

    # Test titles with callout syntax as title
    mkdown = '> [!INFO] > [!WARNING]\n> text'
    result = '!!! info "> [!WARNING]"\n\ttext'
    assert (convert(mkdown) == result)

    # Test callouts without whitespace
    mkdown = '>[!INFO] Title\n>Content'
    result = '!!! info "Title"\n\tContent'
    assert (convert(mkdown) == result)

    # Test > block within callout
    mkdown = '> [!INFO] Title\n> > Block within callout'
    result = '!!! info "Title"\n\t> Block within callout'
    assert (convert(mkdown) == result)

    # Test > character in callout content
    mkdown = '> [!INFO] Title\n> The > character'
    result = '!!! info "Title"\n\tThe > character'
    assert (convert(mkdown) == result)

    # Test callout with leading spaces
    mkdown = ' > [!NOTE] Test\n > Text'
    result = '!!! note "Test"\n\tText'
    assert (convert(mkdown) == result)

    # Test callout without whitespace
    mkdown = '>[!NOTE] Test\n>Text'
    result = '!!! note "Test"\n\tText'
    assert (convert(mkdown) == result)


def test_links():
    # Test link in callout
    mkdown = '> [!NOTE] A [Link](https://example.com)\n> Text'
    result = '!!! note "A [Link](https://example.com)"\n\tText'
    assert (convert(mkdown) == result)

    # Test images in callout
    mkdown = '> [!NOTE]\n> ![](image.png)'
    result = '!!! note\n\t![](image.png)'
    assert (convert(mkdown) == result)


def test_nested_callouts():
    # Test nested callouts
    mkdown = '>[!INFO]-\n> Folded content\n>>[!INFO]+\n>> Folded content'
    result = '??? info\n\tFolded content\n\t???+ info\n\t\tFolded content'
    assert (convert(mkdown) == result)


def test_custom_callouts():
    mkdown = '> [!CUSTOM] Custom callout\n> Text'
    result = '!!! custom "Custom callout"\n\tText'
    assert (convert(mkdown) == result)


def test_inline_blocks():
    mkdown = '> [!infobox|left]\n> Text'
    result = '!!! infobox inline\n\tText'
    assert (convert(mkdown) == result)

    mkdown = '> [!infobox|right]\n> Text'
    result = '!!! infobox inline end\n\tText'
    assert (convert(mkdown) == result)

    mkdown = '> [!infobox|other] Title\n> Text'
    result = '!!! infobox "Title"\n\tText'
    assert (convert(mkdown) == result)


def test_folded_callouts():
    # Test folded block, closed by default
    mkdown = '> [!INFO]- Folded block\n> Folded content'
    result = '??? info "Folded block"\n\tFolded content'
    assert (convert(mkdown) == result)

    # Test folded block, open by default
    mkdown = '> [!INFO]+ Folded block\n> Folded content'
    result = '???+ info "Folded block"\n\tFolded content'
    assert (convert(mkdown) == result)

    # Test folded block, closed by default, untitled
    mkdown = '> [!INFO]-\n> Folded content'
    result = '??? info\n\tFolded content'
    assert (convert(mkdown) == result)

    # Test folded block, open by default, untitled
    mkdown = '> [!INFO]+\n> Folded content'
    result = '???+ info\n\tFolded content'
    assert (convert(mkdown) == result)


def test_aliases_enabled():
    parser = CalloutParser(convert_aliases=True)

    # Test alias conversion
    mkdown = '> [!HINT]\n> Text'
    result = '!!! tip\n\tText'
    assert (parser.parse(mkdown) == result)

    # Test alias conversion with inline block syntax
    mkdown = '> [!HINT | inline]\n> Text'
    result = '!!! tip inline\n\tText'
    assert (parser.parse(mkdown) == result)

    # Test alias conversion where alias is a substring of another alias
    mkdown = '> [!checking]\n> Text'
    unexpected = '!!! successing\n\tText'
    result = '!!! checking\n\tText'
    assert (parser.parse(mkdown) == result)
    assert (parser.parse(mkdown) != unexpected)

    # Test alias conversion where alias is a substring of another alias, with inline block syntax
    mkdown = '> [!checking | inline]\n> Text'
    unexpected = '!!! successing inline\n\tText'
    result = '!!! checking inline\n\tText'
    assert (parser.parse(mkdown) == result)
    assert (parser.parse(mkdown) != unexpected)

    # Test alias where first word is not an alias
    mkdown = '> [!A HINT]\n> Text'
    result = '!!! a hint\n\tText'
    assert (parser.parse(mkdown) == result)

    mkdown = '> [!A_HINT]\n> Text'
    result = '!!! a_hint\n\tText'
    assert (parser.parse(mkdown) == result)


def test_aliases_disabled():
    parser = CalloutParser(convert_aliases=False)

    mkdown = '> [!HINT]\n> Text'
    unexpected = '!!! tip\n\tText'
    result = '!!! hint\n\tText'
    assert (parser.parse(mkdown) == result)
    assert (parser.parse(mkdown) != unexpected)


def test_nested_callouts_with_spaces():
    parser = CalloutParser(convert_aliases=True)

    mkdown = '> [!INFO]\n> > [!INFO]'
    result = '!!! info\n\t!!! info'
    assert (parser.parse(mkdown) == result)


    mkdown = '> [!INFO]\n> > [!INFO] Title\n> > > [!INFO]\n> [!INFO]\n > [!INFO]'
    result = '!!! info\n\t!!! info "Title"\n\t\t!!! info\n!!! info\n!!! info'
    assert (parser.parse(mkdown) == result)


def test_nested_callouts_with_blockquotes():
    parser = CalloutParser(convert_aliases=True)

    mkdown = '> [!INFO]\n> > blockquote'
    result = '!!! info\n\t> blockquote'
    assert (parser.parse(mkdown) == result)

    mkdown = '> [!INFO]\n> > blockquote\n> > > blockquote'
    result = '!!! info\n\t> blockquote\n\t> > blockquote'
    assert (parser.parse(mkdown) == result)

    mkdown = '> [!INFO]\n> > [!INFO]\n> text\n> > blockquote'
    result = '!!! info\n\t!!! info\n\ttext\n\t> blockquote'
    assert (parser.parse(mkdown) == result)


def test_breakless_lists():
    parser = CalloutParser(convert_aliases=True, breakless_lists=False)

    mkdown = '> [!INFO]\n> text\n> - item 1\n> - item 2'
    result = '!!! info\n\ttext\n\t- item 1\n\t- item 2'
    assert (parser.parse(mkdown) == result)

    parser = CalloutParser(convert_aliases=True, breakless_lists=True)

    mkdown = '> [!INFO]\n> text\n> - item 1\n> - item 2'
    result = '!!! info\n\ttext\n\t\n\t- item 1\n\t- item 2'
    assert (parser.parse(mkdown) == result)

    # Shouldn't interfere with standard lists following the correct syntax
    mkdown = '> [!INFO]\n>\n> - item 1\n> - item 2\n> text'
    result = '!!! info\n\t\n\t- item 1\n\t- item 2\n\ttext'
    assert (parser.parse(mkdown) == result)

    # Nested callouts
    mkdown = '> [!INFO]\n> > [!INFO]\n> > text\n> > - item 1\n> > - item 2\n> text\n> - item 1\n> - item 2'
    result = '!!! info\n\t!!! info\n\t\ttext\n\t\t\n\t\t- item 1\n\t\t- item 2\n\ttext\n\t\n\t- item 1\n\t- item 2'
    assert (parser.parse(mkdown) == result)

    # Ordered lists
    mkdown = '> [!INFO]\n> text\n> 1. item 1\n> 2. item 2'
    result = '!!! info\n\ttext\n\t\n\t1. item 1\n\t2. item 2'
    assert (parser.parse(mkdown) == result)

    # Non-lists that look like lists
    mkdown = '> [!INFO]\n> text\n> *Not a list*\n> text\n> *: Not a list'
    result = '!!! info\n\ttext\n\t*Not a list*\n\ttext\n\t*: Not a list'
    assert (parser.parse(mkdown) == result)


def test_edgecase_in_nested_callouts():
    # Go from 1, 2, 3 callouts back to 1
    mkdown = '> [!INFO]\n> > [!INFO]\n> > > [!INFO]\n> > > Text\n> Text'
    result = '!!! info\n\t!!! info\n\t\t!!! info\n\t\t\tText\n\tText'
    assert (convert(mkdown) == result)


def test_callout_in_codeblocks():
    mkdown = '```markdown\n> [!INFO]\n> Text\n```'
    assert (convert(mkdown) == mkdown)

    # Edgecase where the callout might continue after a codeblock
    mkdown = '> [!INFO]\n```\n> code\n```\n> Text'
    result = '!!! info\n```\n> code\n```\n> Text'
    assert (convert(mkdown) == result)

    mkdown = '> [!INFO]\n```\n> code\n```\n> Blockquote\n> [!INFO]\n> Text'
    result = '!!! info\n```\n> code\n```\n> Blockquote\n!!! info\n\tText'
    assert (convert(mkdown) == result)


# TODO: We could handle this edgecase, but it's probably not worth the effort
@pytest.mark.xfail
def test_callout_in_codeblocks_within_callout():
    # A codefence within a callout containing a callout will still be converted
    # Though it's probably not worth the effort to handle this edgecase in the parser
    # Given how unlikely it is to occur in practice
    mkdown = '> [!INFO]\n> ```\n> [!INFO]\n> ```'
    result = '!!! info\n\t```\n> [!INFO]\n\t```'
    assert (convert(mkdown) == result)


def test_content_tabs():
    # Spaces are converted to tabs, which get preserved in the output
    mkdown = '=== "rendered"\n\n    > [!note] Custom title here\n    > Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
    result = '=== "rendered"\n\n\t!!! note "Custom title here"\n\t\tLorem ipsum dolor sit amet, consectetur adipiscing elit.'
    assert (convert(mkdown) == result)

    # Codefences don't get converted
    mkdown = '=== "source"\n\n    ```markdown\n    > [!note] Custom title here\n    > Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n    ```'
    result = '=== "source"\n\n    ```markdown\n    > [!note] Custom title here\n    > Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n    ```'
    assert (convert(mkdown) == result)

    # Embedded content works as well
    mkdown = '> [!NOTE]\n>\t=== "test"'
    result = '!!! note\n\t\t=== "test"'
    assert (convert(mkdown) == result)

    # Embedded content with nested callouts will "work", but the formatting isn't really intuitive
    # (Can't use > for the content tab callout, has to be tabs or spaces)
    # Though this is a very unlikely edgecase and one should probably just use the standard syntax
    # shown in the documentation (https://squidfunk.github.io/mkdocs-material/reference/content-tabs/#embedded-content)
    # Example:
    mkdown = '> [!NOTE]\n\t=== "test"\n\t\t> [!NOTE]\n\t\t> Text'
    result = '!!! note\n\t=== "test"\n\t\t!!! note\n\t\t\tText'
    assert (convert(mkdown) == result)