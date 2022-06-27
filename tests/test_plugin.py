import pytest

from mkdocs_callouts.plugin import CalloutsPlugin


@pytest.fixture
def plugin():
    plugin = CalloutsPlugin()
    return plugin


def test_on_page_markdown(plugin):
    # Test untitled block
    test_markdown = '> [!INFO]\n> Unitled block'
    assert ('!!! info\n\tUnitled block'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test regular titled block
    test_markdown = '> [!INFO] Title\n> Titled block\n> Two lines'
    assert ('!!! info "Title"\n\tTitled block\n\tTwo lines'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test titles with spaces
    test_markdown = '> [!INFO] This title has spaces\n> And text'
    assert ('!!! info "This title has spaces"\n\tAnd text'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test titles with > symbols
    test_markdown = '> [!INFO] > in title >\n> text'
    assert ('!!! info "> in title >"\n\ttext'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test callout paragraphs (empty callout line)
    test_markdown = '> [!INFO] Title\n> Paragraph 1\n>\n> Paragraph 2'
    assert ('!!! info "Title"\n\tParagraph 1\n\t\n\tParagraph 2'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test > block within callout
    test_markdown = '> [!INFO] Title\n> > Block within callout'
    assert ('!!! info "Title"\n\t> Block within callout'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test > in callout content
    test_markdown = '> [!INFO] Title\n> The > character'
    assert ('!!! info "Title"\n\tThe > character'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test folded block, closed by default
    test_markdown = '> [!INFO]- Folded block\n> Folded content'
    assert ('??? info "Folded block"\n\tFolded content'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test folded block, open by default
    test_markdown = '> [!INFO]+ Folded block\n> Folded content'
    assert ('???+ info "Folded block"\n\tFolded content'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test folded block, closed by default, untitled
    test_markdown = '> [!INFO]-\n> Folded content'
    assert ('??? info\n\tFolded content'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # test multiple callouts
    test_markdown = '> [!INFO]-\n> Folded content\n>>[!INFO]+\n>> Folded content'
    assert ('??? info\n\tFolded content\n\t???+ info\n\t\tFolded content\n'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    test_markdown = '> [!INFO]-\n> Folded content'
    assert ('??? info\n\tFolded content'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test folded block, open by default, untitled
    test_markdown = '> [!INFO]+\n> Folded content'
    assert ('???+ info\n\tFolded content\n'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test non-callout blocks
    test_markdown = '> [!custom] Callout\n> Callout Text\nSome text\n> Block'
    assert ('!!! custom "Callout"\n\tCallout Text\nSome text\n> Block'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test wikilink in regular block
    test_markdown = '> [[Wikilink]] in a block\n> [Link](https://example.com)'
    assert ('> [[Wikilink]] in a block\n> [Link](https://example.com)'
            in plugin.on_page_markdown(test_markdown, None, None, None))

    # Test callouts without whitespace
    test_markdown = '>[!INFO] Title\n>Content'
    assert ('!!! info "Title"\n\tContent'
            in plugin.on_page_markdown(test_markdown, None, None, None))
