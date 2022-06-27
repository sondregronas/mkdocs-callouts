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

    # Test wikilink
    test_markdown = '> [[Wikilink]] in a block\n> [Link](https://example.com)'
    assert ('> [[Wikilink]] in a block\n> [Link](https://example.com)'
            in plugin.on_page_markdown(test_markdown, None, None, None))
