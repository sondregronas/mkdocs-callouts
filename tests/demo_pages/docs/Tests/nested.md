# Nested callouts

## Using callout syntax

> [!NOTE]
> This is a nested note.
> > [!WARNING]
> > This is a nested warning.
> > > [!TIP]
> > > This is a nested tip.
> > > > [!DANGER]
> Back in the note now
> > [!CAUTION]
> > This is a nested caution.
> > > [!ERROR]
> > > This is a nested error.
> > > > [!NOTE]
> > > > This is a nested note.
> > > We are back in the error now
> [!TIP]
> This is not nested.

> [!TIP]
> > [!WARNING]
> > > [!TIP]
> > > Text in 3rd
> Text in 1st

## Using admonition syntax

!!! note
    This is a nested note.
    !!! warning
        This is a nested warning.
        !!! tip
            This is a nested tip.
            !!! danger
    Back in the note now
    !!! warning
        This is a nested caution.
        !!! danger  
            This is a nested error.
            !!! note
                This is a nested note.
            We are back in the error now
!!! tip
    This is not nested.

!!! tip
    !!! warning
        !!! tip
            Text in 3rd
    Text in 1st

## Source

```md
> [!NOTE]
> This is a nested note.
> > [!WARNING]
> > This is a nested warning.
> > > [!TIP]
> > > This is a nested tip.
> > > > [!DANGER]
> Back in the note now
> > [!CAUTION]
> > This is a nested caution.
> > > [!ERROR]
> > > This is a nested error.
> > > > [!NOTE]
> > > > This is a nested note.
> > > We are back in the error now
> [!TIP]
> This is not nested.

> [!TIP]
> > [!WARNING]
> > > [!TIP]
> > > Text in 3rd
> Text in 1st
```