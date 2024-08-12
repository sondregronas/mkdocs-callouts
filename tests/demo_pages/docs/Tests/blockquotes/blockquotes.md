# Blockquotes

## Using callout syntax

> Blockquote
> > [!NOTE]
> > This is a nested note.
> Back in the blockquote now

> [!TIP]
> > Blockquote inside tip
> > > [!WARNING]
> > > This is a nested warning inside a blockquote inside a tip
> > Back in the blockquote
> > [!DANGER]
> > A danger callout inside a tip
> > > [!TIP]
> > > A tip inside a danger callout inside a tip
> Back in the tip (Note, this needs an extra line break to render correctly)


## Using admonition syntax

> Blockquote
> !!! note
>     This is a nested note.
> Back in the blockquote now

!!! tip
    > Blockquote inside tip
    > !!! warning
    >     This is a nested warning inside a blockquote inside a tip
    > Back in the blockquote
    !!! danger
        A danger callout inside a tip
        !!! tip
            A tip inside a danger callout inside a tip

    Back in the tip (Note, this needs an extra line break to render correctly)

## Source

```md
> Blockquote
> > [!NOTE]
> > This is a nested note.
> Back in the blockquote now

> [!TIP]
> > Blockquote inside tip
> > > [!WARNING]
> > > This is a nested warning inside a blockquote inside a tip
> > Back in the blockquote
> > [!DANGER]
> > A danger callout inside a tip
> > > [!TIP]
> > > A tip inside a danger callout inside a tip
> Back in the tip (Note, this needs an extra line break to render correctly)
```