# Tricky blockquote nesting

This page is to test the compatability between blockquotes and callouts with unusual nesting.

> > [!NOTE]
> > > Blockquote inside a note
> > > > [!WARNING]
> > > > This should be inside the warning callout
> > > > > [!TIP] This should be a callout
> > > > > This should be inside the tip callout
> > > > > > > > > [!DANGER]
> > > > > > > > > > Blockquote
> > [!TIP]

## In admonition syntax

> !!! note
>     > Blockquote inside a note
>     > !!! warning
>     >     This should be inside the warning callout
>     >     !!! tip "This should be a callout"
>     >         This should be inside the tip callout
>     >         > > > !!! danger
>     >         > > >     > Blockquote
> !!! tip

## Source

```md
> > [!NOTE]
> > > Blockquote inside a note
> > > > [!WARNING]
> > > > This should be inside the warning callout
> > > > > [!TIP] This should be a callout
> > > > > This should be inside the tip callout
> > > > > > > > > [!DANGER]
> > > > > > > > > > Blockquote
> > [!TIP]

## In admonition syntax

> !!! note
>     > Blockquote inside a note
>     > !!! warning
>     >     This should be inside the warning callout
>     >     !!! tip "This should be a callout"
>     >         This should be inside the tip callout
>     >         > > > !!! danger
>     >         > > >     > Blockquote
> !!! tip
```