# Nesting in blockquotes

The culprit is likely inconsistent spacing between blockquotes and callouts. Callouts need to be indented to correctly to be recognized as a callout, and since we indent using tabs and `>` characters they can go "out of sync".

It could also be something completely different.

Feel free to open a PR or issue if you have a solution for this.

### Example
```md
!!! note
    Works

!!! note 
   Doesn't work
```

> > [!NOTE]
> > > Blockquote inside a note
> > > > [!WARNING]
> > > > This should be inside the warning callout
> > > > > [!TIP] This should be a callout
> > > > > This should be inside the tip callout

## In admonition syntax it works

> !!! note
>     > Blockquote inside a note
>     > !!! warning
>     >     This should be inside the warning callout
>     >     !!! tip This should be a callout
>               This should be inside the tip callout


## Source

```md
> > [!NOTE]
> > > Blockquote inside a note
> > > > [!WARNING]
> > > > This should be inside the warning callout
> > > > > [!TIP] This should be a callout
> > > > > This should be inside the tip callout

## In admonition syntax it works

> !!! note
>     > Blockquote inside a note
>     > !!! warning
>     >     This should be inside the warning callout
>     >     !!! tip This should be a callout
>               This should be inside the tip callout
```

## What it gets converted to

Note the inconsistent spacing

```md
> !!! note
>       > Blockquote inside a note
>   > !!! warning
>   >   This should be inside the warning callout
>   >   !!! tip "This should be a callout"
>   >       This should be inside the tip callout
```