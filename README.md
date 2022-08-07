# mkdocs-callouts
[![Build Status](https://img.shields.io/github/workflow/status/sondregronas/mkdocs-callouts/CI)](https://github.com/sondregronas/mkdocs-callouts/)
[![GitHub latest commit](https://img.shields.io/github/last-commit/sondregronas/mkdocs-callouts)](https://github.com/sondregronas/mkdocs-callouts/commit/)
[![PyPi](https://img.shields.io/pypi/v/mkdocs-callouts)](https://pypi.org/project/mkdocs-callouts/)
[![AGPLv3 license](https://img.shields.io/github/license/sondregronas/mkdocs-callouts)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![codecov](https://codecov.io/gh/sondregronas/mkdocs-callouts/branch/main/graph/badge.svg?token=N5IDI7Q4NZ)](https://codecov.io/gh/sondregronas/mkdocs-callouts)
[![Buymeacoffee](https://badgen.net/badge/icon/buymeacoffee?icon=buymeacoffee&label)](https://www.buymeacoffee.com/u92RMis)

A simple plugin that converts Obsidian style callouts and converts them into mkdocs supported ['admonitions'](https://squidfunk.github.io/mkdocs-material/reference/admonitions/) (a.k.a. callouts).

## Setup
Install the plugin using pip:

`pip install mkdocs-callouts`

Activate the plugin in `mkdocs.yml`, note that some markdown_extensions are required for this plugin to function correctly:

```yaml
markdown_extensions:
  - nl2br
  - admonition
  - pymdownx.details
  - pymdownx.superfences

plugins:
  - search
  - callouts
```

> **Note:** If you have no `plugins` entry in your config file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

## Usage
mkdocs-callouts converts the following:
```
> [!INFO] Title
> An information callout from Obsidian
> inspired by the syntax from the Microsoft Docs
```
and turns it into:
```
!!! info "Title"
    An admonition block for MkDocs.
    Allowing you to edit your notes
    with confidence using Obsidian.
```

### Foldable blocks
Foldable blocks are also supported. (`> [!INFO]- Foldable closed by default`, `> [!INFO]+ Foldable open by default`)

### Inline blocks
To turn a callout block into an inline block you can use the `|left` or `|right` syntax in the type notation like so:
```
> [!INFO|left] -> !!! info inline (alt: [!INFO | left])
> [!INFO|inline] -> !!! info inline

> [!INFO|right] -> !!! info inline end 
> [!INFO|inline end] -> !!! info inline end
```

The following also works, but Obsidian may not render the block type correctly.
```
> [!INFO inline] --> !!! info inline
> [!INFO inline end] --> !!! info inline end
```
To get more information about inline blocks, or how to add your own custom callout blocks, check the [Material Mkdocs Documentation](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#inline-blocks).
