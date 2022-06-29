import pytest

from mkdocs_callouts.plugin import CalloutsPlugin


@pytest.fixture
def plugin():
    plugin = CalloutsPlugin()
    return plugin


def test_on_page_markdown(plugin):
    # Test untitled block
    test_markdown = '> [!INFO]\n> Unitled block'
    test_result = '!!! info\n\tUnitled block'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test regular titled block
    test_markdown = '> [!INFO] Title\n> Titled block\n> Two lines'
    test_result = '!!! info "Title"\n\tTitled block\n\tTwo lines'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test titles with spaces
    test_markdown = '> [!INFO] This title has spaces\n> And text'
    test_result = '!!! info "This title has spaces"\n\tAnd text'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test titles with > symbols
    test_markdown = '> [!INFO] > in title >\n> text'
    test_result = '!!! info "> in title >"\n\ttext'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test callout paragraphs (empty callout line)
    test_markdown = '> [!INFO] Title\n> Paragraph 1\n>\n> Paragraph 2'
    test_result = '!!! info "Title"\n\tParagraph 1\n\t\n\tParagraph 2'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test > block within callout
    test_markdown = '> [!INFO] Title\n> > Block within callout'
    test_result = '!!! info "Title"\n\t> Block within callout'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test > in callout content
    test_markdown = '> [!INFO] Title\n> The > character'
    test_result = '!!! info "Title"\n\tThe > character'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test folded block, closed by default
    test_markdown = '> [!INFO]- Folded block\n> Folded content'
    test_result = '??? info "Folded block"\n\tFolded content'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test folded block, open by default
    test_markdown = '> [!INFO]+ Folded block\n> Folded content'
    test_result = '???+ info "Folded block"\n\tFolded content'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test link in callout
    test_markdown = '> [!NOTE] A [Link](https://example.com)\n> Text'
    test_result = '!!! note "A [Link](https://example.com)"\n\tText'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test callout with leading spaces
    test_markdown = ' > [!NOTE] Test\n > Text'
    test_result = '!!! note "Test"\n\tText'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test callout without whitespace
    test_markdown = '>[!NOTE] Test\n>Text'
    test_result = '!!! note "Test"\n\tText'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test folded block, closed by default, untitled
    test_markdown = '> [!INFO]-\n> Folded content'
    test_result = '??? info\n\tFolded content'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # test multiple callouts
    test_markdown = '>[!INFO]-\n> Folded content\n>>[!INFO]+\n>> Folded content'
    test_result = '??? info\n\tFolded content\n\t???+ info\n\t\tFolded content'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    test_markdown = '> [!INFO]-\n> Folded content'
    test_result = '??? info\n\tFolded content'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test folded block, open by default, untitled
    test_markdown = '> [!INFO]+\n> Folded content'
    test_result = '???+ info\n\tFolded content'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test non-callout blocks
    test_markdown = '> [!custom] Callout\n> Callout Text\nSome text\n> Block'
    test_result = '!!! custom "Callout"\n\tCallout Text\nSome text\n> Block'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test link in regular block
    test_markdown = '> [[Wikilink]] in a block\n> [Link](https://example.com)'
    test_result = '> [[Wikilink]] in a block\n> [Link](https://example.com)'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))

    # Test callouts without whitespace
    test_markdown = '>[!INFO] Title\n>Content'
    test_result = '!!! info "Title"\n\tContent'
    assert (test_result == plugin.on_page_markdown(test_markdown, None, None, None))
